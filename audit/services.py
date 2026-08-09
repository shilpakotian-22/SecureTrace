from database.db import db
from database.models import AuditLog


def log_action(
    user,
    action,
    details=""
):
    """
    Create an audit log entry.

    Parameters:
        user: User name/email responsible for the action.
        action: Short description of the action.
        details: Optional additional information.

    Returns:
        AuditLog object on success.
        None if the audit record could not be saved.
    """

    try:

        log = AuditLog(
            user=user,
            action=action,
            details=details
        )

        db.session.add(log)

        db.session.commit()

        return log

    except Exception as error:

        db.session.rollback()

        print(
            "Audit logging error:"
        )

        print(
            error
        )

        return None