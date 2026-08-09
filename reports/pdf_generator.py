from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def generate_report(filename, result):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b><font size=18>SecureTrace</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Leak Investigation Report",
            styles["Heading2"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            f"<b>Recipient:</b> {result['recipient']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Email:</b> {result['recipient_email']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Assignment ID:</b> {result['assignment_id']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Unicode Layer:</b> {result['unicode']}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Font Layer:</b> {result['font']}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Synonym Layer:</b> {result['synonym']}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Confidence:</b> {result['confidence']}%",
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "<b>Investigation Result</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"The leaked document has been attributed to <b>{result['recipient']}</b>.",
            styles["BodyText"]
        )
    )

    pdf.build(story)