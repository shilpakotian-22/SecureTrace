"""
Fingerprint Engine
"""


class FingerprintEngine:

    def __init__(self):

        self.layers = []

    def register_layer(self, layer):

        self.layers.append(layer)

    def generate(self, document_path, recipient):

        output = document_path

        fingerprints = {}

        for layer in self.layers:

            output, fingerprint = layer.apply(
                output,
                recipient
            )

            fingerprints[layer.__class__.__name__] = fingerprint

        return output, fingerprints