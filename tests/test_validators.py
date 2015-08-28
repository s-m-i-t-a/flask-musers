# -*- coding: utf-8 -*-


from flask_musers.validators import has_lowercase, has_uppercase, has_number, has_symbol, min_length


def test_lowercase_return_true_when_value_contains_lowercase_char():
    assert has_lowercase('aBBBBBB')


def test_lowercase_return_false_when_value_not_contains_lowercase_char():
    assert not has_lowercase('ABBBBBB')


def test_uppercase_return_true_when_value_contains_uppercase_char():
    assert has_uppercase('aBBBBBB')


def test_uppercase_return_false_when_value_not_contains_uppercase_char():
    assert not has_uppercase('abbbbbb')


def test_number_return_true_when_value_contains_number_char():
    assert has_number('a3BBBBB')


def test_number_return_false_when_value_not_contains_number_char():
    assert not has_number('abbbbbb')


def test_symbol_return_true_when_value_contains_symbol_char():
    assert has_symbol('a3.BBBB')


def test_symbol_return_false_when_value_not_contains_symbol_char():
    assert not has_symbol('abbbbbb')


def test_min_length_return_true_when_value_have_at_least_given_number_chars():
    assert min_length('aaaaaaaa', 8)


def test_min_length_return_false_when_value_have_less_then_given_number_chars():
    assert not min_length('aaaaaaa', 8)
