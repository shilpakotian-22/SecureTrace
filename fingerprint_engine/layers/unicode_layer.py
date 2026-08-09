from fingerprint_engine.utils.hash_helper import unicode_fingerprint
from fingerprint_engine.utils.docx_helper import (
    open_document,
    save_document
)


ZERO_WIDTH_SPACE = "\u200B"
ZERO_WIDTH_NON_JOINER = "\u200C"


class UnicodeLayer:

    def apply(self, document_path, recipient):

        # Binary fingerprint for this recipient
        fingerprint = unicode_fingerprint(recipient)

        # We will embed these bits
        binary = fingerprint

        document = open_document(document_path)

        bit_index = 0

        for paragraph in document.paragraphs:

            if not paragraph.text.strip():
                continue

            if bit_index >= len(binary):
                break

            if binary[bit_index] == "0":

                paragraph.text += ZERO_WIDTH_SPACE

            else:

                paragraph.text += ZERO_WIDTH_NON_JOINER

            bit_index += 1

        save_document(
            document,
            document_path
        )

        print(
            f"Unicode Layer Embedded {bit_index} bits"
        )

        # Return BOTH the modified document path and the fingerprint
        return document_path, fingerprint