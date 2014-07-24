import six
import pytest

if six.PY3:
    import http.client as httplib
    from unittest.mock import patch, call
else:
    import httplib
    from mock import patch, call

from mongoengine.document import NotUniqueError

from flask_musers.views import register, REGISTRATION_SUCCESS, REGISTRATION_ERROR


REGISTER_URL = '/register'


class TestRegisterView(object):
    @pytest.fixture
    def data(self, request):
        data = {
            'email': 'franta@vonasek.cz',
            'password': 'vonasek123',
            'password_again': 'vonasek123',
        }
        return data

    def test_register_url_resolves_to_register_view(self, app):
        urls = app.url_map.bind('localhost').match(REGISTER_URL)
        view = urls[0]
        f = app.view_functions[view]

        assert f is register

    def test_GET_request_return_status_ok(self, client):
        response = client.get(REGISTER_URL)

        assert response.status_code == httplib.OK

    def test_POST_method_is_allowed(self, client):
        response = client.post(REGISTER_URL, data={})

        assert response.status_code != httplib.METHOD_NOT_ALLOWED

    @patch('flask_musers.views.RegisterForm')
    @patch('flask_musers.views.request')
    def test_pass_POST_data_to_form(self, mock_request, MockRegisterForm, client, data):
        client.post(
            REGISTER_URL,
            data=data
        )

        assert MockRegisterForm.call_args == call(formdata=mock_request.form)

    @patch('flask_musers.views.RegisterForm')
    def test_register_user_when_form_is_valid(self, MockRegisterForm, client, data):
        mock_form = MockRegisterForm.return_value
        mock_form.validate_on_submit.return_value = True

        client.post(
            REGISTER_URL,
            data=data
        )

        assert mock_form.register_user.called

    @patch('flask_musers.views.RegisterForm')
    def test_not_register_user_when_form_is_invalid(self, MockRegisterForm, client, data):
        mock_form = MockRegisterForm.return_value
        mock_form.validate_on_submit.return_value = False

        client.post(
            REGISTER_URL,
            data=data
        )

        assert not mock_form.register_user.called

    @patch('flask_musers.views.RegisterForm')
    def test_redirect_to_login_when_form_is_valid(self, MockRegisterForm, client, data):
        mock_form = MockRegisterForm.return_value
        mock_form.validate_on_submit.return_value = True

        response = client.post(
            REGISTER_URL,
            data=data
        )

        assert response.status_code == httplib.FOUND
        assert response.location.find('login') > -1

    @patch('flask_musers.views.RegisterForm')
    @patch('flask_musers.views.render_template')
    def test_render_template_when_form_is_invalid(self, mock_render_template, MockRegisterForm, client, data):
        mock_form = MockRegisterForm.return_value
        mock_form.validate_on_submit.return_value = False
        mock_render_template.return_value = six.b('')

        response = client.post(
            REGISTER_URL,
            data=data
        )

        assert mock_render_template.called
        assert response.data == mock_render_template.return_value
        assert mock_render_template.call_args == call('musers/register.html', form=mock_form)

    @patch('flask_musers.views.RegisterForm')
    @patch('flask_musers.views.flash')
    def test_flash_message_if_registration_is_successfull(self, mock_flash, MockRegisterForm, client, data):
        mock_form = MockRegisterForm.return_value
        mock_form.validate_on_submit.return_value = True

        client.post(
            REGISTER_URL,
            data=data
        )

        assert mock_flash.called
        assert mock_flash.call_args == call(REGISTRATION_SUCCESS, 'success')

    @patch('flask_musers.views.RegisterForm')
    @patch('flask_musers.views.flash')
    def test_flash_message_if_registration_failed(self, mock_flash, MockRegisterForm, client, data):
        mock_form = MockRegisterForm.return_value
        mock_form.validate_on_submit.return_value = True
        mock_form.register_user.side_effect = NotUniqueError

        client.post(
            REGISTER_URL,
            data=data
        )

        assert mock_flash.called
        assert mock_flash.call_args == call(REGISTRATION_ERROR, 'error')
