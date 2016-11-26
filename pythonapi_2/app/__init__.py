#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = "app\\static\\upload"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", 'gif'}
app = Flask(__name__)

app.config.from_object("config")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS
# 判断文件名称是否支持

from app import views, models
