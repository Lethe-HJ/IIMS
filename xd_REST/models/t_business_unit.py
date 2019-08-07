# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from xd_REST import db
from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_
from xd_REST import app, cache
from . import Base, metadata

class TBusinessUnit(Base):
    __tablename__ = 't_business_unit'

    id = Column(BIGINT(20), primary_key=True, comment='部门ID:主键')
    business_unit = Column(String(255, 'utf8_croatian_ci'), comment='部门')
    create_date = Column(TIMESTAMP(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"), comment='创建时间')
    parent_business_unit_id = Column(BIGINT(255), comment='父部门:填写部门ID')
    remarks = Column(String(255, 'utf8_croatian_ci'))