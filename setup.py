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

module_path = os.path.join(os.path.dirname(__file__), 'flask_musers', '__init__.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]
__version__ = eval(version_line.split('__version__ = ')[-1])

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='flask-musers',
    version=__version__,
    description='Flask app for store user in MongoDB'
                ' and simple views for login, logout and registration.',
    long_description=readme + '\n\n' + history,
    author='Jindřich Smitka',
    author_email='smitka.j@gmail.com',
    url='https://github.com/s-m-i-t-a/flask-musers',
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
        'itsdangerous>=0.24',
        'flask-mongoengine>=0.7.0',
        'mongoengine>=0.10',
        'passlib>=1.6.1',
        'blinker>=1.3',
        'six>=1.7.3',
        'pymongo<4.0',
        'funcsigs==1.0.2',
        'Werkzeug>=0.10.4',
        'railroad==0.4.1',
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
