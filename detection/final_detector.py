class FinalDetector:

    def identify(self, matches):

        if not matches:
            return None

        matches = sorted(
            matches,
            key=lambda item: item["confidence"],
            reverse=True
        )

        best = matches[0]

        if best["confidence"] < 40:

            return {
                "recipient": "Unknown",
                "recipient_email": "-",
                "generated_file": "-",
                "assignment_id": "-",
                "unicode": 0,
                "font": 0,
                "synonym": 0,
                "confidence": 0
            }

        return best