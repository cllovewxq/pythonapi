#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import render_template, redirect, session, url_for

from app import app
from app import db

from models import Interface, Model, User, Parameter
from forms import LoginForm, ModelForm, InterfaceForm, ParameterRequestForm, ParameterResponseForm, SubmitForm


reload(sys)
sys.setdefaultencoding("utf-8")


# 前台首页
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# 前台模块列表
@app.route("/font", methods=["GET", "POST"])
def front():
    model_all = Model.query.all()
    model_forms = []
    for i in range(len(model_all)):
        model_form = {"model_id": model_all[i].model_id,
                      "model_name": model_all[i].model_name}
        model_forms.append(model_form)
    return render_template("front.html",
                           model_forms=model_forms)


# 前台接口列表
@app.route("/front_model/<model_id>", methods=["GET", "POST"])
def front_model(model_id):
    model_one = Model.query.filter_by(model_id=model_id).first()
    interface_model_all = Interface.query.filter_by(model_id=model_id).all()
    interface_model_forms = []
    for i in range(len(interface_model_all)):
        interface_model_form = {"interface_id": interface_model_all[i].interface_id,
                                "interface_name": interface_model_all[i].interface_name,
                                "interface_url": interface_model_all[i].interface_url}
        interface_model_forms.append(interface_model_form)
    return render_template("front_model.html",
                           model_id=model_id,
                           model_one=model_one,
                           interface_model_forms=interface_model_forms)


g_parameter_request = []
g_parameter_response = []


# 前台接口详情
@app.route("/front_interface/<model_id>&<interface_id>", methods=["GET", "POST"])
def front_interface(model_id, interface_id):
    global g_parameter_request, g_parameter_response
    model_one = Model.query.filter_by(model_id=model_id).first()
    interface_model_all = Interface.query.filter_by(model_id=model_id).all()
    interface_model_one = Interface.query.filter_by(interface_id=interface_id).first()
    interface_model_forms = []
    for i in range(len(interface_model_all)):
        interface_model_form = {"interface_id": interface_model_all[i].interface_id,
                                "interface_name": interface_model_all[i].interface_name,
                                "interface_url": interface_model_all[i].interface_url}
        interface_model_forms.append(interface_model_form)
    parameter_request_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=10).all()
    parameter_request_forms = []
    for i in range(len(parameter_request_all)):
        parameter_request_form = {"parameter_id": parameter_request_all[i].parameter_id,
                                  "parameter_name": parameter_request_all[i].parameter_name,
                                  "necessary": parameter_request_all[i].necessary,
                                  "type": parameter_request_all[i].type,
                                  "default": parameter_request_all[i].default,
                                  "remark": parameter_request_all[i].remark,
                                  "parameter_group_id": parameter_request_all[i].parameter_group_id,
                                  "level": parameter_request_all[i].level}
        parameter_request_forms.append(parameter_request_form)
    parameter_response_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=20).all()
    parameter_response_forms = []
    for i in range(len(parameter_response_all)):
        parameter_response_form = {"parameter_id": parameter_response_all[i].parameter_id,
                                   "parameter_name": parameter_response_all[i].parameter_name,
                                   "necessary": parameter_response_all[i].necessary,
                                   "type": parameter_response_all[i].type,
                                   "default": parameter_response_all[i].default,
                                   "remark": parameter_response_all[i].remark,
                                   "parameter_group_id": parameter_response_all[i].parameter_group_id,
                                   "level": parameter_response_all[i].level}
        parameter_response_forms.append(parameter_response_form)
    g_parameter_request = []    # 全局变量、清空列表数据
    g_parameter_response = []   # 全局变量、清空列表数据
    n_parameter_request(parameter_request_forms, 0)
    n_parameter_response(parameter_response_forms, 0)

    return render_template("front_interface.html",
                           model_id=model_id,
                           model_one=model_one,
                           interface_model_forms=interface_model_forms,
                           interface_model_one=interface_model_one,
                           g_parameter_request=g_parameter_request,
                           g_parameter_response=g_parameter_response)


# 请求参数排序
def n_parameter_request(request, parameter_group_id):
    for form in request:
        if form["parameter_group_id"] == parameter_group_id:
            new_parameter_group_id = form["parameter_id"]
            g_parameter_request.append(form)
            n_parameter_request(request, new_parameter_group_id)    # 递归算法
    return g_parameter_request


