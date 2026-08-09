from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for
)

from database.models import Recipient
from recipient.services import add_recipient
from audit.services import log_action

recipient = Blueprint(
    "recipient",
    __name__
)


@recipient.route("/recipients", methods=["GET", "POST"])
def recipients():

    if request.method == "POST":

        result = add_recipient(
            request.form["name"],
            request.form["email"],
            request.form["department"],
            request.form["organization"]
        )

        if result == "duplicate":

            flash("Email already exists.")

        else:

            flash("Recipient added successfully.")

        log_action(

            "System",

            "Added Recipient",

            request.form["email"]

        )    

        return redirect(
            url_for("recipient.recipients")
        )

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    query = Recipient.query

    if search:

        query = query.filter(

            (Recipient.name.ilike(f"%{search}%")) |

            (Recipient.email.ilike(f"%{search}%")) |

            (Recipient.department.ilike(f"%{search}%")) |

            (Recipient.organization.ilike(f"%{search}%"))

        )

    recipients = query.order_by(

        Recipient.id.desc()

    ).paginate(

        page=page,

        per_page=10,

        error_out=False

    )

    return render_template(
        "recipients.html",
        recipients=recipients,
        search=search
    )

@recipient.route("/recipients/edit/<int:id>", methods=["GET", "POST"])
def edit_recipient(id):

    recipient_data = Recipient.query.get_or_404(id)

    if request.method == "POST":

        recipient_data.name = request.form["name"]
        recipient_data.email = request.form["email"]
        recipient_data.department = request.form["department"]
        recipient_data.organization = request.form["organization"]

        from database.db import db

        db.session.commit()

        flash("Recipient updated successfully.")

        return redirect(
            url_for("recipient.recipients")
        )

    return render_template(
        "edit_recipient.html",
        recipient=recipient_data
    )

@recipient.route("/recipients/delete/<int:id>")
def delete_recipient(id):

    recipient = Recipient.query.get_or_404(id)

    from database.db import db

    db.session.delete(recipient)

    db.session.commit()

    flash("Recipient deleted successfully.")

    return redirect(
        url_for("recipient.recipients")
    )