from docx.shared import Pt

from fingerprint_engine.utils.hash_helper import font_fingerprint
from fingerprint_engine.utils.docx_helper import (
    open_document,
    save_document
)


class FontLayer:

    def apply(self, document_path, recipient):

        # Generate recipient fingerprint
        fingerprint = font_fingerprint(recipient)

        # Use it for embedding
        binary = fingerprint

        document = open_document(document_path)

        bit_index = 0

        for paragraph in document.paragraphs:

            for run in paragraph.runs:

                if not run.text.strip():
                    continue

                if bit_index >= len(binary):
                    break

                if binary[bit_index] == "0":

                    run.font.size = Pt(11)

                else:

                    run.font.size = Pt(11.5)

                bit_index += 1

            if bit_index >= len(binary):
                break

        save_document(
            document,
            document_path
        )

        print(
            f"Font Layer Embedded {bit_index} bits"
        )

        # Return BOTH the modified document and the fingerprint
        return document_path, fingerprint