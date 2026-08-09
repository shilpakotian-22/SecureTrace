from app import app

from detection.engine import DetectionEngine

from detection.detectors.unicode_detector import UnicodeDetector
from detection.detectors.font_detector import FontDetector
from detection.detectors.synonym_detector import SynonymDetector

from detection.matchers.database_matcher import DatabaseMatcher
from detection.final_detector import FinalDetector

with app.app_context():

    engine = DetectionEngine()

    engine.register_detector(
        UnicodeDetector()
    )

    engine.register_detector(
        FontDetector()
    )

    engine.register_detector(
        SynonymDetector()
    )

    fingerprints = engine.detect(

        "generated_documents/fingerprinted/DOC-20260514-WA0013_Alice.docx"

    )

    matcher = DatabaseMatcher()

    results = matcher.find_matches(
        fingerprints
    )

    detector = FinalDetector()

    best = detector.identify(
        results
    )

    print()

    print()

    print("=" * 40)

    print("LEAK DETECTION RESULT")

    print("=" * 40)

    print()

    print(best)