# -*- coding: utf-8 -*-

import re
import string


def has_lowercase(value):
    if re.search(r'[a-z]', value):
        return True
    return False


def has_uppercase(value):
    if re.search(r'[A-Z]', value):
        return True
    return False


def has_number(value):
    if re.search(r'\d', value):
        return True

    return False


def has_symbol(value):
    return any(c in string.punctuation for c in value)


def min_length(value, length=8):
    return len(value) >= length


def checker(*args):
    def _checker(value):
        return tuple(fn(value)[1] for fn in args if not fn(value)[0])

    return _checker


def validator(f, message):
    def _validator(value):
        if f(value):
            return (True, '')
        else:
            return (False, message)

    return _validator
