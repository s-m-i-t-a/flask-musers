===============================
Flask mongo users
===============================

.. image:: https://badge.fury.io/py/flask-musers.png
    :target: http://badge.fury.io/py/flask-musers

.. image:: https://travis-ci.org/s-m-i-t-a/flask-musers.png?branch=master
        :target: https://travis-ci.org/s-m-i-t-a/flask-musers

.. image:: https://coveralls.io/repos/s-m-i-t-a/flask-musers/badge.png
        :target: https://coveralls.io/r/s-m-i-t-a/flask-musers


Flask app for store user in MongoDB and simple views for login, logout and registration.

* Free software: BSD license

Quickstart
----------
Install flask-musers::

    pip install flask-musers

In the app you must init the ``MUsers``::

    from flask import Flask
    from flask.ext.musers import MUsers

    app = Flask(__name__)
    MUsers(app)

and register ``flask-musers`` blueprint::

    from flask_musers.views import musers

    app.register_blueprint(musers)

then must be prepared templates for registration - ``musers/register.html`` and login - ``musers/login.html``.

Views has names ``musers.register``, ``musers.login`` and ``musers.logout``. They are used in ``url_for``::

    from flask import url_for

    url_for('musers.register')
    url_for('musers.login')
    url_for('musers.logout')


Config
------

* ``MUSERS_ALLOW_REGISTRATIONS`` - set to ``False``, when you want disable registrations. Default: ``True``
* ``MUSERS_PASSWORD_VALIDATOR`` - used for custom validator. The dotted name for the object to import. Default: `None`
