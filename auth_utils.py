from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    flash
)


def login_required(view_function):
    """
    Require an authenticated user.
    """

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please log in to continue.",
                "warning"
            )

            return redirect(
                url_for(
                    "authentication.login"
                )
            )

        return view_function(
            *args,
            **kwargs
        )

    return wrapped_view


def owner_required(view_function):
    """
    Require an authenticated OWNER.
    """

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please log in to continue.",
                "warning"
            )

            return redirect(
                url_for(
                    "authentication.login"
                )
            )


        if session.get("role") != "OWNER":

            flash(
                "You do not have permission to access this page.",
                "danger"
            )

            return redirect(
                url_for(
                    "dashboard.dashboard_home"
                )
            )


        return view_function(
            *args,
            **kwargs
        )

    return wrapped_view