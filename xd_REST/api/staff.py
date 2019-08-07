from xd_REST import app
from copy import deepcopy
from xd_REST.libs.dst import my_json
from flask import request, current_app, g
from xd_REST.libs.auth import verify_account


@app.route('/iims/staff/login', methods=["POST"])
def login():
    """
    用户登录接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    success, result["message"], result["status"] = verify_account(username, password)  # 验证账户
    if success:
        token = g.user.generate_auth_token()
        g.user.save_token(g.user.id, token)  # 保存token到缓存
        result["data"][0] = {
            "token": token,
            "user_id": g.user.id,
            "username": username
        }
    return result

#
# @app.route('/iims/workdailys/show', methods=["GET"])
# #@auth.auth_required
# def workdailys_get():
#     """
#     工作日报管理页查询 接口
#     :return:
#     """
#     result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
#     detail = request.args.get('detail', None)
#     query = request.args.get('query', None)
#     page = request.args.get('page', None)  # 分页预留
#     per_page = request.args.get('per_page', None)  # 分页预留
#     result["data"] = DDailyRecord.himself_dailys(detail, query)
#     return result
#
#
# @app.route('/iims/workdailys/edit', methods=["GET"])
# #@auth.auth_required
# def workdailys_edit_get():
#     """
#     工作日报 修改页 显示数据查询 接口
#     :return:
#     """
#     result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
#     try:
#         daily_id = request.args["daily_id"]
#     except KeyError as e:
#         result["message"] = e.args[0] + "字段不能为空"
#         result["status"] = "0"
#         return result
#     success, result["data"], result["message"] = DDailyRecord.edit_page_get(daily_id)
#     result["status"] = 1 if success else 0  # 成功状态码为1 失败状态码为0
#     return result
#
# @app.route('/iims/workdailys/add', methods=["POST"])
# #@auth.auth_required
# def workdailys_add_submit():
#     """
#     工作日报 新增页面 提交接口
#     :return:
#     """
#     result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
#     try:
#         work_date = request.json['work_date']
#         work_hours = request.json['work_hours']
#         project_id = request.json['project_id']
#         item_id = request.json['item_id']
#         matters = request.json['matters']
#     except KeyError as e:
#         result["message"] = "ヘ(_ _ヘ)服了 " + e.args[0] + "字段不能为空"
#         result["status"] = 0
#         return result
#     daily = DDailyRecord(work_date=work_date, work_hours=work_hours, project_id=project_id,
#                          work_item_id=item_id, matters=matters)
#     success, result["message"] = DDailyRecord.add_daily(daily)  # 更新数据
#     result["status"] = 1 if success else 0
#     return result
#
# @app.route('/iims/workdailys/edit', methods=["PUT"])
# #@auth.auth_required
# def workdailys_eidt_submit():
#     """
#     工作日报 编辑页面 提交接口
#     :return:
#     """
#     result = deepcopy(my_json)  # 存储给用户的提示信息msg,状态码以及数据
#     try:
#         daily_id = request.json["daily_id"]
#         work_date = request.json['work_date']
#         work_hours = request.json['work_hours']
#         project_id = request.json['project_id']
#         item_id = request.json['item_id']
#         matters = request.json['matters']
#     except KeyError as e:
#         result["message"] = "ヘ(_ _ヘ)服了 " + e.args[0] + "字段不能为空"
#         result["status"] = 0
#         return result
#     daily = DDailyRecord(id=daily_id, work_date=work_date, work_hours=work_hours, project_id=project_id,
#                         work_item_id=item_id, matters=matters)
#     success, result["message"] = DDailyRecord.update_daily(daily)  # 更新数据
#     result["status"] = 1 if success else 0
#     return result
