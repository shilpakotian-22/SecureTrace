import bcrypt

from authentication.models import User
from database.db import db


def create_user(
    full_name,
    email,
    password,
    role
):

    existing = User.query.filter_by(
        email=email
    ).first()

    if existing:

        return False, "Email already registered."

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(

        full_name=full_name,

        email=email,

        password=hashed,

        role=role

    )

    db.session.add(user)

    db.session.commit()

    return True, "Account created successfully."