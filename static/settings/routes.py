from flask import (
    Blueprint,
    render_template,
    request,
    flash
)

from database.db import db
from database.models import AppSettings

settings = Blueprint(
    "settings",
    __name__
)


@settings.route("/settings", methods=["GET", "POST"])
def application_settings():

    app_settings = AppSettings.query.first()

    if not app_settings:

        app_settings = AppSettings()

        db.session.add(app_settings)

        db.session.commit()

    if request.method == "POST":

        app_settings.organization = request.form["organization"]

        app_settings.application_name = request.form["application_name"]

        app_settings.default_sender = request.form["default_sender"]

        app_settings.timezone = request.form["timezone"]

        app_settings.max_upload_size = int(
            request.form["max_upload_size"]
        )

        db.session.commit()

        flash("Settings updated successfully.")

    return render_template(

        "settings.html",

        settings=app_settings

    )