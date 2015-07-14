# -*- coding: utf-8 -*-

from blinker import signal
from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer

from flask_musers.models import User


def prepare_reset_password_for(email):
    user = User.get_by_email(email)

    reset_password = signal('musers-reset-password-token-created')
    reset_password.send(
        user,
        data={
            'token': create_token_for(user, _signer()),
        }
    )


def create_token_for(user, signer):
    return signer.dumps({
        'email': user.email,
    })


def reset_password(token, password):
    user = User.get_by_email(get_email_from_token(token, _signer()))
    user.set_password(password)
    user.save()


def get_email_from_token(token, signer, max_age=3600):
    return signer.loads(token, max_age=max_age)['email']


def _signer():
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])
