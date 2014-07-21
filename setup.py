#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='flask-musers',
    version='0.0.2',
    description='Flask app for store user in MongoDB'
                ' and simple views for login, logout and registration.',
    long_description=readme + '\n\n' + history,
    author='Jindřich Smitka',
    author_email='smitka.j@gmail.com',
    url='https://bitbucket.org/jsmitka/flask-musers',
    packages=[
        'flask_musers',
    ],
    package_dir={'flask-musers': 'flask_musers'},
    include_package_data=True,
    install_requires=[
        'Flask>=0.10.1',
        'Flask-Login>=0.2.7',
        'WTForms>=1.0.4',
        'Jinja2>=2.7',
        'passlib>=1.6.1',
        'flask-mongoengine>=0.7.0',
        'mongoengine',
    ],
    license="BSD",
    zip_safe=False,
    keywords='flask-musers',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
