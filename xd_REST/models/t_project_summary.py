# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from xd_REST import db
from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_, desc
from xd_REST import app, cache
from . import Base, metadata
from xd_REST import session


class TProjectSummary(Base):
    __tablename__ = 't_project_summary'

    id = Column(String(255, 'utf8_croatian_ci'), primary_key=True, index=True, comment='项目主键id 注:用varchar的原因为要使用UUID方式存储')
    project_type = Column(String(50, 'utf8_croatian_ci'), comment='项目类型 从字典表(t_dict)获取')
    project_number = Column(String(255, 'utf8_croatian_ci'), comment='项目编号')
    project_name = Column(String(255, 'utf8_croatian_ci'), comment='项目的名字')
    product_model = Column(String(255, 'utf8_croatian_ci'), comment='产品型号')
    s_number = Column(BIGINT(20), comment='序号')
    project_manager = Column(String(255, 'utf8_croatian_ci'), comment='项目经理')
    classifiation = Column(String(255, 'utf8_croatian_ci'), comment='项目组')
    project_alias = Column(String(255, 'utf8_croatian_ci'), comment='项目的别名')
    oAOder = Column(String(255, 'utf8_croatian_ci'), comment='OA单号')
    isdelete = Column(BIGINT(11), comment='是否已删除 0:否 1:是')
    create_date = Column(TIMESTAMP)
    staff_name = Column(String(50, 'utf8_croatian_ci'), comment='创建人员 从人员表中获取t_staff(staff_name)')
    modify_date = Column(TIMESTAMP, comment='修改日期')
    project_period = Column(BIGINT(11), comment='项目周期 注:项目周期主要指项目开始后完成需要几周')
    status = Column(String(255, 'utf8_croatian_ci'), comment='项目状态 从字典表t_dict(id)获取 主要状态有:进行中，结项,关闭')
    lead_party = Column(String(255, 'utf8_croatian_ci'), comment='主导方 注:主导方主要是:哪个部门或者是公司主导开发的')
    entering_date = Column(TIMESTAMP, comment='录入时间 注:项目的录入时间')
    end_time = Column(TIMESTAMP, comment='结项时间 注:项目结束时间')
    json = Column(JSON, comment='JSON字段主要用于后续的扩展开发')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')

    @staticmethod
    def all_projects(items):
        tb_project = TProjectSummary
        projects = session.query(tb_project.id, tb_project.project_name)\
            .order_by(desc(tb_project.create_date))
        if not items:  # 默认返回所有的数条目
            projects = projects.all()  # 获取所有的项目数据
        else:
            projects = projects.limit(items).all()  # 获取最新的items条项目数据
        return [{"id": i[0], "name": i[1]} for i in projects]  # 列表生成
        # 结构[{},] 示例 [{"id": '005d5b45-4e34-4eb9-b68b-30e0199b6aa5', "name": '宝鸡二维码改造'},]

    @staticmethod
    def fuzzy_query_by_name(query_like):
        """
        查询项目名称中含query_like的条目 并按照日期降序排列
        :param query_like: like查询字符串
        :return:[{"id": ***, "name": ***}, ... ]
        """
        tb_project = TProjectSummary
        # 查询项目名称中含query_like的条目的id与project_name
        query_like = "%{}%".format(query_like)
        projects = session.query(tb_project.id, tb_project.project_name)\
            .filter(tb_project.project_name.like(query_like))\
            .order_by(desc(tb_project.create_date)).all()
        data = [{"id": i[0], "name": i[1]} for i in projects]  # 列表生成
        return True, "数据查询成功", data
