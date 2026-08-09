class ConfidenceMatcher:

    def calculate(
        self,
        unicode_score,
        font_score,
        synonym_score
    ):

        confidence = (

            unicode_score * 0.4 +

            font_score * 0.4 +

            synonym_score * 0.2

        )

        return round(
            confidence,
            2
        )