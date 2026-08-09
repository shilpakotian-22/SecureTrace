from flask import (
    Blueprint,
    redirect,
    session,
    url_for,
    flash
)

from authentication.google_auth.oauth import oauth
from authentication.models import User
from database.db import db

from audit.services import log_action


google_auth = Blueprint(
    "google_auth",
    __name__,
    url_prefix="/auth/google"
)


@google_auth.route(
    "/login"
)
def login():

    redirect_uri = url_for(
        "google_auth.callback",
        _external=True
    )


    return oauth.google.authorize_redirect(
        redirect_uri
    )


@google_auth.route(
    "/callback"
)
def callback():

    try:

        # -----------------------------------------------------
        # Exchange authorization code for token
        # -----------------------------------------------------

        token = (
            oauth.google.authorize_access_token()
        )


        # -----------------------------------------------------
        # Get Google user information
        # -----------------------------------------------------

        google_user = token.get(
            "userinfo"
        )


        if not google_user:

            raise ValueError(
                "Google user information was not returned."
            )


        email = google_user.get(
            "email"
        )

        full_name = google_user.get(
            "name"
        )

        picture = google_user.get(
            "picture"
        )


        if not email:

            raise ValueError(
                "Google account email was not returned."
            )


        if not full_name:

            full_name = email


        # -----------------------------------------------------
        # Find existing user
        # -----------------------------------------------------

        user = User.query.filter_by(
            email=email
        ).first()


        # -----------------------------------------------------
        # Create new Google user
        # -----------------------------------------------------

        if user is None:

            user = User(

                full_name=full_name,

                email=email,

                password="GOOGLE_LOGIN",

                role="VERIFIER"

            )


            db.session.add(
                user
            )

            db.session.commit()


            log_action(

                email,

                "Google User Registration",

                "New Google account registered as VERIFIER."

            )


        else:

            # -------------------------------------------------
            # Update display information
            # -------------------------------------------------

            user.full_name = full_name


            if picture:

                # Picture is stored in the session rather
                # than the database.

                pass


            user.last_login = db.func.now()

            db.session.commit()


        # -----------------------------------------------------
        # Start clean authenticated session
        # -----------------------------------------------------

        session.clear()


        session["user_id"] = user.id

        session["full_name"] = user.full_name

        session["email"] = user.email

        session["role"] = user.role


        if picture:

            session["picture"] = picture


        # -----------------------------------------------------
        # Audit successful Google login
        # -----------------------------------------------------

        log_action(

            user.full_name,

            "Google Login",

            f"Successful Google login for {user.email}"

        )


        flash(
            "Google login successful.",
            "success"
        )


        return redirect(
            url_for(
                "dashboard.dashboard_home"
            )
        )


    except Exception as error:

        # -----------------------------------------------------
        # Rollback database if necessary
        # -----------------------------------------------------

        db.session.rollback()


        print(
            "Google authentication error:"
        )

        print(
            error
        )


        log_action(

            "Unknown",

            "Failed Google Login",

            "Google authentication failed."

        )


        flash(

            "Google authentication failed. "
            "Please try again.",

            "danger"

        )


        return redirect(
            url_for(
                "authentication.login"
            )
        )