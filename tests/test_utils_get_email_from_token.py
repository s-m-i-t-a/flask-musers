# -*- coding: utf-8 -*-

import time

import pytest

from itsdangerous import SignatureExpired, BadData

from flask_musers.models import User
from flask_musers.utils import create_token_for, get_email_from_token, _signer


@pytest.fixture
def user(db):
    return User(email='jozin@zbazin.com', activated=True, name='Jozin Zbazin')


@pytest.fixture
def token(user):
    return create_token_for(user, _signer())


def test_get_email_from_token_return_email(user, token):
    email = get_email_from_token(token, _signer())

    assert email == user.email


def test_raise_signature_expired(user, token):
    time.sleep(2)

    with pytest.raises(SignatureExpired):
        get_email_from_token(token, _signer(), max_age=1)


def test_raise_bad_data(user):
    with pytest.raises(BadData):
        get_email_from_token('bad.token', _signer(), max_age=1)
