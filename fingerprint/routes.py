from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for
)

from fingerprint.services import save_uploaded_document

from database.models import Document

from database.db import db

from audit.services import log_action

from auth_utils import owner_required

import os


fingerprint = Blueprint(
    "fingerprint",
    __name__
)


@fingerprint.route(
    "/upload",
    methods=["GET", "POST"]
)
@owner_required
def upload_document():

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()


    # ---------------------------------------------------------
    # Upload document
    # ---------------------------------------------------------

    if request.method == "POST":

        file = request.files.get(
            "document"
        )


        if not file or not file.filename:

            flash(
                "Please select a document to upload.",
                "warning"
            )

        else:

            document = save_uploaded_document(

                file,

                session["full_name"]

            )


            # -------------------------------------------------
            # Invalid document
            # -------------------------------------------------

            if document == "invalid":

                flash(

                    "Only DOCX and PDF files are allowed.",

                    "danger"

                )


                log_action(

                    session["full_name"],

                    "Failed Document Upload",

                    f"Invalid file: {file.filename}"

                )


            # -------------------------------------------------
            # Successful upload
            # -------------------------------------------------

            else:

                flash(

                    "Document uploaded successfully.",

                    "success"

                )


                log_action(

                    session["full_name"],

                    "Uploaded Document",

                    document.filename

                )


    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------

    page = request.args.get(
        "page",
        1,
        type=int
    )


    query = Document.query


    # ---------------------------------------------------------
    # Filename search
    # ---------------------------------------------------------

    if search:

        query = query.filter(

            Document.filename.ilike(
                f"%{search}%"
            )

        )


    # ---------------------------------------------------------
    # Latest documents first
    # ---------------------------------------------------------

    documents = query.order_by(

        Document.uploaded_at.desc()

    ).paginate(

        page=page,

        per_page=10,

        error_out=False

    )


    return render_template(

        "upload.html",

        documents=documents,

        search=search

    )


@fingerprint.route(
    "/delete/<int:id>"
)
@owner_required
def delete_document(id):

    # ---------------------------------------------------------
    # Find document
    # ---------------------------------------------------------

    document = Document.query.get_or_404(
        id
    )


    filename = document.filename


    # ---------------------------------------------------------
    # Delete physical file
    # ---------------------------------------------------------

    if os.path.exists(
        document.filepath
    ):

        os.remove(
            document.filepath
        )


    # ---------------------------------------------------------
    # Delete database record
    # ---------------------------------------------------------

    db.session.delete(
        document
    )

    db.session.commit()


    # ---------------------------------------------------------
    # Audit
    # ---------------------------------------------------------

    log_action(

        session["full_name"],

        "Deleted Document",

        filename

    )


    flash(

        "Document deleted successfully.",

        "success"

    )


    return redirect(

        url_for(
            "fingerprint.upload_document"
        )

    )