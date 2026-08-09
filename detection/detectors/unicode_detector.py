from fingerprint_engine.utils.docx_helper import open_document


ZERO_WIDTH_SPACE = "\u200B"
ZERO_WIDTH_NON_JOINER = "\u200C"


class UnicodeDetector:

    def extract(self, document_path):

        document = open_document(document_path)

        binary = ""

        for paragraph in document.paragraphs:

            if paragraph.text.endswith(
                ZERO_WIDTH_SPACE
            ):

                binary += "0"

            elif paragraph.text.endswith(
                ZERO_WIDTH_NON_JOINER
            ):

                binary += "1"

        return "UnicodeLayer", binary