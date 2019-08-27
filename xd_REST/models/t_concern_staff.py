# coding: utf-8

from flask import g
from sqlalchemy import Integer, Date, Unicode, Numeric, exc, DateTime, Table
from sqlalchemy import Column, DateTime, String, desc, and_
from . import Base
from .t_work_introduction import TWorkIntroduction as TbIntro
from .t_project_summary import TProjectSummary as TbProject
from .t_staff import TStaff
from xd_REST import session
# from xd_REST.logger import error_log
from datetime import datetime
from . import Base, metadata


class TConcernStaff(Base):
    __tablename__ = 'T_ConcernStaff'

    StaffID = Column(Integer, primary_key=True)
    ConcernIDGroup = Column(Unicode(1000))

    @staticmethod
    def get_his_concern():
        his_concern = session.query(TConcernStaff.ConcernIDGroup).filter_by(StaffID=g.user.ID).first()
        if not his_concern:
            return []
        his_concern = his_concern[0].strip(',').split(',')  # 去掉首尾, 再以,分割成列表
        id_names = session.query(TStaff.ID, TStaff.StaffName).filter(TStaff.ID.in_(his_concern)).all()
        return [{"id": id_name.ID, "name": id_name.StaffName} for id_name in id_names]

    @staticmethod
    def update_concern(concern_li):
        new_concern_li = []
        for i in concern_li:
            id_exist = session.query(TStaff.ID).filter_by(ID=i).first()
            if id_exist:
                new_concern_li.append(str(i))
        new_concern = ",".join(new_concern_li)
        the_concern = session.query(TConcernStaff).filter_by(StaffID=g.user.ID).first()
        the_concern.ConcernIDGroup = new_concern
        session.commit()
        return True
