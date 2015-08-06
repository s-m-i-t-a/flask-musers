# -*- coding: utf-8 -*-

import time

import pytest

from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from flask_musers.models import User
from flask_musers.utils import create_token_for, _signer


@pytest.fixture
def user(db):
    return User(email='jozin@zbazin.com', activated=True, name='Jozin Zbazin')


@pytest.fixture
def serializer(app):
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])


def test_token_contains_email(user, serializer):
    token = create_token_for(user, _signer)

    data = serializer.loads(token)

    assert data['email'] == 'jozin@zbazin.com'


def test_token_expire(user, serializer):
    token = create_token_for(user, _signer)

    time.sleep(2)

    with pytest.raises(SignatureExpired):
        serializer.loads(token, max_age=1)
