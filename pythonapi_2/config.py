#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
SECRET_KEY = "wito_python_api"
