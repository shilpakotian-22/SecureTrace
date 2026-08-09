from detection.engine import DetectionEngine

from detection.detectors.unicode_detector import UnicodeDetector
from detection.detectors.font_detector import FontDetector
from detection.detectors.synonym_detector import SynonymDetector


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

result = engine.detect(

    "generated_documents/fingerprinted/DOC-20260514-WA0013_Alice.docx"

)

print()

print(result)