# 返回参数排序
def n_parameter_response(response, parameter_group_id):
    for form in response:
        if form["parameter_group_id"] == parameter_group_id:
            new_parameter_group_id = form["parameter_id"]
            g_parameter_response.append(form)
            n_parameter_response(response, new_parameter_group_id)  # 递归算法
    return g_parameter_response


# 后台首页
@app.route("/home", methods=["GET", "POST"])
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")


# 后台登录
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_one = User.query.filter_by(user_name=form.username.data).first()
            if user_one.password == form.password.data and user_one.status == 10:
                session["logged_in"] = True
                return redirect(url_for("home"))
            else:
                return render_template("login.html", form=form)
        except AttributeError:
            return render_template("login.html", form=form)
    return render_template("login.html",
                           form=form)


# 后台登出
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))


# 模块管理
@app.route("/model", methods=["GET", "POST"])
def model():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    model_all = Model.query.all()
    model_forms = []
    for i in range(len(model_all)):
        model_form = {"model_id": model_all[i].model_id,
                      "model_name": model_all[i].model_name}
        model_forms.append(model_form)
    return render_template("model.html",
                           model_forms=model_forms)


# 新增模块
@app.route("/addmodel", methods=["GET", "POST"])
def addmodel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_model = ModelForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Model(model_name=add_model.model_name.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("model"))
    return render_template("addmodel.html",
                           add_model=add_model,
                           submit=submit)


