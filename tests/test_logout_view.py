import six
import pytest

if six.PY3:
    import http.client as httplib
else:
    import httplib

from mock import patch, call

from flask_musers.views import logout, LOGOUT_SUCCESS


LOGOUT_URL = '/logout'


class TestLogoutView(object):
    def test_logout_url_resolves_to_logout_view(self, app):
        urls = app.url_map.bind('localhost').match(LOGOUT_URL)
        view = urls[0]
        f = app.view_functions[view]

        assert f is logout

    def test_GET_request_return_status_found(self, client):
        response = client.get(LOGOUT_URL)

        assert response.status_code == httplib.FOUND

    @patch('flask_musers.views.logout_user')
    def test_logout_user(self, mock_logout_user, client):
        client.get(LOGOUT_URL)

        assert mock_logout_user.called

    @patch('flask_musers.views.flash')
    def test_flash_message_when_logout(self, mock_flash, client):
        client.get(LOGOUT_URL)

        assert mock_flash.called

        kall = call(**LOGOUT_SUCCESS)
        assert mock_flash.call_args == kall

    @patch('flask_musers.views.redirect')
    def test_redirect_to_home_page(self, mock_redirect, client):
        mock_redirect.return_value = ''

        client.get(LOGOUT_URL)

        assert mock_redirect.called

        kall = call('/')
        assert mock_redirect.call_args == kall
