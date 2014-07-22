import six
import pytest

if six.PY3:
    import http.client as httplib
    from unittest.mock import patch, call
else:
    import httplib
    from mock import patch, call

from flask_musers.views import login


LOGIN_URL = '/login'


class TestLoginView(object):
    def test_login_url_resolves_to_login_view(self, app):
        urls = app.url_map.bind('localhost').match(LOGIN_URL)
        view = urls[0]
        f = app.view_functions[view]

        assert f is login
