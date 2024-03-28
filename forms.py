from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, TextAreaField

from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterUserForm(FlaskForm):
    """A form for adding a new user to the twitter clone."""

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=20, message="Too many characters")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=50, message="Too many characters"),
        ],
    )
    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(max=30, message="Too many characters")],
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(max=30, message="Too many characters")],
    )


class LoginUserForm(FlaskForm):
    """A form for logging in a user to the twitter clone."""

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=20, message="Too many characters")],
    )
    password = PasswordField("Password", validators=[DataRequired()])


class FeedbackForm(FlaskForm):
    """Feedback form for adding and editing"""

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=100, message="Too many characters")],
    )
    content = TextAreaField(
        "Text",
        validators=[DataRequired()],
    )
