import re

from fingerprint_engine.utils.docx_helper import open_document
from fingerprint_engine.utils.synonym_dictionary import SYNONYMS


class SynonymDetector:

    def extract(self, document_path):

        document = open_document(document_path)

        binary = ""

        reverse_dictionary = {
            value: key
            for key, value in SYNONYMS.items()
        }

        for paragraph in document.paragraphs:

            words = re.findall(
                r"\w+",
                paragraph.text.lower()
            )

            for word in words:

                if word in SYNONYMS:

                    binary += "0"

                elif word in reverse_dictionary:

                    binary += "1"

        return "SynonymLayer", binary