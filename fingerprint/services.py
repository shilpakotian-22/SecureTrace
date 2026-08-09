"""
Fingerprint Services
"""

import os

from database.db import db
from database.models import Document

ALLOWED_EXTENSIONS = {
    "docx",
    "pdf"
}

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


def save_uploaded_document(file, uploaded_by):

    if not allowed_file(file.filename):
        return "invalid"

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    document = Document(
        filename=file.filename,
        filepath=filepath,
        uploaded_by=uploaded_by
    )

    db.session.add(document)
    db.session.commit()

    return document