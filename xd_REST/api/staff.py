from xd_REST.logger import app
from copy import deepcopy
from xd_REST.libs.dst import my_json
from flask import request, current_app, g

from xd_REST.libs.auth import verify_account
# from xd_REST.logger import error_log
from xd_REST.libs import auth
from xd_REST.models.t_staff import TStaff
from xd_REST.models.t_companyframe import CompanyFrame, t_T_CompanyFrame
from xd_REST.models.t_daily_record import TDailyRecord
from sqlalchemy import func
from xd_REST import session


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
            "username": username,
            "department": TStaff.get_department_by_id(g.user.ID)
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
    result["data"]["hours_count"] = session.query(func.sum(TDailyRecord.WorkHours)).filter_by(userid=g.user.ID).first()[0]
    result["data"]["daycounts"] = session.query(func.count(TDailyRecord.WorkDate)).filter_by(userid=g.user.ID).first()[0]
    result["status"] = 1 if success else 0
    return result


@app.route('/iims/staff/group', methods=["GET"])
@auth.auth_required
def staff_group():
    """
    部门分组数据接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    staff_id = request.args.get('target_id', g.user.ID)  # 默认为当前用户id
    result["data"] = CompanyFrame().get_group(staff_id)
    result["status"] = 1
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
#
#
# @app.route('/iims/test/add_group', methods=["GET"])
# def add_group():
#     news = {
#         "Java组": ["张理斌", "王鹏伟", "余哲", "易文杰", "沈力", "章廖", "柯亮", "蔡连", "彭榕"],
#         "测试组": ["侯祥菲", "周小丽"],
#         "前端组": ["毛振", "张宇"],
#         "python组": ["王朝锟", "李所", "谢婷婷"],
#         "UI组": ["李娜", "陈汶卿", "龙慧银"],
#         "项目助理组": ["彭灿", "胡嘉峰"],
#         "算法组": ["丁凡"],
#         "C++组": ["郭灯佳", "曾雷", "郭明"]
#     }
#     for key in news.keys():
#         ids = []
#         for name in news[key]:
#             id = session.query(TStaff.ID).filter_by(StaffName=name).first()
#             id = id[0] if id else -1
#             ids.append(str(id))
#         ids = ",".join(ids)
#         frame = {
#             "Level": 3,
#             "Name": key,
#             "ParentId": 14,
#             "staff": ids,
#             "IsLeaf": 1
#         }
#         sql_0 = """
#         INSERT INTO T_CompanyFrame (Level, Name, IsLeaf, ParentId, staff)
#         VALUES (:Level, :Name, :IsLeaf, :ParentId, :staff);
#         """
#         session.execute(sql_0, frame)
#         session.commit()
