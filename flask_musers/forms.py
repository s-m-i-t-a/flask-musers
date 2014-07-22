# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import PasswordField, TextField, validators


class RegisterForm(Form):
    email = TextField('Email', [validators.Required(), validators.Email(message='Enter a valid e-mail address.')])
    password = PasswordField('New Password', [validators.Required(),
                                              validators.Length(min=8, message='Password must be at least 8 characters long.'),
                                              validators.EqualTo('password_again', message='Passwords is not equal!')])
    password_again = PasswordField('Password again', [validators.Required()])
    first_name = TextField('First name', [validators.Optional()])
    last_name = TextField('Last name', [validators.Optional()])


class LoginForm(Form):
    email = TextField('Email', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.Required()])
