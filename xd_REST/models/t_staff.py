# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from xd_REST import db
from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_
from xd_REST import app, cache
from . import Base, metadata
from .t_business_unit import TBusinessUnit
from xd_REST.logger import error_log


class TStaff(Base):
    __tablename__ = 't_staff'

    id = Column(BIGINT(20), primary_key=True, comment='人员主键id')
    staff_name = Column(String(100, 'utf8_croatian_ci'), unique=True, comment='员工的名字')
    password = Column(String(255, 'utf8_croatian_ci'), comment='密码 注:主要用于登录时 填写的密码')
    classifiation = Column(String(255, 'utf8_croatian_ci'), comment='人员组 注:部门下面的组  如:基础组,卡本柜组,研发二组')
    department = Column(String(255, 'utf8_croatian_ci'), comment='部门')
    sex = Column(String(10, 'utf8_croatian_ci'), comment='性别ID 外键:t_sex(id)')
    staff_code = Column(String(255, 'utf8_croatian_ci'), comment='员工code 注:员工代表本条数据，用于前端显示而非显示id')
    staff_phone = Column(String(255, 'utf8_croatian_ci'), comment='员工的电话')
    position = Column(String(255, 'utf8_croatian_ci'), comment='职位')
    create_user = Column(BIGINT(20), comment='创建用户ID 外键:t_sys_admin(id)')
    serial_num = Column(BIGINT(11), comment='人员序号')
    isdelete = Column(BIGINT(11), comment='是否删除 0:否 1:是/假删')
    create_date = Column(TIMESTAMP(fsp=6), server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"), comment='创建日期')
    staff_status = Column(String(10, 'utf8_croatian_ci'), comment='人员状态 从字典表获取人员状态t_dict(id)')
    is_update = Column(BIGINT(11), comment='是否可修改(1:可修改 null:不可修改)')
    business_unit_id = Column(ForeignKey('t_business_unit.id', ondelete='CASCADE'), index=True, comment='部门 外键:t_businessunit(id)')
    json = Column(JSON, comment='JSON类型用于人员后续扩展开发')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')

    business_unit = relationship('TBusinessUnit')

    def init_password(self):
        self.device_password = encrypt_oracle(current_app.config.get("INIT_PASSWORD", "xd12345678"),
                                              current_app.config.get("AES_KEY", "12345678"))

    def encode_password(self, password):
        # 加密密码
        self.device_password = encrypt_oracle(password, current_app.config.get("AES_KEY", "12345678"))

    def decode_password(self):
        # 解密密码
        return decrypt_oracle(self.device_password, current_app.config.get("AES_KEY", "12345678"))

    def verify_password(self, password):
        return self.password == password

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    def save_token(self, id, token):
        # query.update({"token": token})  # 使用之前的Basequery 避免重复查询
        # db.session.commit()
        cache.set(id, token, timeout=3600)

    @staticmethod
    def verify_parse_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valId token, but expired
        except BadSignature:
            return None  # invalId token
        # user = db.session.query(UUser).get(data['id'])
        return data