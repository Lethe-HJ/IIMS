from xd_REST import app
from copy import deepcopy
from xd_REST.libs.dst import my_json
from xd_REST.libs import auth
from flask import request, current_app, g
from xd_REST.models.t_work_introduction import TWorkIntroduction as TbIntros
from xd_REST.models.t_project_summary import TProjectSummary as TbProject
from xd_REST.models.t_work_property import TWorkProperty as TbProperty


@app.route('/iims/intros/data', methods=["GET"])
@auth.auth_required
def intros_data():
    """
    工作简介数据接口i1
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    detail = bool(request.args.get('detail', None))  # 前端传过来的的true与false是字符串 需转为bool
    query = request.args.get('query', None)
    page = request.args.get('page', None)  # 分页预留
    per_page = request.args.get('per_page', None)  # 分页预留
    result["data"] = TbIntros.himself_intros(detail)
    result["message"] = "数据获取成功"
    return result


@app.route('/iims/intros/query', methods=["GET"])
@auth.auth_required
def intros_query():
    """
    工作简介查询接口i2
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    detail = bool(request.args.get('detail', None))  # 前端传过来的的true与false是字符串 需转为bool
    query = request.args.get('query', None)
    page = request.args.get('page', None)  # 分页预留
    per_page = request.args.get('per_page', None)  # 分页预留
    result["data"] = TbIntros.query_daily(detail, query)
    result["message"] = "数据获取成功"
    return result


@app.route('/iims/intros/edit/data', methods=["GET"])
@auth.auth_required
def intros_edit_data():
    """
    当前工作简介信息接口i4
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    result["data"] = {}

    try:
        intro_id = request.args["intro_id"]  # 日报id必须有
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result
    # 查询当前工作日报的编辑信息
    success, result["message"], result["data"] = TbIntros.get_the_intro(intro_id)
    return result


@app.route('/iims/intros/add', methods=["POST"])
@auth.auth_required
def intros_add():
    """
    工作简介新增提交接口i3
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = {}
    try:
        args["work_address"] = request.json['work_address']
        args["work_property_id"] = request.json['work_property_id']
        args["project_id"] = request.json['project_id']
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result
    args["work_intro"] = request.json.get('work_intro', None)  # work_intro字段可以为空
    args["remarks"] = request.json.get('remarks', None)  # remark字段可以为空
    TbIntros.add_intro(**args)
    result["message"] = "工作简介新增成功"
    return result


@app.route('/iims/intros/edit', methods=["PUT"])
@auth.auth_required
def intros_edit():
    """
    工作简介编辑提交接口i5
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = {}
    try:
        intro_id = request.json['intro_id']
        args["work_address"] = request.json['work_address']
        args["work_property_id"] = request.json['work_property_id']
        args["project_id"] = request.json['project_id']
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result
    args["work_intro"] = request.json.get('work_intro', None)  # work_intro字段可以为空
    args["remarks"] = request.json.get('remarks', None)  # remark字段可以为空
    success, result["message"] = TbIntros.edit_intro(intro_id, **args)
    result["status"] = 1 if success else 0
    return result
