from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)

from database.models import AuditLog


audit = Blueprint(
    "audit",
    __name__
)


@audit.route("/audit")
def audit_logs():

    # ---------------------------------------------------------
    # Authentication check
    # ---------------------------------------------------------

    if (
        "user_id" not in session
        and
        "google_user" not in session
    ):

        return redirect(
            url_for(
                "authentication.login"
            )
        )


    # ---------------------------------------------------------
    # Owner-only access
    # ---------------------------------------------------------

    if session.get("role") != "OWNER":

        flash(
            "You do not have permission to access audit logs.",
            "danger"
        )

        return redirect(
            url_for(
                "dashboard.dashboard_home"
            )
        )


    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()


    page = request.args.get(
        "page",
        1,
        type=int
    )


    query = AuditLog.query


    if search:

        search_term = f"%{search}%"


        query = query.filter(

            AuditLog.user.ilike(
                search_term
            )

            |

            AuditLog.action.ilike(
                search_term
            )

            |

            AuditLog.details.ilike(
                search_term
            )

        )


    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------

    logs = query.order_by(

        AuditLog.timestamp.desc()

    ).paginate(

        page=page,

        per_page=15,

        error_out=False

    )


    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    total_logs = AuditLog.query.count()


    return render_template(

        "audit_logs.html",

        logs=logs,

        search=search,

        total_logs=total_logs

    )