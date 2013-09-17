# -*- coding: utf-8 -*-

from mongoengine.document import NotUniqueError

from flask import flash, redirect
from flask.views import MethodView

from flask.ext.login import login_user, logout_user, login_required

from flask_cbv.views.generic import FormView
from .forms import RegisterForm, LoginForm
from .models import User


class RegisterView(FormView):
    template = 'auth/register.html'
    form_class = RegisterForm
    success_url = '/login/'  # FIXME: pouzit url_for

    def form_valid(self, form, *args, **kwargs):
        user = User()
        user.email = form.email.data
        user.last_name = form.last_name.data
        user.first_name = form.first_name.data
        user.set_password(form.password.data)
        user.activated = True  # TODO: Aktivovat az po obdrzenim mailu s linkem???
        try:
            user.save()
        except NotUniqueError:
            flash('Correct your registration data and please try again.', 'error')
            return self.form_invalid(form, *args, **kwargs)

        flash('Thank you, your registration is successfully done.', 'success')

        return super(RegisterView, self).form_valid(form, *args, **kwargs)


class LoginView(FormView):
    template = 'auth/login.html'
    form_class = LoginForm
    success_url = '/dashboard/'

    def form_valid(self, form, *args, **kwargs):
        try:
            user = User.objects.get(email=form.email.data)
        except User.DoesNotExist:
            user = None

        if user is None or not user.check_password(form.password.data):
            flash('Your username and password didn\'t match. Please try again.', 'error')
            return self.form_invalid(form, *args, **kwargs)

        login_user(user)
        flash("Logged in successfully.", 'success')

        return super(LoginView, self).form_valid(form, *args, **kwargs)


class LogoutView(MethodView):
    redirect = '/login/'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        logout_user()
        flash("Logged out successfully.", 'success')
        return redirect(self.redirect)
