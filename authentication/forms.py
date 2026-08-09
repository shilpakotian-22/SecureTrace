from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email
)


class LoginForm(FlaskForm):

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    role = SelectField(
        "Role",
        choices=[
            ("OWNER", "Owner"),
            ("VERIFIER", "Verifier")
        ]
    )

    submit = SubmitField(
        "Login"
    )