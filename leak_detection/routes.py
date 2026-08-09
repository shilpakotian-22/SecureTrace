from flask import (

    Blueprint,

    render_template,

    request,

    flash

)

from leak_detection.services import detect_leak

from database.models import DetectionHistory

import os

leak_detection = Blueprint(

    "leak_detection",

    __name__

)


@leak_detection.route(

    "/detect",

    methods=["GET", "POST"]

)

def detect():

    if request.method == "POST":

        file = request.files["document"]

        upload_folder = "temp_detection"

        os.makedirs(

            upload_folder,

            exist_ok=True

        )

        filepath = os.path.join(

            upload_folder,

            file.filename

        )

        file.save(filepath)

        result = detect_leak(
            filepath
        )

        return render_template(

            "detect.html",

            result=result

        )

    return render_template(

        "detect.html"

    )

@leak_detection.route("/history")
def history():

    records = DetectionHistory.query.order_by(

        DetectionHistory.detected_at.desc()

    ).all()

    return render_template(

        "history.html",

        history=records

    )