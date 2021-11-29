"""Forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from flaskblog.models import User


class SignUpForm(FlaskForm):
    """Generates a form for sign up page."""

    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField("Confirm password",
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        """Validate if the username is already taken checking the database."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken")

    def validate_email(self, email):
        """Validate if the e-mail is already taken checking the database."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E-mail already taken")


class SignInForm(FlaskForm):
    """Generates a form for sign in page."""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=2, max=20)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")
