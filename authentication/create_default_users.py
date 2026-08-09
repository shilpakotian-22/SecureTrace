"""
Create Default Users
"""

import bcrypt

from app import app
from database.db import db
from authentication.models import User


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


with app.app_context():

    owner = User.query.filter_by(username="owner").first()

    if owner is None:

        owner = User(
            username="owner",
            password=hash_password("owner123"),
            role="OWNER"
        )

        db.session.add(owner)

    verifier = User.query.filter_by(username="verifier").first()

    if verifier is None:

        verifier = User(
            username="verifier",
            password=hash_password("verify123"),
            role="VERIFIER"
        )

        db.session.add(verifier)

    db.session.commit()

    print("Default users created successfully!")