#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, FormField, SubmitField, FieldList, IntegerField
from wtforms.validators import Required, DataRequired


class LoginForm(Form):
    username = StringField("登陆名", validators=[Required()])
    password = PasswordField("密码", validators=[Required()])


class ModelForm(Form):
    model_name = StringField("中文名称", validators=[Required()])


class InterfaceForm(Form):
    interface_name = StringField("接口名称", validators=[Required()])
    interface_url = StringField("接口地址", validators=[Required()])
    interface_method = StringField("接口方法", validators=[Required()])
    request_exam = TextField("请求示例", validators=[Required()])
    response_exam = TextField("返回示例", validators=[Required()])


class ParameterRequestForm(Form):
    parameter_group_id = StringField("从属", validators=[Required()])
    parameter_name = StringField("参数名称", validators=[Required()])
    necessary = StringField("是否必须", validators=[Required()])
    type = StringField("类型", validators=[Required()])
    default = StringField("默认值", validators=[Required()])
    remark = StringField("备注", validators=[Required()])
    level = StringField("层级", validators=[Required()])


class ParameterResponseForm(Form):
    parameter_group_id = StringField("从属", validators=[Required()])
    parameter_name = StringField("参数名称", validators=[Required()])
    necessary = StringField("是否必须", validators=[Required()])
    type = StringField("类型", validators=[Required()])
    default = StringField("示例", validators=[Required()])
    remark = StringField("描述", validators=[Required()])
    level = StringField("层级", validators=[Required()])


class SubmitForm(Form):
    submit = SubmitField("保存")

if __name__ == '__main__':
    print help(FieldList)
