# -*- coding: utf-8 -*-

import six

import pytest

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from mongoengine import signals


database = MongoEngine()


def create_app():
    app = Flask(__name__)

    # config
    app.config['TESTING'] = True
    app.config['MONGODB_SETTINGS'] = {
        'HOST': 'localhost',
        'PORT': 27017,
        'DB': 'musers_test',
    }
    app.config['SECRET_KEY'] = 'secret'

    database.init_app(app)

    from flask_musers import login_manager
    login_manager.init_app(app)

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
        if (self.application.config['MONGODB_SETTINGS']['USER'] and
                self.application.config['MONGODB_SETTINGS']['PASSWORD']):
            user = self.application.config['MONGODB_SETTINGS']['USER']
            password = self.application.config['MONGODB_SETTINGS']['PASSWORD']
            dtb.authenticate(user, password)

        for name in dtb.collection_names():
            if not name.startswith('system'):
                dtb.drop_collection(name)


@pytest.fixture
def app(request):
    app = create_app()

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
def db(request, app):
    db = Db(application=app)

    request.addfinalizer(db.clean)

    return db
