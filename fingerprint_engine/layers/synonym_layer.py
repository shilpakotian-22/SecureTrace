import re

from fingerprint_engine.utils.hash_helper import synonym_fingerprint
from fingerprint_engine.utils.synonym_dictionary import SYNONYMS

from fingerprint_engine.utils.docx_helper import (
    open_document,
    save_document
)


class SynonymLayer:

    def apply(self, document_path, recipient):

        fingerprint = synonym_fingerprint(recipient)

        binary = fingerprint

        document = open_document(document_path)

        bit_index = 0

        replacements = 0

        for paragraph in document.paragraphs:

            for run in paragraph.runs:

                if not run.text.strip():
                    continue

                text = run.text

                words = re.findall(r"\w+|[^\w\s]", text)

                new_words = []

                for word in words:

                    clean = word.lower()

                    if clean in SYNONYMS and bit_index < len(binary):

                        if binary[bit_index] == "1":

                            replacement = SYNONYMS[clean]

                            if word[0].isupper():

                                replacement = replacement.capitalize()

                            new_words.append(replacement)

                            replacements += 1

                        else:

                            new_words.append(word)

                        bit_index += 1

                    else:

                        new_words.append(word)

                run.text = ""

                for i, token in enumerate(new_words):

                    if i > 0 and token.isalnum() and new_words[i-1].isalnum():

                        run.text += " "

                    run.text += token

        save_document(
            document,
            document_path
        )

        print(
            f"Synonym Layer Replaced {replacements} words"
        )

        return document_path, fingerprint