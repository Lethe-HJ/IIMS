# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text, Float
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from xd_REST import db
from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_, desc
from xd_REST import app, cache
from . import Base, metadata
from .t_work_introduction import TWorkIntroduction as TbIntro
from .t_project_summary import TProjectSummary as TbProject
from .t_staff import TStaff
from xd_REST import session
from xd_REST.logger import error_log


class TDailyRecord(Base):
    __tablename__ = 't_daily_record'

    id = Column(BIGINT(20), primary_key=True, comment='每日日报ID:主键')
    work_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='工作时间 注:当前日期 如:2018-11.29')
    weeks = Column(BIGINT(11), comment='周 注:该年的第几周')
    day_in_week = Column(String(50, 'utf8_croatian_ci'), comment='星期几 注:一周七天 1,2,3,4,5,6,7')
    job_description = Column(String(255, 'utf8_croatian_ci'), comment='工作简介 从工作简历表获取t_work_introduction(work_intro)')
    work_hours = Column(Float(7), comment='工时 注:上班小时')
    work_matters = Column(String(3000, 'utf8_croatian_ci'), comment='工作事项 注:每天工作的内容')
    staff_name = Column(String(255, 'utf8_croatian_ci'), comment='人员姓名 从人员表中获取:t_staff(saff_name)')
    project_name = Column(String(255, 'utf8_croatian_ci'), comment='项目名称 从项目表中获取t_project_summary(project_name) 注:主要方便查询!')
    descrip_number = Column(BIGINT(11), comment='工作简介序号 从工作简历表获取t_work_introduction(s_number)')
    project_id = Column(String(255, 'utf8_croatian_ci'), index=True, comment='项目ID 外键:t_project_summary(id)')
    isdelete = Column(BIGINT(11), server_default=text("'0'"), comment='是否已删除 0：否 1:是')
    create_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    workintro_id = Column(BIGINT(20), index=True, comment='工作简介ID 外键:t_work_introduction(id)')
    staff_id = Column(BIGINT(20), index=True, comment='人员ID 外键:t_staff(id)')
    business_unit_id = Column(ForeignKey('t_business_unit.id'), index=True, comment='部门ID 外键:t_business_unit(id)')
    json = Column(JSON, comment='JSON字段用于日报后续扩展开发')

    business_unit = relationship('TBusinessUnit')

    @staticmethod
    @error_log
    def his_all_daily(detail):
        """
        获取当前用户的工作日报
        :param detail: 详细与否
        :return: data字典
        """
        current_user = g.user.id
        # current_user = 199
        tb_daily = TDailyRecord  # 名字太长 换个短点的名字
        # 查询当前用户的所有工作日报 按创建时间排序
        his_dailies = session.query(tb_daily).filter_by(staff_id=current_user) \
            .order_by(desc(tb_daily.create_date)).all()
        return tb_daily.pack_daily_data(his_dailies, detail)


    @staticmethod
    @error_log
    def query_daily(detail, query=None):
        """
        获取当前用户的工作日报
        :param detail: 详细与否
        :param query: 查询的信息
        :return: data字典
        """
        tb_daily = TDailyRecord  # 名字太长 换个短点的名字
        his_dailies = tb_daily.search_bar_entries(query)  # 获取给搜索栏的条目
        return tb_daily.pack_daily_data(his_dailies, detail)


    @staticmethod
    @error_log
    def pack_daily_data(dailies, detail=None):
        data_li = []
        for daily in dailies:  # 遍历当前用户的所有工作简介条目
            data = {}  # 每次循环需要重新新建data字典
            data["daily_id"] = daily.id  # 工作日报id
            # 工作简介名称
            data["work_intro"] = session.query(TbIntro.work_intro).filter_by(id=daily.workintro_id).first()[0]
            # 项目名称
            data["project_name"] = session.query(TbProject.project_name).filter_by(id=daily.project_id).first()[0]
            data["work_date"] = daily.work_date  # 工作日期
            if detail:  # 详细查询要多出工时,具体事项字段
                data["work_hours"] = daily.work_hours  # 工时
                data["work_matters"] = daily.work_matters  # 具体事项
            data_li.append(data)  # 将data字典添加到data_li数组尾部
        return data_li


    @staticmethod
    @error_log
    def add_daily(**kwargs):
        kwargs["staff_id"] = g.user.id
        daily = TDailyRecord(**kwargs)
        daily.staff_name = session.query(TStaff.staff_name).filter_by(id=g.user.id).first()[0]
        daily.project_name = session.query(TbProject.project_name).filter_by(id=kwargs["project_id"]).first()[0]
        session.add(daily)
        session.commit()


    @staticmethod
    @error_log
    def edit_daily(daily_id, **kwargs):
        the_daily = session.query(TDailyRecord).filter_by(id=daily_id)
        if the_daily.first().staff_id != g.user.id:
            return False, "不能修改他人创建的工作简介"
        else:
            the_daily.update(kwargs)
            session.commit()
            return True, "数据修改成功"


    @staticmethod
    @error_log
    def search_bar_entries(query):
        """
        查询给搜索栏的条目
        :return:
        """
        # 如果query是项目 查询query值相应的项目的id
        sql_0 = """
                SELECT id
                FROM t_project_summary
                WHERE project_name LIKE :query"""
        sql_1 = """
                SELECT id
                FROM t_work_introduction
                WHERE work_intro LIKE :query"""
        # 查询 (这个项目id对应的工作日报条目 或 query值为工作简介内容的)且必为当前用户创建的 工作日报条目
        sql_2 = """
                SELECT id, workintro_id, project_id, work_date, work_hours, work_matters 
                FROM t_daily_record
                WHERE (workintro_id IN ({0}) OR project_id IN ({1})) AND staff_id=:staff_id
                ORDER BY create_date DESC;
                    """.format(sql_1, sql_0)  # 嵌套查询 这个查询比较复杂 所以用原生sql来查
        args_1 = {"query": "%{}%".format(query), "staff_id": g.user.id}
        his_dailies = session.execute(sql_2, args_1)  # @1 执行的sql代码见本文件末尾
        return his_dailies


    @staticmethod
    @error_log
    def get_the_daily(daily_id):
        data = {}  # 每次循环需要重新新建data字典
        daily = session.query(TDailyRecord).filter_by(id=daily_id).first()
        if daily.staff_id != g.user.id:
            return False, "不能查看他人的工作日报", data
        data["daily_id"] = daily.id  # 工作日报id
        # 工作简介名称
        # 项目名称
        data["work_date"] = daily.work_date  # 工作日期
        data["work_hours"] = daily.work_hours  # 工时
        data["work_matters"] = daily.work_matters  # 具体事项
        data["project_name"] = session.query(TbProject.project_name).filter_by(id=daily.project_id).first()[0]
        data["project_id"] = daily.project_id  # 当前日报对应的的项目id
        data["workintro_id"] = daily.workintro_id  # 当前日报对应的的工作简介id
        data["work_intro"] = session.query(TbIntro.work_intro).filter_by(id=daily.workintro_id).first()[0]
        return True, "数据查询成功", data
