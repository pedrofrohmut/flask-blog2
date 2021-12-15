"""Application routes."""
import os
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from flaskblog import mail


def size_down_image(form_image):
    """Size down images using pillow."""
    output_size = (125, 125)
    new_image = Image.open(form_image)
    new_image.thumbnail(output_size)
    return new_image


def save_image(form_image):
    """Save image."""
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_image.filename)
    image_file_name = random_hex + file_extension
    image_path = os.path.join(current_app.root_path, "static/profile_pics", image_file_name)
    sized_down_image = size_down_image(form_image)
    sized_down_image.save(image_path)
    return image_file_name


def send_password_reset_email(user):
    """."""
    token = user.get_reset_token()
    message = Message("Request Reset Password",
                      sender="noreply@demo.com",
                      recipients=[user.email])
    message.body = f"""
Flask Blog

To reset your password, visit the following link:
{url_for("users.reset_password", token=token, _external=True)}

If you did not make this request, simply ignore this e-mail an no changes will be made.
"""
    print(url_for("users.reset_password", token=token, _external=True))
    mail.send(message)
