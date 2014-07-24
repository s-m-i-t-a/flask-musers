# -*- coding: utf-8 -*-

from mongoengine.document import NotUniqueError

from flask import flash, redirect, Blueprint, request, url_for, render_template

from flask.ext.login import login_user, logout_user, login_required

from .forms import RegisterForm, LoginForm
from .models import UserError


musers = Blueprint('musers', __name__)


REGISTRATION_SUCCESS = 'Thank you, your registration is successfully done.'
REGISTRATION_ERROR = 'Correct your registration data and please try again.'

LOGIN_SUCCESS = {
    'message': 'Logged in successfully.',
    'category': 'success',
}

LOGIN_ERROR = {
    'message': 'Your username and password didn\'t match. Please try again.',
    'category': 'error',
}

LOGOUT_SUCCESS = {
    'message': 'Logged out successfully.',
    'category': 'success',
}


@musers.route('/register', endpoint='register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(formdata=request.form)
    if form.validate_on_submit():
        try:
            form.register_user()
            flash(REGISTRATION_SUCCESS, 'success')
            return redirect(url_for('musers.login'))
        except NotUniqueError:
            flash(REGISTRATION_ERROR, 'error')
    return render_template('musers/register.html', form=form)


@musers.route('/login', endpoint='login', methods=['GET', 'POST'])
def login():
    form = LoginForm(formdata=request.form)
    if form.validate_on_submit():
        try:
            user = form.get_user()
            login_user(user)
            flash(**LOGIN_SUCCESS)
            next_url = request.args.get('next', '/')
            return redirect(next_url)
        except UserError:
            flash(**LOGIN_ERROR)

    return render_template('musers/login.html', form=form)


@musers.route('/logout', endpoint='logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(**LOGOUT_SUCCESS)
    return redirect('/')


# class LogoutView(MethodView):
#     redirect = '/login/'
#     decorators = [login_required]

#     def get(self, *args, **kwargs):
#         logout_user()
#         flash("Logged out successfully.", 'success')
#         return redirect(self.redirect)
