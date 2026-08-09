from detection.engine import DetectionEngine

from detection.detectors.unicode_detector import UnicodeDetector
from detection.detectors.font_detector import FontDetector
from detection.detectors.synonym_detector import SynonymDetector

from detection.matchers.database_matcher import DatabaseMatcher
from detection.final_detector import FinalDetector

from database.db import db

from database.models import DetectionHistory
from audit.services import log_action


def detect_leak(document_path):

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
        document_path
    )

    matcher = DatabaseMatcher()

    matches = matcher.find_matches(
        fingerprints
    )

    detector = FinalDetector()

    best_match = detector.identify(matches)

    if best_match is None:

        return {
            "recipient": "Unknown",
            "confidence": 0
        }

    history = DetectionHistory(

        uploaded_file=document_path,

        detected_recipient=best_match["recipient"],

        confidence=best_match["confidence"]

    )

    db.session.add(history)
    db.session.commit()

    log_action(

        "System",

        "Leak Detection",

        best_match["recipient"]

    )

    return best_match