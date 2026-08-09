from docx import Document


def open_document(filepath):

    return Document(filepath)


def save_document(document, filepath):

    document.save(filepath)