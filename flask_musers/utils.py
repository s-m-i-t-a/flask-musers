# -*- coding: utf-8 -*-

from blinker import signal

from flask_musers.models import User


def prepare_reset_password_for(email):
    user = User.get_by_email(email)

    reset_password = signal('musers-reset-password-token-created')
    reset_password.send(
        user,
        data={
            'token': create_token_for(user, expires=3600),
        }
    )


def create_token_for(user, expires):
    pass
