"""
Database Models
"""

from datetime import datetime
from datetime import timedelta

from database.db import db


def indian_time():

    return datetime.utcnow() + timedelta(
        hours=5,
        minutes=30
    )


class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    filepath = db.Column(
        db.String(500),
        nullable=False
    )

    uploaded_by = db.Column(
        db.String(50),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=indian_time
    )

    assignments = db.relationship(
        "Assignment",
        back_populates="document"
    )

    def __repr__(self):

        return f"<Document {self.filename}>"


class Recipient(db.Model):

    __tablename__ = "recipients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    organization = db.Column(
        db.String(150),
        nullable=False
    )

    assignments = db.relationship(
        "Assignment",
        back_populates="recipient"
    )

    def __repr__(self):

        return f"<Recipient {self.name}>"


class Assignment(db.Model):

    __tablename__ = "assignments"

    __table_args__ = (
        db.UniqueConstraint(
            "document_id",
            "recipient_id",
            name="uq_assignment_document_recipient"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "documents.id"
        ),
        nullable=False
    )

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "recipients.id"
        ),
        nullable=False
    )

    assigned_at = db.Column(
        db.DateTime,
        default=indian_time,
        nullable=False
    )

    document = db.relationship(
        "Document",
        back_populates="assignments"
    )

    recipient = db.relationship(
        "Recipient",
        back_populates="assignments"
    )

    generated_document = db.relationship(
        "GeneratedDocument",
        back_populates="assignment",
        uselist=False
    )

    def __repr__(self):

        return (
            f"<Assignment "
            f"{self.id}: "
            f"document={self.document_id}, "
            f"recipient={self.recipient_id}>"
        )


class GeneratedDocument(db.Model):

    __tablename__ = "generated_documents"

    __table_args__ = (
        db.UniqueConstraint(
            "assignment_id",
            name="uq_generated_document_assignment"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    assignment_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "assignments.id"
        ),
        nullable=False
    )

    recipient = db.Column(
        db.String(100),
        nullable=False
    )

    recipient_email = db.Column(
        db.String(150),
        nullable=False
    )

    unicode_hash = db.Column(
        db.String(64)
    )

    font_hash = db.Column(
        db.String(64)
    )

    synonym_hash = db.Column(
        db.String(64)
    )

    generated_file = db.Column(
        db.String(500),
        nullable=False
    )

    generated_at = db.Column(
        db.DateTime,
        default=indian_time,
        nullable=False
    )

    email_status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    assignment = db.relationship(
        "Assignment",
        back_populates="generated_document"
    )

    def __repr__(self):

        return (
            f"<GeneratedDocument "
            f"{self.id}: "
            f"{self.recipient}>"
        )


class DetectionHistory(db.Model):

    __tablename__ = "detection_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    uploaded_file = db.Column(
        db.String(255),
        nullable=False
    )

    detected_recipient = db.Column(
        db.String(120),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    detected_at = db.Column(
        db.DateTime,
        default=indian_time
    )

    def __repr__(self):

        return (
            f"<DetectionHistory "
            f"{self.id}: "
            f"{self.detected_recipient}>"
        )


class EmailHistory(db.Model):

    __tablename__ = "email_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender = db.Column(
        db.String(150),
        nullable=False
    )

    recipient = db.Column(
        db.String(150),
        nullable=False
    )

    subject = db.Column(
        db.String(250),
        nullable=False
    )

    attachment = db.Column(
        db.String(500),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending",
        nullable=False
    )

    sent_at = db.Column(
        db.DateTime,
        default=indian_time
    )

    def __repr__(self):

        return (
            f"<EmailHistory "
            f"{self.id}: "
            f"{self.recipient}>"
        )


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user = db.Column(
        db.String(150),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    details = db.Column(
        db.Text
    )

    timestamp = db.Column(
        db.DateTime,
        default=indian_time
    )

    def __repr__(self):

        return (
            f"<AuditLog "
            f"{self.id}: "
            f"{self.action}>"
        )


class AppSettings(db.Model):

    __tablename__ = "app_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    organization = db.Column(
        db.String(200),
        default="SecureTrace"
    )

    application_name = db.Column(
        db.String(200),
        default="SecureTrace"
    )

    default_sender = db.Column(
        db.String(150),
        default=""
    )

    timezone = db.Column(
        db.String(50),
        default="Asia/Kolkata"
    )

    max_upload_size = db.Column(
        db.Integer,
        default=20
    )

    def __repr__(self):

        return (
            f"<AppSettings "
            f"{self.application_name}>"
        )