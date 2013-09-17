# -*- coding: utf-8 -*-

from flask import Blueprint

from .views import RegisterView, LoginView, LogoutView


auth = Blueprint('auth', __name__, template_folder='templates')


auth.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
auth.add_url_rule('/login/', view_func=LoginView.as_view('login'))
auth.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
