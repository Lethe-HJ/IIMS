from xd_REST.logger import app
from copy import deepcopy
from xd_REST.libs.dst import my_json
from flask import request, current_app, g

from xd_REST.libs.auth import verify_account
# from xd_REST.logger import error_log
from xd_REST.libs import auth
from xd_REST.models.t_staff import TStaff
from xd_REST.models.t_companyframe import CompanyFrame
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
        g.user.save_token(g.user.ID, token)  # 保存token到缓存
        result["data"][0] = {
            "token": token,
            "user_id": g.user.ID,
            "username": username
        }
    return result


@app.route('/iims/staff/center', methods=["GET"])
@auth.auth_required
def staff_center():
    """
    个人中心数据接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码

    success, result["message"], result["data"] = TStaff.staff_center_data()
    result["data"]["label"] = CompanyFrame().get_label()
    result["status"] = 1 if success else 0
    return result


@app.route('/iims/staff/update_password', methods=["POST"])
@auth.auth_required
def staff_update_password():
    """
    用户修改密码
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    target_id = request.json.get('target_id', g.user.ID)  # 默认为当前用户id
    password = request.json.get('password', "E10ADC3949BA59ABBE56E057F20F883E")  # 默认为123456
    success, result["message"] = TStaff.update_password(target_id, password)
    result["status"] = 1 if success else 0
    return result
