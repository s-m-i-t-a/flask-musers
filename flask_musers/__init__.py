# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager

from app import app
from .models import User


login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        user = User.active.get(pk=userid)
    except User.DoesNotExist:
        user = None

    return user
