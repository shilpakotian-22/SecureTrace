import base64
import mimetypes
import os

from email.message import EmailMessage
from email.utils import parseaddr

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


class EmailSendError(Exception):
    """
    Controlled exception for email delivery failures.
    """

    pass


def get_token_path():
    """
    Return the absolute path to token.json.
    """

    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    return os.path.join(
        base_dir,
        "token.json"
    )


def get_service():
    """
    Create an authenticated Gmail API service.
    """

    token_path = get_token_path()

    if not os.path.isfile(token_path):

        raise EmailSendError(
            "Gmail authorization is not configured. "
            "Please authorize Gmail before sending documents."
        )

    try:

        creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES
        )

    except Exception as error:

        raise EmailSendError(
            "The Gmail authorization file could not be loaded."
        ) from error


    # ---------------------------------------------------------
    # Refresh expired credentials
    # ---------------------------------------------------------

    if creds.expired:

        if not creds.refresh_token:

            raise EmailSendError(
                "Gmail authorization has expired and cannot "
                "be refreshed. Please authorize Gmail again."
            )

        try:

            creds.refresh(
                Request()
            )

        except Exception as error:

            raise EmailSendError(
                "Gmail authorization could not be refreshed. "
                "Please authorize Gmail again."
            ) from error


        # Save refreshed credentials.

        try:

            with open(
                token_path,
                "w",
                encoding="utf-8"
            ) as token_file:

                token_file.write(
                    creds.to_json()
                )

        except OSError as error:

            # Sending can still potentially work even if
            # the refreshed token cannot be persisted.
            print(
                "Warning: refreshed Gmail credentials "
                "could not be saved."
            )

            print(
                f"Token save error: {error}"
            )


    if not creds.valid:

        raise EmailSendError(
            "Gmail authorization is invalid. "
            "Please authorize Gmail again."
        )


    try:

        return build(
            "gmail",
            "v1",
            credentials=creds,
            cache_discovery=False
        )

    except Exception as error:

        raise EmailSendError(
            "Unable to connect to the Gmail service."
        ) from error


def validate_email_address(email_address):
    """
    Perform basic recipient email validation.
    """

    if not email_address:

        raise EmailSendError(
            "Recipient email address is missing."
        )


    name, address = parseaddr(
        email_address
    )


    if (
        not address
        or
        "@" not in address
        or
        address.startswith("@")
        or
        address.endswith("@")
    ):

        raise EmailSendError(
            "The recipient email address is invalid."
        )


    return address


def send_email(
    recipient,
    subject,
    body,
    attachment_path
):
    """
    Send an email with an optional document attachment
    through the Gmail API.

    Returns:
        True on successful delivery.

    Raises:
        EmailSendError on controlled delivery failures.
    """

    # ---------------------------------------------------------
    # Validate recipient
    # ---------------------------------------------------------

    recipient = validate_email_address(
        recipient
    )


    # ---------------------------------------------------------
    # Validate subject/body
    # ---------------------------------------------------------

    if not subject:

        raise EmailSendError(
            "Email subject is missing."
        )


    if not body:

        raise EmailSendError(
            "Email body is missing."
        )


    # ---------------------------------------------------------
    # Validate attachment
    # ---------------------------------------------------------

    if not attachment_path:

        raise EmailSendError(
            "Email attachment is missing."
        )


    if not os.path.isfile(
        attachment_path
    ):

        raise EmailSendError(
            "The fingerprinted document could not be found."
        )


    # ---------------------------------------------------------
    # Build Gmail service
    # ---------------------------------------------------------

    service = get_service()


    # ---------------------------------------------------------
    # Build email
    # ---------------------------------------------------------

    message = EmailMessage()

    message["To"] = recipient

    message["Subject"] = subject

    message.set_content(
        body
    )


    # ---------------------------------------------------------
    # Add attachment
    # ---------------------------------------------------------

    mime_type, _ = mimetypes.guess_type(
        attachment_path
    )


    if mime_type:

        if "/" in mime_type:

            maintype, subtype = mime_type.split(
                "/",
                1
            )

        else:

            maintype = "application"
            subtype = "octet-stream"

    else:

        maintype = "application"
        subtype = "octet-stream"


    try:

        with open(
            attachment_path,
            "rb"
        ) as file:

            attachment_data = file.read()

    except OSError as error:

        raise EmailSendError(
            "The fingerprinted document could not be opened."
        ) from error


    message.add_attachment(

        attachment_data,

        maintype=maintype,

        subtype=subtype,

        filename=os.path.basename(
            attachment_path
        )

    )


    # ---------------------------------------------------------
    # Encode message
    # ---------------------------------------------------------

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode(
        "utf-8"
    )


    # ---------------------------------------------------------
    # Send through Gmail API
    # ---------------------------------------------------------

    try:

        service.users().messages().send(

            userId="me",

            body={
                "raw": raw_message
            }

        ).execute()

    except Exception as error:

        print(
            f"Gmail delivery error: {error}"
        )

        raise EmailSendError(
            "The email could not be delivered. "
            "Please verify Gmail authorization and try again."
        ) from error


    return True