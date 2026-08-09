from email_service.gmail_sender import (
    send_email,
    EmailSendError
)

from database.models import AppSettings


def send_generated_document(document):
    """
    Send a generated fingerprinted document
    to its assigned recipient.
    """

    if document is None:

        raise EmailSendError(
            "Generated document was not found."
        )


    if not document.recipient_email:

        raise EmailSendError(
            "Recipient email address is missing."
        )


    if not document.generated_file:

        raise EmailSendError(
            "Generated document file is missing."
        )


    # ---------------------------------------------------------
    # Application branding
    # ---------------------------------------------------------

    settings = AppSettings.query.first()


    if settings:

        application_name = (
            settings.application_name
            or
            "SecureTrace"
        )

        organization = (
            settings.organization
            or
            application_name
        )

    else:

        application_name = "SecureTrace"

        organization = "SecureTrace"


    subject = (
        f"{application_name} "
        f"Fingerprint-Protected Document"
    )


    body = f"""
Hello {document.recipient},

Please find your assigned fingerprinted document attached.

This document was generated and distributed through
{application_name}.

Organization:
{organization}

Regards,
{application_name}
"""


    return send_email(

        document.recipient_email,

        subject,

        body.strip(),

        document.generated_file

    )