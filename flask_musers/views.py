# -*- coding: utf-8 -*-

from mongoengine.document import NotUniqueError

from flask import flash, redirect, Blueprint, request, url_for, render_template

from flask.ext.login import login_user, logout_user, login_required

from .forms import RegisterForm, LoginForm


musers = Blueprint('musers', __name__)


REGISTRATION_SUCCESS = 'Thank you, your registration is successfully done.'
REGISTRATION_ERROR = 'Correct your registration data and please try again.'


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


@musers.route('/login', endpoint='login', methods=['GET'])
def login():
    pass


# class RegisterView(FormView):
#     template = 'auth/register.html'
#     form_class = RegisterForm
#     success_url = '/login/'  # FIXME: pouzit url_for

#     def form_valid(self, form, *args, **kwargs):
#         user = User()
#         user.email = form.email.data
#         user.last_name = form.last_name.data
#         user.first_name = form.first_name.data
#         user.set_password(form.password.data)
#         user.activated = True  # TODO: Aktivovat az po obdrzenim mailu s linkem???
#         try:
#             user.save()
#         except NotUniqueError:
#             flash('Correct your registration data and please try again.', 'error')
#             return self.form_invalid(form, *args, **kwargs)

#         flash('Thank you, your registration is successfully done.', 'success')

#         return super(RegisterView, self).form_valid(form, *args, **kwargs)


# class LoginView(FormView):
#     template = 'auth/login.html'
#     form_class = LoginForm
#     success_url = '/dashboard/'

#     def form_valid(self, form, *args, **kwargs):
#         try:
#             user = User.objects.get(email=form.email.data)
#         except User.DoesNotExist:
#             user = None

#         if user is None or not user.check_password(form.password.data):
#             flash('Your username and password didn\'t match. Please try again.', 'error')
#             return self.form_invalid(form, *args, **kwargs)

#         login_user(user)
#         flash("Logged in successfully.", 'success')

#         return super(LoginView, self).form_valid(form, *args, **kwargs)


# class LogoutView(MethodView):
#     redirect = '/login/'
#     decorators = [login_required]

#     def get(self, *args, **kwargs):
#         logout_user()
#         flash("Logged out successfully.", 'success')
#         return redirect(self.redirect)
