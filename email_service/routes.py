from flask import (
    Blueprint,
    render_template,
    request
)

from database.models import EmailHistory
from database.db import db


email_service = Blueprint(
    "email_service",
    __name__,
    url_prefix="/email"
)


@email_service.route("/history")
def history():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()


    query = EmailHistory.query


    if search:

        search_term = f"%{search}%"

        query = query.filter(

            db.or_(

                EmailHistory.recipient.ilike(
                    search_term
                ),

                EmailHistory.subject.ilike(
                    search_term
                ),

                EmailHistory.status.ilike(
                    search_term
                )

            )

        )


    emails = query.order_by(

        EmailHistory.sent_at.desc()

    ).paginate(

        page=page,

        per_page=10,

        error_out=False

    )


    total = EmailHistory.query.count()

    sent = EmailHistory.query.filter_by(
        status="Sent"
    ).count()

    pending = EmailHistory.query.filter_by(
        status="Pending"
    ).count()

    failed = EmailHistory.query.filter_by(
        status="Failed"
    ).count()


    return render_template(

        "email_history.html",

        emails=emails,

        search=search,

        total=total,

        sent=sent,

        pending=pending,

        failed=failed

    )