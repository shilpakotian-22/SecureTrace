class BinaryMatcher:

    def compare(self, stored, extracted):

        if not stored or not extracted:

            return 0

        length = min(
            len(stored),
            len(extracted)
        )

        matches = 0

        for i in range(length):

            if stored[i] == extracted[i]:

                matches += 1

        return round(

            (matches / length) * 100,

            2

        )