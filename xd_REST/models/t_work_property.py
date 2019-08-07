# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from xd_REST import session
from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_
from xd_REST import app, cache
from . import Base, metadata


class TWorkProperty(Base):
    __tablename__ = 't_work_property'

    id = Column(BIGINT(20), primary_key=True, comment='工作性质ID')
    create_date = Column(TIMESTAMP(fsp=6), server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"), comment='创建时间')
    work_property_name = Column(String(255, 'utf8_croatian_ci'), comment='工作性质')
    create_user = Column(BIGINT(20), comment='创建人')
    department = Column(String(255, 'utf8_croatian_ci'), comment='部门')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')

    @staticmethod
    def all_properties():
        """
        查询工作性质
        :return: [{"id": ***, "name": ***}, ... ]
        """
        tb_property = TWorkProperty
        # 查询工作性质
        properties = session.query(tb_property.id, tb_property.work_property_name).all()
        return [{"id": i[0], "name": i[1]} for i in properties]  # 列表生成