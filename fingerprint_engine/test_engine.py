from fingerprint_engine.engine import FingerprintEngine

from fingerprint_engine.layers.unicode_layer import UnicodeLayer
from fingerprint_engine.layers.font_layer import FontLayer
from fingerprint_engine.layers.synonym_layer import SynonymLayer

from fingerprint_engine.utils.file_helper import copy_document

engine = FingerprintEngine()

engine.register_layer(
    UnicodeLayer()
)

engine.register_layer(
    FontLayer()
)

engine.register_layer(
    SynonymLayer()
)

document = copy_document(
    "uploads/sample.docx",
    "Alice"
)

engine.generate(
    document,
    "Alice"
)