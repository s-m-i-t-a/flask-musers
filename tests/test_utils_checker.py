# -*- coding: utf-8 -*-

from mock import Mock, call

from flask_musers.utils import checker


def test_return_checker_function():
    f = checker()

    assert callable(f)


def test_checker_call_given_functions_with_given_param():
    param = "test"
    f1 = Mock(return_value=(True, ""))
    f2 = Mock(return_value=(True, ""))

    f = checker(f1, f2)

    f(param)

    assert f1.called
    assert f1.call_args == call(param)

    assert f2.called
    assert f2.call_args == call(param)


def test_created_checker_return_zero_length_tuple_when_no_error_occurs():
    f1 = Mock(return_value=(True, ""))
    f2 = Mock(return_value=(True, ""))

    f = checker(f1, f2)

    result = f("test")

    assert len(result) == 0


def test_created_checker_return_error_messages_in_tuple_when_validator_funcs_failure():
    f1 = Mock(return_value=(False, "Error 1"))
    f2 = Mock(return_value=(False, "Error 2"))

    f = checker(f1, f2)

    result = f("test")

    assert "Error 1" in result
    assert "Error 2" in result
