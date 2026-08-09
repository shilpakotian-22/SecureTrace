from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
    send_file
)

import os

from database.models import (
    Document,
    Recipient,
    Assignment,
    GeneratedDocument,
    EmailHistory
)

from assignment.services import assign_document
from assignment.generator import generate_document
from email_service.services import send_generated_document
from database.db import db
from audit.services import log_action


assignment = Blueprint(
    "assignment",
    __name__
)


def user_is_authenticated():

    return (
        "user_id" in session
        or
        "google_user" in session
    )


@assignment.route(
    "/assignments",
    methods=["GET", "POST"]
)
def assignments():

    if not user_is_authenticated():

        return redirect(
            url_for("authentication.login")
        )

    if request.method == "POST":

        document_id = request.form.get("document")
        recipient_id = request.form.get("recipient")

        if not document_id or not recipient_id:

            flash(
                "Please select both a document and a recipient.",
                "warning"
            )

            return redirect(
                url_for("assignment.assignments")
            )

        result = assign_document(
            document_id,
            recipient_id
        )

        if result == "duplicate":

            flash(
                "This document is already assigned to this recipient.",
                "warning"
            )

        elif result == "document_not_found":

            flash(
                "The selected document could not be found.",
                "danger"
            )

        elif result == "recipient_not_found":

            flash(
                "The selected recipient could not be found.",
                "danger"
            )

        elif result == "error":

            flash(
                "Unable to create the assignment. "
                "Please try again.",
                "danger"
            )

        else:

            flash(
                "Assignment created successfully.",
                "success"
            )


        return redirect(
            url_for("assignment.assignments")
        )

    documents = Document.query.order_by(
        Document.uploaded_at.desc()
    ).all()

    recipients = Recipient.query.order_by(
        Recipient.name.asc()
    ).all()

    assignments = Assignment.query.order_by(
        Assignment.assigned_at.desc()
    ).all()

    generated_documents = GeneratedDocument.query.order_by(
        GeneratedDocument.generated_at.desc()
    ).all()

    return render_template(
        "assignments.html",
        documents=documents,
        recipients=recipients,
        assignments=assignments,
        generated_documents=generated_documents
    )


@assignment.route(
    "/generate",
    methods=["POST"]
)
def generate_fingerprints():

    if not user_is_authenticated():

        return redirect(
            url_for("authentication.login")
        )

    assignments = Assignment.query.order_by(
        Assignment.assigned_at.asc()
    ).all()

    generated = 0
    skipped = 0
    failed = 0

    for assignment_record in assignments:

        existing_document = GeneratedDocument.query.filter_by(
            assignment_id=assignment_record.id
        ).first()

        if existing_document:

            skipped += 1

            continue

        try:

            result = generate_document(
                assignment_record
            )

            if result is not None:

                generated += 1

            else:

                failed += 1

        except Exception:

            failed += 1

    if generated > 0:

        flash(
            f"{generated} fingerprinted document(s) "
            "generated successfully.",
            "success"
        )

    if skipped > 0:

        flash(
            f"{skipped} assignment(s) already have "
            "fingerprinted documents and were skipped.",
            "info"
        )

    if failed > 0:

        flash(
            f"{failed} assignment(s) could not be processed.",
            "danger"
        )

    if session.get("full_name"):

        log_action(
            session["full_name"],
            "Generated Fingerprinted Documents",
            f"Generated: {generated}, "
            f"Skipped: {skipped}, "
            f"Failed: {failed}"
        )

    return redirect(
        url_for("assignment.assignments")
    )


@assignment.route("/generated")
def generated_documents():

    if not user_is_authenticated():

        return redirect(
            url_for("authentication.login")
        )

    documents = GeneratedDocument.query.order_by(
        GeneratedDocument.generated_at.desc()
    ).all()

    return render_template(
        "generated_documents.html",
        documents=documents
    )


@assignment.route(
    "/generated/download/<int:id>"
)
def download_generated(id):

    if not user_is_authenticated():

        return redirect(
            url_for("authentication.login")
        )

    document = GeneratedDocument.query.get_or_404(id)

    if not document.generated_file:

        flash(
            "The generated document path is unavailable.",
            "danger"
        )

        return redirect(
            url_for("assignment.generated_documents")
        )

    if not os.path.isfile(document.generated_file):

        flash(
            "The generated document could not be found on the server.",
            "danger"
        )

        return redirect(
            url_for("assignment.generated_documents")
        )

    return send_file(
        document.generated_file,
        as_attachment=True
    )


@assignment.route(
    "/send/<int:id>",
    methods=["POST"]
)
def send_document(id):

    document = GeneratedDocument.query.get_or_404(
        id
    )

    try:

        # -----------------------------------------------------
        # Mark as pending while delivery is being attempted
        # -----------------------------------------------------

        document.email_status = "Pending"

        db.session.commit()


        # -----------------------------------------------------
        # Send document
        # -----------------------------------------------------

        send_generated_document(
            document
        )


        # -----------------------------------------------------
        # Record successful email
        # -----------------------------------------------------

        history = EmailHistory(

            sender=session.get(
                "email",
                "System"
            ),

            recipient=document.recipient_email,

            subject=(
                "Fingerprint-Protected Document"
            ),

            attachment=document.generated_file,

            status="Sent"

        )


        db.session.add(
            history
        )


        document.email_status = "Sent"


        db.session.commit()


        # -----------------------------------------------------
        # Audit
        # -----------------------------------------------------

        try:

            log_action(

                session.get(
                    "full_name",
                    "System"
                ),

                "Sent Fingerprinted Document",

                document.recipient_email

            )

        except Exception as audit_error:

            print(
                "Warning: email sent successfully, "
                "but audit logging failed:"
            )

            print(
                audit_error
            )


        flash(
            "Fingerprint-protected document "
            "sent successfully.",
            "success"
        )


    except Exception as error:

        # -----------------------------------------------------
        # Mark generated document as failed
        # -----------------------------------------------------

        document.email_status = "Failed"


        # -----------------------------------------------------
        # Record failed attempt
        # -----------------------------------------------------

        try:

            history = EmailHistory(

                sender=session.get(
                    "email",
                    "System"
                ),

                recipient=document.recipient_email,

                subject=(
                    "Fingerprint-Protected Document"
                ),

                attachment=document.generated_file,

                status="Failed"

            )

            db.session.add(
                history
            )

            db.session.commit()

        except Exception as history_error:

            db.session.rollback()

            print(
                "Warning: could not record "
                "failed email history:"
            )

            print(
                history_error
            )


        # -----------------------------------------------------
        # Audit failed delivery
        # -----------------------------------------------------

        try:

            log_action(

                session.get(
                    "full_name",
                    "System"
                ),

                "Failed Fingerprinted Document Email",

                document.recipient_email

            )

        except Exception as audit_error:

            print(
                "Warning: failed email audit logging:"
            )

            print(
                audit_error
            )


        flash(
            "The document could not be sent. "
            "Please verify Gmail authorization "
            "and try again.",
            "danger"
        )


    return redirect(
        url_for(
            "assignment.generated_documents"
        )
    )