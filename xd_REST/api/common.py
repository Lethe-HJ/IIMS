from xd_REST.logger import app
from copy import deepcopy
from xd_REST.libs import dst
from xd_REST.libs import auth
from flask import request, current_app, g
from xd_REST.models.t_work_introduction import TWorkIntroduction as TbIntros
from xd_REST.models.t_project_summary import TProjectSummary as TbProject
from xd_REST.models.t_staff import TStaff
from xd_REST.models.t_work_property import TWorkProperty as TbProperty
from xd_REST.models.t_companyframe import t_T_CompanyFrame as TFrame, FrameTree
from xd_REST.models.t_daily_record import TDailyRecord as TbDaily
from xd_REST.models.t_concern_staff import TConcernStaff
# from xd_REST.logger import error_log

my_json = deepcopy(dst.my_json)
my_json["data"] = {}


@app.route('/iims/common/projects/data', methods=["GET"])
@auth.auth_required
def common_projects_data():
    """
    项目信息数据接口c0
    :return:
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    limit = request.args.get("limit", None)
    projects = []
    projects.extend(TbIntros.history_projects_in_intros())
    projects.extend(TbProject.all_projects(limit))  # 获取最近的limit个项目 以 [{"id":***, "name":***}]形式
    projects = sorted(set(projects), key=projects.index)  # 保留原顺序的去重
    result["data"]["projects"] = [{"id": i[0], "name": i[1]} for i in projects]
    return result


@app.route('/iims/common/projects/query', methods=["GET"])
@auth.auth_required
def common_projects_query():
    """
    项目信息查询接口c2
    :return:
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    query = request.args.get("query", None)
    success, result["message"], result["data"]["projects"] = TbProject.fuzzy_query_by_name(query)
    result["status"] = 1 if success else 0
    return result


@app.route('/iims/common/intros/data', methods=["GET"])
@auth.auth_required
def common_intros_data():
    """
    项目简介信息数据接口c1
    :return:
    """

    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    try:
        project_id = request.args["project_id"]
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = 2
        return result
    result["data"]["intros"] = TbIntros.intros_of_project(project_id)
    return result


@app.route('/iims/common/intros/query', methods=["GET"])
@auth.auth_required
def common_intros_query():
    """
    项目简介信息查询接口c3
    :return:
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    try:
        query = request.args["query"]
        project_id = request.args["project_id"]
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = 2
        return result
    result["data"]["intros"] = TbIntros.search_his_intros(query, project_id)
    return result


@app.route('/iims/common/property/data', methods=["GET"])
@auth.auth_required
def common_property_data():
    """
    工作性质数据接口c4
    :return:
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    result["data"]["property"] = TbProperty.all_properties()
    return result


@app.route('/iims/common/classification', methods=["GET"])
@auth.auth_required
def common_classification():
    """
    分类信息接口
    :return:
    """
    pattern = request.args.get("pattern", "group")
    result = deepcopy(my_json)
    frame_tree = FrameTree(pattern)
    frame_tree = frame_tree.build_tree()
    result["status"] = 1
    result["message"] = "数据返回成功"
    result["data"] = frame_tree
    return result


@app.route('/iims/common/concern', methods=["GET"])
@auth.auth_required
def common_concern():
    """
    我的关注查询接口
    :return:
    """
    result = deepcopy(my_json)
    result["status"] = 1
    result["message"] = "数据返回成功"
    result["data"] = TConcernStaff.get_his_concern()
    return result


@app.route('/iims/common/concern', methods=["PUT"])
@auth.auth_required
def common_concern_edit():
    """
    我的关注编辑提交接口
    :return:
    """
    result = deepcopy(my_json)
    try:
        concern = request.json['concern']
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result
    TConcernStaff.update_concern(concern)
    result["status"] = 1
    result["message"] = "数据返回成功"
    return result


@app.route('/iims/common/staff', methods=["GET"])
@auth.auth_required
def common_staff():
    """
    员工姓名数据查询接口
    :return:
    """
    result = deepcopy(my_json)
    result["status"] = 1
    result["message"] = "数据返回成功"
    result["data"] = TStaff.get_all_staff()
    return result


@app.route('/iims/common/class', methods=["PUT"])
@auth.auth_required
def common_class():
    """
    员工新增分组提交接口
    :return:
    """
    result = deepcopy(my_json)
    result["status"] = 1
    result["message"] = "数据返回成功"
    result["data"] = TStaff.get_all_staff()
    return result