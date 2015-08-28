import six

from mock import patch, call

from flask import request

from flask_musers.forms import RegisterForm


class TestRegisterForm(object):
    @patch('flask_musers.forms.User.register')
    def test_register_user_create_user(self, mock_register, app):
        data = {
            'email': 'franta@vonasek.cz',
            'password': 'vonasek123',
            'password_again': 'vonasek123',
        }

        with app.test_request_context('/register', method='POST', data=data):
            form = RegisterForm(formdata=request.form)
            form.validate_on_submit()
            form.register_user()

        assert mock_register.called

        kall = call(email=data['email'], password=data['password'], activated=True, name='')
        assert mock_register.call_args == kall

    @patch('flask_musers.forms.User.register')
    def test_register_user_return_new_user(self, mock_register, app):
        data = {
            'email': 'franta@vonasek.cz',
            'password': 'vonasek123',
            'password_again': 'vonasek123',
        }

        with app.test_request_context('/register', method='POST', data=data):
            form = RegisterForm(formdata=request.form)
            form.validate_on_submit()
            user = form.register_user()

        assert user == mock_register.return_value
