from database.models import GeneratedDocument

from detection.matchers.binary_matcher import BinaryMatcher

from detection.matchers.confidence_matcher import ConfidenceMatcher

class DatabaseMatcher:

    def __init__(self):

        self.matcher = BinaryMatcher()

        self.confidence = ConfidenceMatcher()

    def find_matches(self, fingerprints):

        results = []

        documents = GeneratedDocument.query.all()

        for document in documents:

            unicode_score = self.matcher.compare(
                document.unicode_hash,
                fingerprints.get("UnicodeLayer", "")
            )

            font_score = self.matcher.compare(
                document.font_hash,
                fingerprints.get("FontLayer", "")
            )

            synonym_score = self.matcher.compare(
                document.synonym_hash,
                fingerprints.get("SynonymLayer", "")
            )

            confidence = self.confidence.calculate(
                unicode_score,
                font_score,
                synonym_score
            )

            results.append({

                "recipient": document.recipient,

                "recipient_email": document.recipient_email,

                "generated_file": document.generated_file,

                "generated_at": document.generated_at,

                "email_status": document.email_status,

                "assignment_id": document.assignment_id,

                "unicode": unicode_score,

                "font": font_score,

                "synonym": synonym_score,

                "confidence": confidence

            })

        return results