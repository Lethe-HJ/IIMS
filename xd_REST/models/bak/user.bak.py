# # coding: utf-8
# from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text
# from sqlalchemy.dialects.mysql.enumerated import ENUM
# from hashlib import md5
# from flask import current_app, g
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
# from xd_REST import db
# from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
# from sqlalchemy import CHAR, Column, DateTime, String
# from sqlalchemy.ext.declarative import declarative_base
# from xd_REST import app, cache
#
# Base = declarative_base()
# metadata = Base.metadata
#
#
# class UUser(Base):
#     __tablename__ = 'u_user'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(10), nullable=False)
#     gender = Column(ENUM('W', 'M'), nullable=False)
#     position = Column(String(20), nullable=False)
#     phone = Column(String(20), nullable=False)
#     email = Column(String(20), nullable=False)
#     password = Column(String(32), nullable=False, server_default=text("'123456'"))
#     token = Column(String(32))
#     avatar = Column(String(50), nullable=False, server_default=text("'/src/images/avatar/default.png'"))
#     last_login = Column(DateTime)
#     modify_time = Column(DateTime)
#     create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
#
    # def init_password(self):
    #     self.device_password = encrypt_oracle(current_app.config.get("INIT_PASSWORD", "xd12345678"),
    #                                           current_app.config.get("AES_KEY", "12345678"))
    #
    # def encode_password(self, password):
    #     # 加密密码
    #     self.device_password = encrypt_oracle(password, current_app.config.get("AES_KEY", "12345678"))
    #
    # def decode_password(self):
    #     # 解密密码
    #     return decrypt_oracle(self.device_password, current_app.config.get("AES_KEY", "12345678"))
    #
    # def verify_password(self, password):
    #     return self.password == password
    #
    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id}).decode('ascii')
    #
    # def save_token(self, id, token):
    #     # query.update({"token": token})  # 使用之前的Basequery 避免重复查询
    #     # db.session.commit()
    #     cache.set(id, token, timeout=3600)
    #
    # @staticmethod
    # def verify_parse_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None  # valId token, but expired
    #     except BadSignature:
    #         return None  # invalId token
    #     # user = db.session.query(UUser).get(data['id'])
    #     return data