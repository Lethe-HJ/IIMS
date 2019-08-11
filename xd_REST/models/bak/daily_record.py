# # coding: utf-8
# from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text, or_, subquery, all_, any_, distinct
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.mysql.enumerated import ENUM
# from flask import current_app, g
# from xd_REST import db
# from . import Base, metadata
# from .project import PProject, PProjectItem, PUserProject
#
#
# class DDailyRecord(Base):
#     __tablename__ = 'd_daily_record'
#
#     id = Column(Integer, primary_key=True)
#     project_id = Column(ForeignKey('p_project.id'), nullable=False, index=True)
#     work_item_id = Column(ForeignKey('p_project_items.id'), nullable=False, index=True)
#     matters = Column(Text, nullable=False)
#     work_date = Column(DateTime, nullable=False)
#     create_time = Column(DateTime, nullable=False)
#     work_hours = Column(Integer, nullable=False)
#     day_in_week = Column(Integer, nullable=False)
#     update_time = Column(DateTime, nullable=False)
#     create_user_id = Column(ForeignKey('u_user.id'), nullable=False, index=True)
#     update_user_id = Column(ForeignKey('u_user.id'), nullable=False, index=True)
#     is_del = Column(Integer, nullable=False)
#
#     create_user = relationship('UUser', primaryjoin='DDailyRecord.create_user_id == UUser.id')
#     project = relationship('PProject')
#     update_user = relationship('UUser', primaryjoin='DDailyRecord.update_user_id == UUser.id')
#     work_item = relationship('PProjectItem')
#
#     @staticmethod
#     def himself_dailys(detail, query):
#         # user_id = g.user.ID
#         user_id = 1
#         data_li = []
#         if query:  # 如果有查询 则优先查询
#             # 从用户的日报中查询 属于指定项目的日报条目
#             # 项目表与工作日报表 联表查询用户创建的条目
#             User_project = db.session.query(DDailyRecord).join(PProject).filter(DDailyRecord.create_user_id==user_id)
#             # 从上述查询中 查询满足项目名或项目别名为query的条目
#             dailys = User_project.filter(or_(PProject.project_alias==query,PProject.project_name==query)).all()
#         else:
#             # 从工作日报表中查询用户的日报记录
#             dailys = db.session.query(DDailyRecord).filter_by(create_user_id=user_id).all()
#         data = {}
#         for i in dailys:
#             data["daily_id"] = i.id
#             data["work_date"] = i.work_date
#             data["matters"] = i.matters
#             if detail:
#                 # 查询这个工作日报条目对应的工作项名称
#                 work_item = db.session.query(PProjectItem).filter_by(id=i.work_item_id).first()
#                 data["work_item"] = work_item.item_name
#                 # 查询当前项目的项目别名
#                 alias = db.session.query(PProject).filter_by(id=i.project_id).first().project_alias
#                 data["alias"] = alias
#                 data["work_hour"] = i.work_hours
#             data_li.append(data)
#         return data_li
#
#     @staticmethod
#     def edit_page_get(daily_id):
#         # try:
#         data = {}
#         # 查询指定的工作日报条目
#         this_daily = db.session.query(DDailyRecord).filter_by(id=daily_id).first()
#         # 如果正在修改的日报不属于当前的用户 则提示
#         # current_user = g.user.ID
#         current_user = 1
#         if this_daily.create_user_id is not current_user:
#             return False, data, "(─.─||| 对不起 无法修改他人创建的日报"
#         data["work_hour"] = this_daily.work_hours
#         data["work_date"] = this_daily.work_date
#         data["matters"] = this_daily.matters
#
#         data["work_item"] = []
#         # 查询当前用户可选的工作项id及工作项名称
#         items = db.session.query(PProjectItem).filter_by(create_user=current_user).all()
#         for item in items:
#             dt = {"id": item.id, "item_name": item.item_name}
#             if item.id is this_daily.work_item_id:  # 将当前日报所属工作项插入到数组头部
#                 data["work_item"].insert(0, dt)
#             else:  # 当前用户可选的其他项目添加到尾部
#                 data["work_item"].append(dt)
#         data["alias"] = []
#         # 子查询 查询当前用户可选的项目id及项目名称
#         subquery = db.session.query(PUserProject.project_id).filter_by(user_id=current_user).subquery()
#         projects = db.session.query(PProject.id, PProject.project_alias).filter(PProject.id==any_(subquery))
#         for project in projects:
#             dt = {"id": project.id, "item_name": project.project_alias}
#             # 将当前日报所属项目插入到数组头部
#             if project.id is this_daily.project_id:
#                 data["alias"].insert(0, dt)
#             else:  # 当前用户可选的其他项目添加到尾部
#                 data["alias"].append(dt)
#         return True, data, "ヾ(Ő∀Ő๑)ﾉ太好了 我把数据带回来了"
#         # except Exception as e:
#         #     return False, data, "ヾﾉ≧∀≦)o死开!" + e.args[0]
#
#     @staticmethod
#     def add_daily(daily):
#         """
#         日报新增
#         :param daily: DDailyRecord对象
#         :return: dst.my_json 字典
#         """
#         # curren_user = g.user.ID
#         curren_user = 1
#         # 查询当前用户可选的所有项目与工作项的搭配
#         projects_and_items = db.session.query(PUserProject.project_id, PUserProject.project_item_id)\
#             .filter_by(user_id=curren_user).all()
#
#         # 过滤
#         projects = set(i[0] for i in projects_and_items)
#         if daily.project_id not in projects:
#             return False, "无此项目或这不是您的项目"
#         items = set((i[1] for i in projects_and_items))
#         if daily.work_item_id not in items:
#             return False, "无此工作项或这不是您的工作项"
#         if (daily.project_id, daily.work_item_id) not in projects_and_items:
#             return False, "该工作项不属于该项目"
#         for project_and_item in projects_and_items:
#             print(project_and_item)
#         return True, "ヾ(Ő∀Ő๑)ﾉ太好了 数据添加成功"
#
#     @staticmethod
#     def update_daily(daily):
#         """
#         日报修改
#         :param daily: DDailyRecord对象
#         :return: dst.my_json 字典
#         """
#         # 查找当前的日报条目
#         this_daily = db.session.query(DDailyRecord).filter_by(id=daily.id).first()
#         # 检查当前的日报是否是当前的用户创建的
#         # current_user = g.user.ID
#         current_user = 1
#         if this_daily.create_user_id is not current_user:
#             return False, "(─.─||| 对不起 无法修改他人创建的日报"
#         this_daily.id = daily.id
#         this_daily.work_date = daily.work_date
#         this_daily.work_hours = daily.work_hours
#         this_daily.project_id = daily.project_id
#         this_daily.work_item_id = daily.work_item_id
#         this_daily.matters = daily.matters
#         db.session.add(this_daily)
#         db.session.commit()
#         return True, "ヾ(Ő∀Ő๑)ﾉ太好了 数据修改完成"
