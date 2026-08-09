import os

from fingerprint_engine.engine import FingerprintEngine
from fingerprint_engine.layers.unicode_layer import UnicodeLayer
from fingerprint_engine.layers.font_layer import FontLayer
from fingerprint_engine.layers.synonym_layer import SynonymLayer
from fingerprint_engine.utils.file_helper import copy_document

from database.db import db
from database.models import GeneratedDocument

from audit.services import log_action


def generate_document(assignment):
    """
    Generate a fingerprinted document for a single assignment.

    Returns:
        str: Generated document path on success.
        None: If generation fails.
    """

    copied_document = None

    try:

        # ---------------------------------------------------------
        # Validate assignment
        # ---------------------------------------------------------

        if assignment is None:

            print("Generation failed: assignment is None.")

            return None

        if assignment.document is None:

            print(
                f"Generation failed: assignment "
                f"{assignment.id} has no document."
            )

            return None

        if assignment.recipient is None:

            print(
                f"Generation failed: assignment "
                f"{assignment.id} has no recipient."
            )

            return None


        # ---------------------------------------------------------
        # Source document information
        # ---------------------------------------------------------

        document_path = assignment.document.filepath

        if not document_path:

            print(
                f"Generation failed: assignment "
                f"{assignment.id} has no document path."
            )

            return None


        if not os.path.isfile(document_path):

            print(
                f"Generation failed: source document does not exist: "
                f"{document_path}"
            )

            return None


        recipient = assignment.recipient.name

        recipient_email = assignment.recipient.email


        if not recipient:

            print(
                f"Generation failed: assignment "
                f"{assignment.id} has no recipient name."
            )

            return None


        if not recipient_email:

            print(
                f"Generation failed: assignment "
                f"{assignment.id} has no recipient email."
            )

            return None


        # ---------------------------------------------------------
        # Validate document type
        # ---------------------------------------------------------

        extension = os.path.splitext(
            document_path
        )[1].lower()


        if extension != ".docx":

            print(
                f"Generation skipped: unsupported document type "
                f"{extension}"
            )

            return None


        # ---------------------------------------------------------
        # Prevent duplicate generation
        # ---------------------------------------------------------

        existing_document = GeneratedDocument.query.filter_by(
            assignment_id=assignment.id
        ).first()


        if existing_document:

            existing_path = existing_document.generated_file

            if (
                existing_path
                and
                os.path.isfile(existing_path)
            ):

                print(
                    f"Fingerprint already exists for assignment "
                    f"{assignment.id}: {existing_path}"
                )

                return existing_path

            # Database record exists but generated file is missing.
            # Remove the stale record so generation can be rebuilt.

            db.session.delete(
                existing_document
            )

            db.session.commit()


        # ---------------------------------------------------------
        # Create fingerprint engine
        # ---------------------------------------------------------

        engine = FingerprintEngine()


        engine.register_layer(
            UnicodeLayer()
        )


        engine.register_layer(
            FontLayer()
        )


        engine.register_layer(
            SynonymLayer()
        )


        # ---------------------------------------------------------
        # Create recipient-specific copy
        # ---------------------------------------------------------

        copied_document = copy_document(
            document_path,
            recipient
        )


        if not copied_document:

            print(
                "Generation failed: document copy operation "
                "returned no output."
            )

            return None


        if not os.path.isfile(copied_document):

            print(
                "Generation failed: copied document does not exist: "
                f"{copied_document}"
            )

            return None


        print(
            f"Copied document to: {copied_document}"
        )


        # ---------------------------------------------------------
        # Generate fingerprints
        # ---------------------------------------------------------

        generation_result = engine.generate(
            copied_document,
            recipient
        )


        if not generation_result:

            print(
                "Generation failed: fingerprint engine "
                "returned no result."
            )

            return None


        # Current engine contract:
        # (generated_document_path, fingerprints)

        if not isinstance(
            generation_result,
            tuple
        ) or len(generation_result) != 2:

            print(
                "Generation failed: unexpected fingerprint "
                "engine response."
            )

            return None


        generated_path, fingerprints = generation_result


        if not generated_path:

            print(
                "Generation failed: fingerprint engine "
                "returned no document path."
            )

            return None


        if not os.path.isfile(generated_path):

            print(
                "Generation failed: fingerprinted document "
                "was not created: "
                f"{generated_path}"
            )

            return None


        if not isinstance(
            fingerprints,
            dict
        ):

            print(
                "Generation failed: fingerprint data is invalid."
            )

            return None


        # ---------------------------------------------------------
        # Extract fingerprint hashes
        # ---------------------------------------------------------

        unicode_hash = fingerprints.get(
            "UnicodeLayer"
        )

        font_hash = fingerprints.get(
            "FontLayer"
        )

        synonym_hash = fingerprints.get(
            "SynonymLayer"
        )


        if not unicode_hash:

            print(
                "Warning: Unicode fingerprint was not returned."
            )


        if not font_hash:

            print(
                "Warning: Font fingerprint was not returned."
            )


        if not synonym_hash:

            print(
                "Warning: Synonym fingerprint was not returned."
            )


        # ---------------------------------------------------------
        # Create database record
        # ---------------------------------------------------------

        generated = GeneratedDocument(

            assignment_id=assignment.id,

            recipient=recipient,

            recipient_email=recipient_email,

            unicode_hash=unicode_hash,

            font_hash=font_hash,

            synonym_hash=synonym_hash,

            generated_file=generated_path

        )


        db.session.add(
            generated
        )


        db.session.commit()


        # ---------------------------------------------------------
        # Audit logging
        # ---------------------------------------------------------
        #
        # The document has already been successfully committed.
        # Therefore an audit failure should not turn a successful
        # generation into a failed generation.
        # ---------------------------------------------------------

        try:

            log_action(

                "System",

                "Generated Fingerprinted Document",

                generated_path

            )

        except Exception as audit_error:

            print(
                "Warning: fingerprint generated successfully, "
                "but audit logging failed: "
                f"{audit_error}"
            )


        print(
            f"Fingerprint generation successful: "
            f"{generated_path}"
        )


        return generated_path


    except Exception as error:

        # ---------------------------------------------------------
        # Database rollback
        # ---------------------------------------------------------

        db.session.rollback()


        print(
            "Fingerprint generation failed: "
            f"{error}"
        )


        # ---------------------------------------------------------
        # Remove partially generated file
        # ---------------------------------------------------------

        if (
            copied_document
            and
            os.path.isfile(copied_document)
        ):

            try:

                os.remove(
                    copied_document
                )

                print(
                    f"Removed incomplete generated file: "
                    f"{copied_document}"
                )

            except OSError as cleanup_error:

                print(
                    "Warning: could not remove incomplete "
                    "generated file: "
                    f"{cleanup_error}"
                )


        return None