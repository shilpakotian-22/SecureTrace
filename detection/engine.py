"""
Leak Detection Engine
"""


class DetectionEngine:

    def __init__(self):

        self.detectors = []

    def register_detector(self, detector):

        self.detectors.append(detector)

    def detect(self, document_path):

        fingerprints = {}

        for detector in self.detectors:

            name, fingerprint = detector.extract(
                document_path
            )

            fingerprints[name] = fingerprint

        return fingerprints