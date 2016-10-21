# -*- coding: utf-8 -*-

import six

import pytest

from itertools import chain

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from mock import Mock
from mongoengine import signals


database = MongoEngine()


def config():
    return {
        'TESTING': True,
        'MONGODB_SETTINGS': {
            'HOST': 'localhost',
            'PORT': 27017,
            'DB': 'musers_test',
            'USER': None,
            'PASSWORD': None,
        },
        'SECRET_KEY': 'secret',
        'LOGIN_DISABLED': True,
    }


def not_allowed_registration_config(config):
    nar_config = {
        'MUSERS_ALLOW_REGISTRATIONS': False,
    }
    return {key: value for (key, value) in chain(config.items(), nar_config.items())}


def custom_validator_config(config):
    cfg = {
        'MUSERS_PASSWORD_VALIDATOR': 'tests.validator'
    }
    return {key: value for (key, value) in chain(config.items(), cfg.items())}


def create_app(config):
    app = Flask(__name__)

    # config
    for key, value in config.items():
        app.config[key] = value

    database.init_app(app)

    from flask.ext.musers import MUsers
    MUsers(app)

    # register blueprints
    from flask_musers.views import musers
    app.register_blueprint(musers)

    return app


# XXX: when object is created, call ensure_indexes,
# then indexes is set on recreated database.
def ensure_indexes(sender, document, **kwargs):
    document.ensure_indexes()

signals.pre_init.connect(ensure_indexes)


class Db(object):
    def __init__(self, application):
        self.application = application

    def clean(self):
        # smazeme vsechny vytvorene kolekce
        connection_name = self.application.config['MONGODB_SETTINGS']['DB']
        dtb = database.connection[connection_name]
        dtb = dtb.database
        if (self.application.config['MONGODB_SETTINGS']['USER'] and
                self.application.config['MONGODB_SETTINGS']['PASSWORD']):
            user = self.application.config['MONGODB_SETTINGS']['USER']
            password = self.application.config['MONGODB_SETTINGS']['PASSWORD']
            dtb.authenticate(user, password)

        for name in dtb.collection_names(False):
            dtb.drop_collection(name)


def pytest_generate_tests(metafunc):
    if hasattr(metafunc.function, 'not_allowed_registration'):
        metafunc.parametrize('app', ['not_allowed_registration'], indirect=True)
    elif hasattr(metafunc.function, 'custom_validator'):
        metafunc.parametrize('app', ['custom_validator'], indirect=True)


@pytest.fixture
def app(request):
    if getattr(request, 'param', '') == 'not_allowed_registration':
        app = create_app(not_allowed_registration_config(config()))
    elif getattr(request, 'param', '') == 'custom_validator':
        app = create_app(custom_validator_config(config()))
    else:
        app = create_app(config())

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    db = Db(application=app)

    yield db

    db.clean()