# 编辑模块
@app.route("/editmodel/<model_id>", methods=["GET", "POST"])
def editmodel(model_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    model_one = Model.query.filter_by(model_id=model_id).first()
    edit_model = ModelForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        model_one.model_name = edit_model.model_name.data
        db.session.commit()
        return redirect(url_for("model"))
    edit_model.model_name.data = model_one.model_name
    return render_template("editmodel.html",
                           edit_model=edit_model,
                           submit=submit)


# 接口列表
@app.route("/interface/<model_id>")
def interface(model_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    interface_model_all = Interface.query.filter_by(model_id=model_id).all()
    interface_model_forms = []
    for i in range(len(interface_model_all)):
        interface_model_form = {"interface_id": interface_model_all[i].interface_id,
                                "interface_name": interface_model_all[i].interface_name,
                                "interface_url": interface_model_all[i].interface_url}
        interface_model_forms.append(interface_model_form)
    return render_template("interface.html",
                           model_id=model_id,
                           interface_model_forms=interface_model_forms)


# 新增接口
@app.route("/addinterface/<model_id>", methods=["GET", "POST"])
def addinterface(model_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_interface = InterfaceForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Interface(interface_name=add_interface.interface_name.data,
                        model_id=model_id,
                        interface_url=add_interface.interface_url.data,
                        interface_method=add_interface.interface_method.data,
                        request_exam=add_interface.request_exam.data,
                        response_exam=add_interface.response_exam.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("interface",
                                model_id=model_id))
    return render_template("addinterface.html",
                           add_interface=add_interface,
                           model_id=model_id,
                           submit=submit)


# 编辑接口
@app.route("/editinterface/<model_id>&<interface_id>", methods=["GET", "POST"])
def editinterface(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    interface_model_one = Interface.query.filter_by(interface_id=interface_id).first()
    edit_interface_model = InterfaceForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        interface_model_one.interface_name = edit_interface_model.interface_name.data
        interface_model_one.interface_url = edit_interface_model.interface_url.data
        interface_model_one.interface_method = edit_interface_model.interface_method.data
        interface_model_one.request_exam = edit_interface_model.request_exam.data
        interface_model_one.response_exam = edit_interface_model.response_exam.data
        db.session.commit()
        return redirect(url_for("interface",
                                model_id=model_id))
    edit_interface_model.interface_name.data = interface_model_one.interface_name
    edit_interface_model.interface_url.data = interface_model_one.interface_url
    edit_interface_model.interface_method.data = interface_model_one.interface_method
    edit_interface_model.request_exam.data = interface_model_one.request_exam
    edit_interface_model.response_exam.data = interface_model_one.response_exam
    return render_template("editinterface.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           edit_interface_model=edit_interface_model,
                           submit=submit)


# 请求参数列表
@app.route("/parameter_request/<model_id>&<interface_id>", methods=["GET", "POST"])
def parameter_request(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_request_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=10).all()
    parameter_request_forms = []
    for i in range(len(parameter_request_all)):
        parameter_request_form = {"parameter_id": parameter_request_all[i].parameter_id,
                                  "parameter_name": parameter_request_all[i].parameter_name,
                                  "necessary": parameter_request_all[i].necessary,
                                  "type": parameter_request_all[i].type,
                                  "default": parameter_request_all[i].default,
                                  "remark": parameter_request_all[i].remark,
                                  "parameter_group_id": parameter_request_all[i].parameter_group_id,
                                  "level": parameter_request_all[i].level}
        parameter_request_forms.append(parameter_request_form)
    return render_template("parameter_request.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_request_forms=parameter_request_forms)


# 新增请求参数
@app.route("/addparameter_request/<model_id>&<interface_id>", methods=["GET", "POST"])
def addparameter_request(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_parameter_request = ParameterRequestForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Parameter(interface_id=interface_id,
                        parameter_type=10,
                        parameter_group_id=add_parameter_request.parameter_group_id.data,
                        parameter_name=add_parameter_request.parameter_name.data,
                        necessary=add_parameter_request.necessary.data,
                        type=add_parameter_request.type.data,
                        default=add_parameter_request.default.data,
                        remark=add_parameter_request.remark.data,
                        level=add_parameter_request.level.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("parameter_request",
                                model_id=model_id,
                                interface_id=interface_id))
    return render_template("addparameter_request.html",
                           add_parameter_request=add_parameter_request,
                           model_id=model_id,
                           interface_id=interface_id,
                           submit=submit)


# 编辑请求参数
@app.route("/editparameter_request/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def editparameter_request(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_request_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    edit_parameter_request = ParameterRequestForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        parameter_request_one.parameter_name = edit_parameter_request.parameter_name.data
        parameter_request_one.necessary = edit_parameter_request.necessary.data
        parameter_request_one.type = edit_parameter_request.type.data
        parameter_request_one.default = edit_parameter_request.default.data
        parameter_request_one.remark = edit_parameter_request.remark.data
        parameter_request_one.parameter_group_id = edit_parameter_request.parameter_group_id.data
        parameter_request_one.level = edit_parameter_request.level.data
        db.session.commit()
        return redirect(url_for("parameter_request",
                                model_id=model_id,
                                interface_id=interface_id))
    edit_parameter_request.parameter_name.data = parameter_request_one.parameter_name
    edit_parameter_request.necessary.data = parameter_request_one.necessary
    edit_parameter_request.type.data = parameter_request_one.type
    edit_parameter_request.default.data = parameter_request_one.default
    edit_parameter_request.remark.data = parameter_request_one.remark
    edit_parameter_request.parameter_group_id.data = parameter_request_one.parameter_group_id
    edit_parameter_request.level.data = parameter_request_one.level
    return render_template("editparameter_request.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_id=parameter_id,
                           edit_parameter_request=edit_parameter_request,
                           submit=submit)


# 删除请求参数
@app.route("/deleteparameter_request/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def deleteparameter_request(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    deleteparameter_request_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    db.session.delete(deleteparameter_request_one)
    db.session.commit()
    parameter_request_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=10).all()
    parameter_request_forms = []
    for i in range(len(parameter_request_all)):
        parameter_request_form = {"parameter_id": parameter_request_all[i].parameter_id,
                                  "parameter_name": parameter_request_all[i].parameter_name,
                                  "necessary": parameter_request_all[i].necessary,
                                  "type": parameter_request_all[i].type,
                                  "default": parameter_request_all[i].default,
                                  "remark": parameter_request_all[i].remark,
                                  "parameter_group_id": parameter_request_all[i].parameter_group_id,
                                  "level": parameter_request_all[i].level}
        parameter_request_forms.append(parameter_request_form)
    return render_template("parameter_request.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_request_forms=parameter_request_forms)


# 返回参数列表
@app.route("/parameter_response/<model_id>&<interface_id>", methods=["GET", "POST"])
def parameter_response(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_response_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=20).all()
    parameter_response_forms = []
    for i in range(len(parameter_response_all)):
        parameter_response_form = {"parameter_id": parameter_response_all[i].parameter_id,
                                   "parameter_name": parameter_response_all[i].parameter_name,
                                   "necessary": parameter_response_all[i].necessary,
                                   "type": parameter_response_all[i].type,
                                   "default": parameter_response_all[i].default,
                                   "remark": parameter_response_all[i].remark,
                                   "parameter_group_id": parameter_response_all[i].parameter_group_id,
                                   "level": parameter_response_all[i].level}
        parameter_response_forms.append(parameter_response_form)
    return render_template("parameter_response.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_response_forms=parameter_response_forms)


# 新增返回参数
@app.route("/addparameter_response/<model_id>&<interface_id>", methods=["GET", "POST"])
def addparameter_response(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_parameter_response = ParameterResponseForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Parameter(interface_id=interface_id,
                        parameter_type=20,
                        parameter_group_id=add_parameter_response.parameter_group_id.data,
                        parameter_name=add_parameter_response.parameter_name.data,
                        necessary=add_parameter_response.necessary.data,
                        type=add_parameter_response.type.data,
                        default=add_parameter_response.default.data,
                        remark=add_parameter_response.remark.data,
                        level=add_parameter_response.level.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("parameter_response",
                                model_id=model_id,
                                interface_id=interface_id))
    return render_template("addparameter_response.html",
                           add_parameter_response=add_parameter_response,
                           model_id=model_id,
                           interface_id=interface_id,
                           submit=submit)


# 编辑返回参数
@app.route("/editparameter_response/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def editparameter_response(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_response_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    edit_parameter_response = ParameterResponseForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        parameter_response_one.parameter_name = edit_parameter_response.parameter_name.data
        parameter_response_one.necessary = edit_parameter_response.necessary.data
        parameter_response_one.type = edit_parameter_response.type.data
        parameter_response_one.default = edit_parameter_response.default.data
        parameter_response_one.remark = edit_parameter_response.remark.data
        parameter_response_one.parameter_group_id = edit_parameter_response.parameter_group_id.data
        parameter_response_one.level = edit_parameter_response.level.data
        db.session.commit()
        return redirect(url_for("parameter_response",
                                model_id=model_id,
                                interface_id=interface_id))
    edit_parameter_response.parameter_name.data = parameter_response_one.parameter_name
    edit_parameter_response.necessary.data = parameter_response_one.necessary
    edit_parameter_response.type.data = parameter_response_one.type
    edit_parameter_response.default.data = parameter_response_one.default
    edit_parameter_response.remark.data = parameter_response_one.remark
    edit_parameter_response.parameter_group_id.data = parameter_response_one.parameter_group_id
    edit_parameter_response.level.data = parameter_response_one.level
    return render_template("editparameter_response.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_id=parameter_id,
                           edit_parameter_response=edit_parameter_response,
                           submit=submit)


# 删除返回参数
@app.route("/deleteparameter_response/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def deleteparameter_response(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    deleteparameter_response_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    db.session.delete(deleteparameter_response_one)
    db.session.commit()
    parameter_response_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=20).all()
    parameter_response_forms = []
    for i in range(len(parameter_response_all)):
        parameter_response_form = {"parameter_id": parameter_response_all[i].parameter_id,
                                   "parameter_name": parameter_response_all[i].parameter_name,
                                   "necessary": parameter_response_all[i].necessary,
                                   "type": parameter_response_all[i].type,
                                   "default": parameter_response_all[i].default,
                                   "remark": parameter_response_all[i].remark,
                                   "parameter_group_id": parameter_response_all[i].parameter_group_id,
                                   "level": parameter_response_all[i].level}
        parameter_response_forms.append(parameter_response_form)
    return render_template("parameter_response.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_response_forms=parameter_response_forms)


# 用户管理
@app.route("/user", methods=["GET", "POST"])
def user():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user_all = User.query.filter_by(status=10).all()
    user_forms = []
    for i in range(len(user_all)):
        user_form = {"user_id": user_all[i].user_id,
                     "user_name": user_all[i].user_name,
                     "status": user_all[i].status}
        user_forms.append(user_form)
    return render_template("user.html",
                           user_forms=user_forms)

# with app.test_request_context():
#     print url_for("editinterface", x=3, y=10, api_name="actionOpen")
