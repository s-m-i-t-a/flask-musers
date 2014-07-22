import six
import pytest

if six.PY3:
    import http.client as httplib
else:
    import httplib

from flask_musers.views import register


REGISTER_URL = '/register'


class TestRegisterView(object):
    def test_register_url_resolves_to_register_view(self, app):
        urls = app.url_map.bind('localhost').match(REGISTER_URL)
        view = urls[0]
        f = app.view_functions[view]

        assert f is register

    def test_GET_request_return_status_ok(self, client):
        response = client.get(REGISTER_URL)

        assert response.status_code == httplib.OK
