from sqlalchemy.exc import IntegrityError

from database.db import db
from database.models import (
    Assignment,
    Document,
    Recipient
)


def assign_document(document_id, recipient_id):
    """
    Create an assignment between a document and recipient.

    Returns:
        Assignment object on success
        "duplicate" if assignment already exists
        "document_not_found" if document does not exist
        "recipient_not_found" if recipient does not exist
        "error" if a database error occurs
    """

    # ---------------------------------------------------------
    # Validate document
    # ---------------------------------------------------------

    document = Document.query.get(document_id)

    if document is None:

        return "document_not_found"


    # ---------------------------------------------------------
    # Validate recipient
    # ---------------------------------------------------------

    recipient = Recipient.query.get(recipient_id)

    if recipient is None:

        return "recipient_not_found"


    # ---------------------------------------------------------
    # Prevent duplicate assignment
    # ---------------------------------------------------------

    existing = Assignment.query.filter_by(
        document_id=document.id,
        recipient_id=recipient.id
    ).first()


    if existing:

        return "duplicate"


    # ---------------------------------------------------------
    # Create assignment
    # ---------------------------------------------------------

    assignment = Assignment(

        document_id=document.id,

        recipient_id=recipient.id

    )


    try:

        db.session.add(
            assignment
        )

        db.session.commit()


        return assignment


    except IntegrityError:

        db.session.rollback()

        # This protects against a duplicate created by
        # another request at nearly the same time.

        existing = Assignment.query.filter_by(

            document_id=document.id,

            recipient_id=recipient.id

        ).first()


        if existing:

            return "duplicate"


        return "error"


    except Exception:

        db.session.rollback()

        return "error"