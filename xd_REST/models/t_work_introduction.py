# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, JSON, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import CHAR, Column, DateTime, String, or_, and_, desc
from . import Base, metadata
from .t_project_summary import TProjectSummary as TbProject
from .t_work_property import TWorkProperty
from .t_staff import TStaff
from xd_REST import session
from flask import current_app, g


class TWorkIntroduction(Base):
    __tablename__ = 't_work_introduction'

    id = Column(BIGINT(20), primary_key=True, comment='工作简介主键id')
    s_number = Column(BIGINT(11), comment='序号')
    work_address = Column(String(50, 'utf8_croatian_ci'), comment='工作地址')
    work_property_id = Column(ForeignKey('t_work_property.id'), index=True, comment='工作性质')
    project_id = Column(String(255, 'utf8_croatian_ci'), index=True, comment='项目id')
    work_intro = Column(String(300, 'utf8_croatian_ci'), comment='工作简介')
    create_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    staff_id = Column(ForeignKey('t_staff.id'), index=True, comment='人员ID')
    staff_name = Column(String(50, 'utf8_croatian_ci'), comment='人员姓名')
    work_status = Column(BIGINT(255), comment='工作状态')
    json = Column(JSON, comment='JSON类型用于工作简介后续扩展开发')
    remarks = Column(String(200, 'utf8_croatian_ci'), comment='备注')

    staff = relationship('TStaff')
    work_property = relationship('TWorkProperty')

    @staticmethod
    def search_entries_projects(query):
        """
        查询给搜索栏的条目
        :return:
        """
        # 如果query是项目 查询query值相应的项目的id
        sql_0 = """
            SELECT id
            FROM t_project_summary
            WHERE project_name LIKE :query"""
        # 查询 (这个项目id对应的工作简介条目 或 query值为工作简介内容的)且必为当前用户创建的 工作简介条目
        sql_1 = """
            SELECT id, work_intro, project_id, work_address, work_property_id, staff_id
            FROM t_work_introduction
            WHERE (work_intro LIKE :query OR project_id IN ({0})) AND staff_id=:staff_id
            ORDER BY create_date DESC;
                """.format(sql_0)  # 嵌套查询 这个查询比较复杂 所以用原生sql来查
        args_1 = {"query": "%{}%".format(query), "staff_id": g.user.id}
        his_intros = session.execute(sql_1, args_1)  # @1 执行的sql代码见本文件末尾
        return his_intros


    @staticmethod
    def himself_intros(detail):
        """
        获取当前用户的工作简介
        :param detail: 详细与否
        :param query: 查询的信息
        :return: data字典
        """
        data_li = []
        current_user = g.user.id
        # current_user = 199
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        # 查询当前用户的所有工作简介 按创建时间排序
        his_dailies = session.query(tb_intro).filter_by(staff_id=current_user) \
            .order_by(desc(tb_intro.create_date)).all()
        return tb_intro.pack_intro_data(his_dailies, detail)


    @staticmethod
    def query_daily(detail, query=None):
        """
        查询当前用户的工作简介
        :param detail: 详细与否
        :param query: 查询的信息
        :return: data字典
        """
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        his_intros = tb_intro.search_entries_projects(query)  # 获取给搜索栏的条目
        return tb_intro.pack_intro_data(his_intros, detail)


    @staticmethod
    def pack_intro_data(intros, detail=None):
        data_li = []
        for intro in intros:  # 遍历当前用户的所有工作简介条目
            data = {}  # 每次循环需要重新新建data字典
            data["intro_id"] = intro.id  # 工作日报id
            # 项目名称
            data["project_name"] = session.query(TbProject.project_name).filter_by(id=intro.project_id).first()[0]
            data["work_intro"] = intro.work_intro  # 工作日期
            if detail:  # 详细查询要多出工时,具体事项字段
                data["work_address"] = intro.work_address  # 工作地址
                data["work_property"] = session.query(TWorkProperty.work_property_name)\
                        .filter_by(id=intro.work_property_id).first()
            data_li.append(data)  # 将data字典添加到data_li数组尾部
        return data_li


    @staticmethod
    def his_all_intros():
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        his_intros = session.query(tb_intro.id, tb_intro.work_intro).filter_by(staff_id=g.user.id).all()
        return [{"id": i.id, "name": i.work_intro} for i in his_intros]  # 列表生成
        # 结构[{},] 示例 [{"id": 9676, "name": '美签项目 自动填表功能技术验证'},]

    @staticmethod
    def fuzzy_query_by_name(project_id, query_like):
        """
        查询工作简介名称中含query_like的条目(且属于当前项目,可选) 并按照日期降序排列
        :param query_like: 限制条件 like查询字符串
        :param project_id: 限制条件 项目id
        :return:[{"id": ***, "name": ***}, ... ]
        """
        tb_intros = TWorkIntroduction
        # 查询工作简介名称中含query_like的条目的id与work_intro
        condition = and_(tb_intros.work_intro.like(query_like), tb_intros.staff_id==g.user.id)
        if project_id:  # 如果有project_id 则将其加入and条件中
            condition = and_(condition, tb_intros.project_id==project_id)
        intros = session.query(tb_intros.id, tb_intros.work_intro) \
            .filter(condition).order_by(desc(tb_intros.create_date)).all()
        return [{"id": i[0], "name": i[1]} for i in intros]  # 列表生成

    @staticmethod
    def add_intro(**intro):
        the_intro = TWorkIntroduction(**intro)
        the_intro.staff_id = g.user.id
        the_intro.staff_name = session.query(TStaff.staff_name).filter_by(id=g.user.id).first()[0]
        session.add(the_intro)
        session.commit()


    @staticmethod
    def edit_intro(intro_id, **kwargs):
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        the_intro = session.query(tb_intro).filter_by(id=intro_id)
        if the_intro.first().staff_id != g.user.id:
            return False, "不能修改他人创建的工作简介"
        else:
            the_intro.update(kwargs)
            session.commit()
            return True, "工作简介修改成功"


    @staticmethod
    def get_the_intro(intro_id):
        data = {}  # 每次循环需要重新新建data字典
        intro = session.query(TWorkIntroduction).filter_by(id=intro_id).first()
        if intro.staff_id != g.user.id:
            return False, "不能查看他人的工作简介", data
        data["intro_id"] = intro.id  # 工作简介id
        data["work_intro"] = intro.work_intro  # 工作简介名称
        data["project_name"] = session.query(TbProject.project_name) \
            .filter_by(id=intro.project_id).first()[0]  # 项目名称
        data["work_address"] = intro.work_address  # 工作地址
        # 查询这个工作简介对应的工作性质
        data["work_property"] = session.query(TWorkProperty.work_property_name) \
            .filter_by(id=intro.work_property_id).first()[0]
        return True, "数据查询成功", data


    @staticmethod
    def intros_of_project(project_id):
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        # 查询当前项目 当前用户对应 的工作简介
        his_intros = session.query(tb_intro.id, tb_intro.work_intro)\
            .filter(and_(tb_intro.staff_id==g.user.id, tb_intro.project_id==project_id))\
            .order_by(desc(tb_intro.create_date)).all()
        return [{"id": i.id, "name": i.work_intro} for i in his_intros]  # 列表生成


    @staticmethod
    def search_his_intros(query_like, project_id):
        # 查询用户的工作简介名称中含query_like的条目的id与work_intro
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        query_like = "%{}%".format(query_like)
        intros = session.query(tb_intro.id, tb_intro.work_intro) \
            .filter(and_(tb_intro.work_intro.like(query_like), tb_intro.staff_id==g.user.id, tb_intro.project_id==project_id)) \
            .order_by(desc(tb_intro.create_date)).all()
        data = [{"id": i[0], "name": i[1]} for i in intros]  # 列表生成
        return data
        # 结构[{},] 示例 [{"id": 9676, "name": '美签项目 自动填表功能技术验证'},]



# @1处的查询sql语句
# SELECT id, work_intro, project_id, work_address, work_property_id
# FROM t_work_introduction
# WHERE (work_intro='东航公务证件管理系统'
#   OR
#       project_id = (
#           SELECT id
#           FROM t_project_summary
#           WHERE project_name='东航公务证件管理系统'
#           LIMIT 1))
#   AND
#       staff_id = 199;