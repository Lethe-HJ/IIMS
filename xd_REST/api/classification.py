from xd_REST.logger import app
from copy import deepcopy
from xd_REST.libs import dst
from xd_REST.libs import auth
from flask import request, current_app, g
from xd_REST.models.t_work_introduction import TWorkIntroduction as TbIntros
from xd_REST.models.t_project_summary import TProjectSummary as TbProject
from xd_REST.models.t_staff import TStaff
from xd_REST.models.t_work_property import TWorkProperty as TbProperty
from xd_REST.models.t_companyframe import CompanyFrame as TFrame, FrameTree
from xd_REST.models.t_daily_record import TDailyRecord as TbDaily
from xd_REST.models.t_concern_staff import TConcernStaff
# from xd_REST.logger import error_log


@app.route('/iims/class/group', methods=["PUT"])
@auth.auth_required
def common_class():
    """
    员工新增分组提交接口
    :return:
    """
    result = deepcopy(dst.my_json)
    result["status"] = 1
    result["message"] = "数据返回成功"
    result["data"] = TStaff.get_all_staff()
    return result