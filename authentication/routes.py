from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from authentication.forms import LoginForm
from authentication.services import verify_user

from authentication.register_form import RegisterForm
from authentication.register_service import create_user

from authentication.models import User
from database.db import db

from audit.services import log_action


authentication = Blueprint(
    "authentication",
    __name__,
    url_prefix="/auth"
)


@authentication.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # ---------------------------------------------------------
    # Already logged in
    # ---------------------------------------------------------

    if "user_id" in session:

        return redirect(
            url_for(
                "dashboard.dashboard_home"
            )
        )


    form = LoginForm()


    if form.validate_on_submit():

        user = verify_user(

            form.email.data,

            form.password.data,

            form.role.data

        )


        if user:

            # -------------------------------------------------
            # Clear previous session
            # -------------------------------------------------

            session.clear()


            # -------------------------------------------------
            # Create authenticated session
            # -------------------------------------------------

            session["user_id"] = user.id

            session["full_name"] = user.full_name

            session["email"] = user.email

            session["role"] = user.role


            # -------------------------------------------------
            # Update last login
            # -------------------------------------------------

            user.last_login = db.func.now()

            db.session.commit()


            # -------------------------------------------------
            # Audit successful login
            # -------------------------------------------------

            log_action(

                user.full_name,

                "User Login",

                f"Successful login for {user.email}"

            )


            flash(
                "Login successful.",
                "success"
            )


            return redirect(
                url_for(
                    "dashboard.dashboard_home"
                )
            )


        # -----------------------------------------------------
        # Failed login
        # -----------------------------------------------------

        flash(
            "Invalid email, password or role.",
            "danger"
        )


        log_action(

            form.email.data or "Unknown",

            "Failed Login",

            "Invalid email, password or role."

        )


    return render_template(
        "login.html",
        form=form
    )


@authentication.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    form = RegisterForm()


    if form.validate_on_submit():

        success, message = create_user(

            form.full_name.data,

            form.email.data,

            form.password.data,

            form.role.data

        )


        if success:

            log_action(

                form.email.data,

                "User Registration",

                f"New user registered with role "
                f"{form.role.data}"

            )


            flash(
                message,
                "success"
            )


            return redirect(
                url_for(
                    "authentication.login"
                )
            )


        flash(
            message,
            "danger"
        )


    return render_template(

        "register.html",

        form=form

    )


@authentication.route(
    "/logout"
)
def logout():

    user_name = session.get(
        "full_name",
        "Unknown"
    )

    user_email = session.get(
        "email",
        "Unknown"
    )


    # ---------------------------------------------------------
    # Audit before clearing the session
    # ---------------------------------------------------------

    log_action(

        user_name,

        "User Logout",

        f"Logout for {user_email}"

    )


    # ---------------------------------------------------------
    # Completely destroy authentication session
    # ---------------------------------------------------------

    session.clear()


    flash(
        "You have been logged out successfully.",
        "success"
    )


    return redirect(
        url_for(
            "authentication.login"
        )
    )