from database.db import db
from database.models import Recipient


def add_recipient(name, email, department, organization):

    existing = Recipient.query.filter_by(
        email=email
    ).first()

    if existing:
        return "duplicate"

    recipient = Recipient(
        name=name,
        email=email,
        department=department,
        organization=organization
    )

    db.session.add(recipient)
    db.session.commit()

    return recipient


def update_recipient(recipient, name, email, department, organization):

    recipient.name = name
    recipient.email = email
    recipient.department = department
    recipient.organization = organization

    db.session.commit()