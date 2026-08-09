from flask import (
    Blueprint,
    send_file,
    render_template,
    flash,
    redirect,
    url_for
)

import os

from database.models import DetectionHistory
from reports.pdf_generator import generate_report

reports = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports"
)

@reports.route("/")
def reports_home():

    detections = DetectionHistory.query.order_by(
        DetectionHistory.id.desc()
    ).all()

    return render_template(
        "reports.html",
        detections=detections
    )

@reports.route("/download/<int:id>")
def download_report(id):

    detection = DetectionHistory.query.get_or_404(id)

    report_folder = "generated_reports"

    os.makedirs(
        report_folder,
        exist_ok=True
    )

    filename = os.path.join(
        report_folder,
        f"Investigation_Report_{id}.pdf"
    )

    result = {

        "recipient": detection.detected_recipient,

        "recipient_email": "Not Available",

        "assignment_id": "-",

        "unicode": 0,

        "font": 0,

        "synonym": 0,

        "confidence": detection.confidence

    }

    generate_report(
        filename,
        result
    )

    return send_file(
        filename,
        as_attachment=True
    )