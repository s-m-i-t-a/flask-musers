# -*- coding: utf-8 -*-

import pytest

from flask_musers.models import User
from flask_musers.utils import create_token_for, get_email_from_token, _signer


@pytest.fixture
def user(db):
    return User(email='jozin@zbazin.com', activated=True, name='Jozin Zbazin')


@pytest.fixture
def token(user):
    return create_token_for(user)


def test_get_email_from_token_return_email(user, token):
    email = get_email_from_token(token, _signer())

    assert email == user.email
