# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import PasswordField, TextField, validators

from .models import User


class RegisterForm(Form):
    email = TextField('Email', [validators.Required(), validators.Email(message='Enter a valid e-mail address.')])
    password = PasswordField('New Password', [validators.Required(),
                                              validators.Length(min=8, message='Password must be at least 8 characters long.'),
                                              validators.EqualTo('password_again', message='Passwords is not equal!')])
    password_again = PasswordField('Password again', [validators.Required()])
    name = TextField('Name', [validators.Optional()])

    def register_user(self):
        return User.register(email=self.email.data, password=self.password.data, activated=True, name=self.name.data)


class LoginForm(Form):
    email = TextField('Email', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.Required()])

    def get_user(self):
        return User.get_user(email=self.email.data, password=self.password.data)
