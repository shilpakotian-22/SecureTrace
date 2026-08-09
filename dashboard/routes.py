from flask import (
    Blueprint,
    render_template,
    session
)

from database.models import (
    Document,
    Recipient,
    Assignment,
    GeneratedDocument,
    DetectionHistory,
    EmailHistory
)

from sqlalchemy import extract

from authentication.models import User

from auth_utils import login_required


dashboard = Blueprint(
    "dashboard",
    __name__
)


@dashboard.route("/")
def home():

    return render_template(
        "home.html"
    )


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    # ---------------------------------------------------------
    # OWNER DASHBOARD
    # ---------------------------------------------------------

    if session.get("role") == "OWNER":

        stats = {

            "documents": Document.query.count(),

            "recipients": Recipient.query.count(),

            "assignments": Assignment.query.count(),

            "generated": GeneratedDocument.query.count(),

            "detections": DetectionHistory.query.count(),

            "users": User.query.count(),

            "emails_sent": EmailHistory.query.filter_by(
                status="Sent"
            ).count(),

            "pending_emails": EmailHistory.query.filter_by(
                status="Pending"
            ).count(),

            "failed_emails": EmailHistory.query.filter_by(
                status="Failed"
            ).count()

        }


        # -----------------------------------------------------
        # Recent documents
        # -----------------------------------------------------

        recent_documents = Document.query.order_by(

            Document.uploaded_at.desc()

        ).limit(5).all()


        # -----------------------------------------------------
        # Recent detections
        # -----------------------------------------------------

        recent_detections = DetectionHistory.query.order_by(

            DetectionHistory.detected_at.desc()

        ).limit(5).all()


        # -----------------------------------------------------
        # Monthly upload statistics
        # -----------------------------------------------------

        monthly_uploads = []

        month_labels = [

            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"

        ]


        for month in range(1, 13):

            count = Document.query.filter(

                extract(
                    "month",
                    Document.uploaded_at
                ) == month

            ).count()


            monthly_uploads.append(
                count
            )


        return render_template(

            "owner_dashboard.html",

            stats=stats,

            recent_documents=recent_documents,

            recent_detections=recent_detections,

            month_labels=month_labels,

            monthly_uploads=monthly_uploads

        )


    # ---------------------------------------------------------
    # VERIFIER DASHBOARD
    # ---------------------------------------------------------

    return render_template(
        "verifier_dashboard.html"
    )