import six
import pytest

if six.PY3:
    from unittest.mock import patch, call
else:
    from mock import patch, call

from flask_musers import MUsers


class TestMUsers(object):
    @patch('flask_musers.User.get_active_user_by_pk_or_none')
    def test_load_user(self, mock_get_active_user_by_pk_or_none):
        mu = MUsers()
        mu.load_user('1234567')

        assert mock_get_active_user_by_pk_or_none.called

        kall = call('1234567')
        assert mock_get_active_user_by_pk_or_none.call_args == kall

    @patch('flask_musers.User.get_active_user_by_pk_or_none')
    def test_load_user_return_none_when_user_dont_exists(self, mock_get_active_user_by_pk_or_none):
        mock_get_active_user_by_pk_or_none.return_value = None

        mu = MUsers()
        user = mu.load_user('1234567')

        assert user is None

    @patch('flask_musers.User.get_active_user_by_pk_or_none')
    def test_load_user_return_user_object(self, mock_get_active_user_by_pk_or_none):

        mu = MUsers()
        user = mu.load_user('1234567')

        assert user == mock_get_active_user_by_pk_or_none.return_value
