# -*- coding: utf-8 -*-

import pytest

from blinker import signal
from mock import patch, call

from flask_musers.utils import prepare_reset_password_for, reset_password


@pytest.yield_fixture
def mock_get_by_email():
    with patch('flask_musers.utils.User.get_by_email') as mock_get_by_email:
        yield mock_get_by_email


@pytest.yield_fixture
def mock_create_token():
    with patch('flask_musers.utils.create_token_for') as mock_create_token:
        yield mock_create_token


@pytest.yield_fixture
def mock_get_email_from_token():
    with patch('flask_musers.utils.get_email_from_token') as geft:
        yield geft


@pytest.yield_fixture
def mock_signer():
    with patch('flask_musers.utils._signer') as signer:
        yield signer


def test_find_user_by_email(
    mock_get_by_email,
    mock_create_token,
    mock_signer
):
    prepare_reset_password_for('jozin@zbazin.com')

    assert mock_get_by_email.called
    assert mock_get_by_email.call_args == call('jozin@zbazin.com')


def test_create_token_for_found_user(
    mock_get_by_email,
    mock_create_token,
    mock_signer
):
    prepare_reset_password_for('jozin@zbazin.com')

    assert mock_create_token.called
    assert mock_create_token.call_args == call(mock_get_by_email.return_value, mock_signer.return_value)


def test_send_signal_with_user_and_token(
    mock_get_by_email,
    mock_create_token,
    mock_signer
):
    rp = signal('musers-reset-password-token-created')

    @rp.connect
    def catch_signal(user, data):
        catch_signal._called = True
        assert user == mock_get_by_email.return_value
        assert data['token'] == mock_create_token.return_value
    catch_signal._called = False

    prepare_reset_password_for('jozin@zbazin.com')
    assert catch_signal._called, "Signal has not been captured"


def test_reset_password_get_email_from_token(
    mock_get_by_email,
    mock_get_email_from_token,
    mock_signer
):
    reset_password('token', 'password')

    assert mock_get_email_from_token.called
    assert mock_get_email_from_token.call_args == call('token', mock_signer.return_value)


def test_reset_password_get_user(
    mock_get_email_from_token,
    mock_get_by_email,
    mock_signer
):
    reset_password('token', 'password')

    assert mock_get_by_email.called
    assert mock_get_by_email.call_args == call(mock_get_email_from_token.return_value)


def test_reset_password_set_new_password(
    mock_get_by_email,
    mock_get_email_from_token,
    mock_signer
):
    reset_password('token', 'password')

    assert mock_get_by_email.return_value.set_password.called
    assert mock_get_by_email.return_value.set_password.call_args == call(
        'password'
    )
    assert mock_get_by_email.return_value.save.called
