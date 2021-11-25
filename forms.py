"""Forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


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


class SignInForm(FlaskForm):
    """Generates a form for sign in page."""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=2, max=20)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")
