"""
User Model
Project: SecureTrace
"""

from datetime import datetime, timedelta

def indian_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

from database.db import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=indian_time
    )

    last_login = db.Column(
        db.DateTime
    )

    def __repr__(self):

        return f"<User {self.email}>"