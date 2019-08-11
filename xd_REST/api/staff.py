from xd_REST import app
from copy import deepcopy
from xd_REST.libs.dst import my_json
from flask import request, current_app, g
from xd_REST.libs.auth import verify_account
from xd_REST.logger import error_log

@error_log
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