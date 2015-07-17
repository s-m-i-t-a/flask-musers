# -*- coding: utf-8 -*-

import pytest

from flask_musers.models import validate_password, InvalidPassword


def test_password_minimal_lenght():
    with pytest.raises(InvalidPassword) as excinfo:
        validate_password('a')

        assert excinfo.value.message == 'The password must be at least 8 characters long'


def test_weak_password():
    with pytest.raises(InvalidPassword) as excinfo:
        validate_password('aaaaaaaa')

        assert excinfo.value.message == 'The password must contain at least one lowercase letter, one uppercase letter, number and symbol.'


def test_return_strong_password():
    password = 'Ahoj12!b'

    assert validate_password(password) == password
