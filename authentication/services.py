import bcrypt

from authentication.models import User
from database.db import db
from datetime import datetime, timedelta

def indian_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

def verify_user(email, password, role):

    user = User.query.filter_by(
        email=email,
        role=role
    ).first()

    if user is None:
        return None

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    ):

        user.last_login = indian_time()

        db.session.commit()

        return user

    return None