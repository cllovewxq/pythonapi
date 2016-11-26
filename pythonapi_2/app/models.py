#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64))
    password = db.Column(db.String(64))
    status = db.Column(db.Integer)
    level = db.Column(db.Integer)


class Model(db.Model):
    model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(256))
    status = db.Column(db.Integer)


class Interface(db.Model):
    interface_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer, db.ForeignKey("model.model_id"))
    interface_name = db.Column(db.String(64))
    interface_url = db.Column(db.String(1024))
    interface_method = db.Column(db.String(64))
    request_exam = db.Column(db.String(4096))
    response_exam = db.Column(db.String(4096))
    status = db.Column(db.Integer)


class Parameter(db.Model):
    parameter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_id = db.Column(db.Integer, db.ForeignKey("interface.interface_id"))
    parameter_type = db.Column(db.String(64))
    parameter_group_id = db.Column(db.Integer)
    parameter_name = db.Column(db.String(64))
    necessary = db.Column(db.String(64))
    type = db.Column(db.String(64))
    default = db.Column(db.String(64))
    remark = db.Column(db.String(64))
    level = db.Column(db.String(64))
