from detection.matchers.binary_matcher import BinaryMatcher

matcher = BinaryMatcher()

stored = "11001100"

extracted = "11011100"

score = matcher.compare(
    stored,
    extracted
)

print()

print("Similarity:", score, "%")