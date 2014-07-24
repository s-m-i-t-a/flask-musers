import six
import pytest

if six.PY3:
    import http.client as httplib
    from unittest.mock import patch, call
else:
    import httplib
    from mock import patch, call

from flask_musers.models import UserError
from flask_musers.views import login, LOGIN_SUCCESS, LOGIN_ERROR


LOGIN_URL = '/login'


class TestLoginView(object):
    @pytest.fixture
    def data(self, request):
        data = {
            'email': 'franta@vonasek.cz',
            'password': 'vonasek123',
        }
        return data

    def test_login_url_resolves_to_login_view(self, app):
        urls = app.url_map.bind('localhost').match(LOGIN_URL)
        view = urls[0]
        f = app.view_functions[view]

        assert f is login

    def test_GET_request_return_status_ok(self, client):
        response = client.get(LOGIN_URL)

        assert response.status_code == httplib.OK

    def test_POST_method_is_allowed(self, client):
        response = client.post(LOGIN_URL, data={})

        assert response.status_code != httplib.METHOD_NOT_ALLOWED

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.request')
    @patch('flask_musers.views.login_user')
    def test_pass_POST_data_to_form(self, mock_login_user, mock_request, MockLoginForm, client, data):

        client.post(
            LOGIN_URL,
            data=data
        )

        assert MockLoginForm.call_args == call(formdata=mock_request.form)

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    def test_get_user_when_form_is_valid(self, mock_login_user, MockLoginForm, client, data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True

        client.post(
            LOGIN_URL,
            data=data
        )

        assert mock_form.get_user.called

    @patch('flask_musers.views.LoginForm')
    def test_get_user_when_form_is_not_valid(self, MockLoginForm, client, data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = False

        client.post(
            LOGIN_URL,
            data=data
        )

        assert not mock_form.get_user.called

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    def test_login_user_when_email_and_password_match(self, mock_login_user, MockLoginForm, client, data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True
        mock_user = mock_form.get_user.return_value

        client.post(
            LOGIN_URL,
            data=data
        )

        assert mock_login_user.called

        kall = call(mock_user)
        assert mock_login_user.call_args == kall

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    @patch('flask_musers.views.redirect')
    def test_redirect_to_next_when_user_is_logged(self,
                                                  mock_redirect,
                                                  mock_login_user,
                                                  MockLoginForm,
                                                  client,
                                                  data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True
        mock_redirect.return_value = ''

        client.post(
            '{0}?next=/dashboard'.format(LOGIN_URL),
            data=data
        )

        assert mock_redirect.called

        kall = call('/dashboard')
        assert mock_redirect.call_args == kall

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    @patch('flask_musers.views.redirect')
    def test_redirect_to_index_when_user_is_logged(self,
                                                   mock_redirect,
                                                   mock_login_user,
                                                   MockLoginForm,
                                                   client,
                                                   data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True
        mock_redirect.return_value = ''

        client.post(
            LOGIN_URL,
            data=data
        )

        assert mock_redirect.called

        kall = call('/')
        assert mock_redirect.call_args == kall

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    @patch('flask_musers.views.flash')
    def test_flash_message_when_successfull_login(self,
                                                  mock_flash,
                                                  mock_login_user,
                                                  MockLoginForm,
                                                  client,
                                                  data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True

        client.post(
            LOGIN_URL,
            data=data
        )

        assert mock_flash.called

        kall = call(**LOGIN_SUCCESS)
        assert mock_flash.call_args == kall

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    @patch('flask_musers.views.flash')
    def test_flash_error_message_when_bad_user_try_login(self,
                                                         mock_flash,
                                                         mock_login_user,
                                                         MockLoginForm,
                                                         client,
                                                         data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True
        mock_form.get_user.side_effect = UserError

        client.post(
            LOGIN_URL,
            data=data
        )

        assert mock_flash.called

        kall = call(**LOGIN_ERROR)
        assert mock_flash.call_args == kall

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.render_template')
    def test_GET_request_render_template(self,
                                         mock_render_template,
                                         MockLoginForm,
                                         client):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = False
        mock_render_template.return_value = six.b('')

        response = client.get(LOGIN_URL)

        assert mock_render_template.called

        assert response.data == mock_render_template.return_value

        kall = call('musers/login.html', form=mock_form)
        assert mock_render_template.call_args == kall

    @patch('flask_musers.views.LoginForm')
    @patch('flask_musers.views.login_user')
    @patch('flask_musers.views.render_template')
    def test_render_template_when_bad_user_try_login(self,
                                                     mock_render_template,
                                                     mock_login_user,
                                                     MockLoginForm,
                                                     client,
                                                     data):
        mock_form = MockLoginForm.return_value
        mock_form.validate_on_submit.return_value = True
        mock_form.get_user.side_effect = UserError
        mock_render_template.return_value = six.b('')

        response = client.post(LOGIN_URL, data=data)

        assert mock_render_template.called

        assert response.data == mock_render_template.return_value

        kall = call('musers/login.html', form=mock_form)
        assert mock_render_template.call_args == kall
