# -*- coding: utf-8 -*-

from mock import Mock, call

from flask_musers.validators import validator


def test_return_validation_function():
    f = validator(lambda: None, "message")

    assert callable(f)


def test_created_validator_call_given_function_with_param():
    f = Mock()
    param = "test"

    valid = validator(f, "message")

    valid(param)

    assert f.called
    assert f.call_args == call(param)


def test_created_validator_return_tuple_with_empty_message_and_true_when_given_function_return_true():
    f = validator(lambda x: True, "message")

    result = f("test")

    assert result[0]
    assert result[1] == ""


def test_create_validator_return_tuple_with_message_and_false_when_given_function_return_false():
    f = validator(lambda x: False, "message")

    result = f("test")

    assert not result[0]
    assert result[1] == "message"
