# -*- coding: utf-8 -*-

'''
from flask import Flask
from flask.ext.musers import MUsers

app = Flask(__name__)
MUsers(app)
.
.
.
'''


from flask.ext.login import LoginManager
from .models import User


__version__ = '0.5.2'


class MUsers(object):
    def __init__(self, app=None):
        self.login_manager = LoginManager()
        self.login_manager.user_loader(self.load_user)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.login_manager.init_app(app)

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['musers'] = self
        self.app = app

    def load_user(self, userid):
        return User.get_active_user_by_pk_or_none(userid)
