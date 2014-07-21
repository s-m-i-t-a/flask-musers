# -*- coding: utf-8 -*-

'''
In the app you must init the *LoginManager*.

from flask import Flask
from flask_musers import login_manager

app = Flask(__name__)
login_manager.init_app(app)
.
.
.
'''

from flask.ext.login import LoginManager

from .models import User


__version__ = '0.0.3'


login_manager = LoginManager()
# login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        user = User.active.get(pk=userid)
    except User.DoesNotExist:
        user = None

    return user
