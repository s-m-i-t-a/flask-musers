import pytest
import six

if six.PY3:
    from unittest.mock import patch, call
else:
    from mock import patch, call

from flask import request

from flask_musers.models import UserError
from flask_musers.forms import LoginForm


class TestLoginForm(object):
    @pytest.fixture
    def data(self, request):
        data = {
            'email': 'franta@vonasek.cz',
            'password': 'vonasek123',
        }
        return data

    @patch('flask_musers.forms.User.get_user')
    def test_get_user(self, mock_get_user, data, app):
        with app.test_request_context('/login', method='POST', data=data):
            form = LoginForm(formdata=request.form)
            form.validate_on_submit()
            form.get_user()

        assert mock_get_user.called

        kall = call(email=data['email'], password=data['password'])
        assert mock_get_user.call_args == kall

    @patch('flask_musers.forms.User.get_user')
    def test_get_user_raise_error_with_bad_data(self, mock_get_user, data, app):
        mock_get_user.side_effect = UserError

        with app.test_request_context('/login', method='POST', data=data):
            form = LoginForm(formdata=request.form)
            form.validate_on_submit()
            with pytest.raises(UserError):
                form.get_user()

    @patch('flask_musers.forms.User.get_user')
    def test_get_user_return_user(self, mock_get_user, data, app):
        with app.test_request_context('/login', method='POST', data=data):
            form = LoginForm(formdata=request.form)
            form.validate_on_submit()
            user = form.get_user()

        assert user == mock_get_user.return_value
