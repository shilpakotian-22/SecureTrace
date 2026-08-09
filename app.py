from flask import Flask, send_from_directory
import os
import bcrypt

from authentication.models import User
from authentication.routes import authentication

from dashboard.routes import dashboard

from database.db import db
from database.models import (
    Document,
    Recipient,
    Assignment,
    AppSettings
)

from fingerprint.routes import fingerprint
from recipient.routes import recipient
from assignment.routes import assignment
from leak_detection import leak_detection

from authentication.google_auth.oauth import init_oauth
from authentication.google_auth.routes import google_auth

from email_service.routes import email_service
from reports.routes import reports
from audit.routes import audit
from settings.routes import settings
from errors.routes import errors
from werkzeug.exceptions import RequestEntityTooLarge
from flask import flash, redirect, request


def hash_password(password):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    init_oauth(app)

    db.init_app(app)

    with app.app_context():

        db.create_all()

    # Register Blueprints
    app.register_blueprint(authentication)
    app.register_blueprint(google_auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(fingerprint)
    app.register_blueprint(recipient)
    app.register_blueprint(assignment)
    app.register_blueprint(leak_detection)
    app.register_blueprint(email_service)
    app.register_blueprint(reports)
    app.register_blueprint(audit)
    app.register_blueprint(settings)
    app.register_blueprint(errors)

    return app


app = create_app()


@app.context_processor
def inject_settings():

    settings = AppSettings.query.first()

    if settings is None:

        settings = AppSettings()

        db.session.add(settings)
        db.session.commit()

    return dict(
        app_settings=settings
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    upload_folder = os.path.join(
        BASE_DIR,
        "uploads"
    )

    return send_from_directory(
        upload_folder,
        filename,
        as_attachment=True
    )

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(error):

    flash(
        "The uploaded file exceeds the maximum allowed size.",
        "danger"
    )

    return redirect(request.referrer or "/upload")

if __name__ == "__main__":

    app.run(debug=True)