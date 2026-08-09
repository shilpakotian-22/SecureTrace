from docx.shared import Pt

from fingerprint_engine.utils.docx_helper import open_document


class FontDetector:

    def extract(self, document_path):

        document = open_document(document_path)

        binary = ""

        for paragraph in document.paragraphs:

            for run in paragraph.runs:

                if not run.text.strip():
                    continue

                size = run.font.size

                print(run.text, size)

                if size is None:
                    continue

                if abs(size.pt - 11) < 0.2:
                    binary += "0"

                elif abs(size.pt - 11.5) < 0.2:
                    binary += "1"

        return "FontLayer", binary