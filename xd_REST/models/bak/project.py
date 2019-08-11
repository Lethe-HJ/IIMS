# # coding: utf-8
# from sqlalchemy.orm import relationship
# from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text
# from sqlalchemy.dialects.mysql.enumerated import ENUM
#
# from flask import current_app, g
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
# from xd_REST import db
# from xd_REST.libs.aes import encrypt_oracle, decrypt_oracle
# from sqlalchemy import CHAR, Column, DateTime, String, or_
# from xd_REST import app, cache
# from . import Base, metadata
#
#
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
#     def init_password(self):
#         self.device_password = encrypt_oracle(current_app.config.get("INIT_PASSWORD", "xd12345678"),
#                                               current_app.config.get("AES_KEY", "12345678"))
#
#     def encode_password(self, password):
#         # 加密密码
#         self.device_password = encrypt_oracle(password, current_app.config.get("AES_KEY", "12345678"))
#
#     def decode_password(self):
#         # 解密密码
#         return decrypt_oracle(self.device_password, current_app.config.get("AES_KEY", "12345678"))
#
#     def verify_password(self, password):
#         return self.password == password
#
#     def generate_auth_token(self, expiration=600):
#         s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
#         return s.dumps({'id': self.id}).decode('ascii')
#
#     def save_token(self, id, token):
#         # query.update({"token": token})  # 使用之前的Basequery 避免重复查询
#         # db.session.commit()
#         cache.set(id, token, timeout=3600)
#
#     @staticmethod
#     def verify_parse_token(token):
#         s = Serializer(app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None  # valId token, but expired
#         except BadSignature:
#             return None  # invalId token
#         # user = db.session.query(UUser).get(data['id'])
#         return data
#
# class PProject(Base):
#     __tablename__ = 'p_project'
#
#     id = Column(Integer, primary_key=True)
#     type_id = Column(String(50))
#     s_number = Column(String(50), nullable=False)
#     project_name = Column(String(50), nullable=False)
#     project_alias = Column(String(50), nullable=False)
#     classifiation = Column(String(50))
#     project_number = Column(String(50))
#     create_time = Column(DateTime, nullable=False)
#     create_user = Column(ForeignKey('u_user.id'), nullable=False, index=True)
#     project_manager = Column(String(50))
#     product_model = Column(String(50))
#     oa_order = Column(String(50))
#     is_del = Column(Integer)
#     update_time = Column(DateTime)
#     update_user = Column(ForeignKey('u_user.id'), index=True)
#     project_status = Column(String(50))
#     remarks = Column(String(50))
#     entering_time = Column(DateTime)
#     status = Column(String(50))
#     lead_party = Column(String(50))
#     end_time = Column(DateTime)
#
#     u_user = relationship('UUser', primaryjoin='PProject.create_user == UUser.id')
#     u_user1 = relationship('UUser', primaryjoin='PProject.update_user == UUser.id')
#
#
#
# class PProjectItem(Base):
#     __tablename__ = 'p_project_items'
#
#     id = Column(Integer, primary_key=True)
#     project_id = Column(ForeignKey('p_project.id'), nullable=False, index=True)
#     create_user = Column(ForeignKey('u_user.id'), nullable=False, index=True)
#     item_name = Column(String(50), server_default=text("'其它'"))
#     item_description = Column(Text, nullable=True)
#     work_addr = Column(String(50), nullable=False)
#     work_nature = Column(String(50), nullable=False)
#     create_time = Column(DateTime, nullable=True)
#     start_time = Column(DateTime)
#     end_time = Column(DateTime)
#     remark = Column(Text, nullable=True)
#
#     u_user = relationship('UUser')
#     project = relationship('PProject')
#
#     @staticmethod
#     def himself_items(detail, query):
#         # user_id = g.user.ID
#         user_id = 1
#         data_li = []
#         if query:  # 如果有查询 则优先查询
#             items = db.session.query(PProjectItem).filter_by(item_name=query).all()
#         else:
#             items = db.session.query(PProjectItem).filter_by(create_user=user_id).all()
#
#         for i in items:
#             print(i.id)
#             data = {}
#             data["id"] = i.id
#             data["work_item"] = i.item_name
#             if detail:
#                 data["work_addr"] = i.work_addr
#                 data["work_nature"] = i.work_nature
#                 data["remark"] = i.remark
#                 data["alias"] = []
#                 # 在人员项目关联表中查找用户关联的项目的记录
#                 project_li = db.session.query(PUserProject).filter_by(user_id=user_id).all()
#                 ids = []
#                 for project in project_li:
#                     ids.append(project.project_id)
#                 for id in set(ids):
#                     # 根据id在项目表中查找条目
#                     sub_project = db.session.query(PProject).filter_by(id=id).first()
#                     data["alias"].append({"id": id, "alias": sub_project.project_alias})
#             else:
#                 data["alias"] = db.session.query(PProject).filter_by(id=i.project_id).first().project_alias
#             data_li.append(data)
#         return data_li
#
#     @staticmethod
#     def add_item(item):
#         db.session.add(item)
#         db.session.commit()
#
#
#     @staticmethod
#     def edit_item(item, item_id):
#         this_item = db.session.query(PProjectItem).filter_by(id=item_id).first()
#         this_item.work_addr = item.work_addr
#         this_item.work_nature = item.work_nature
#         this_item.project_id = item.project_id
#         this_item.item_name = item.item_name
#         this_item.remark = item.remark
#         db.session.add(this_item)
#         db.session.commit()
#
#
# class PUserProject(Base):
#     __tablename__ = 'p_user_project'
#     __table_args__ = (
#         db.Index('UserId_ProjectId_ProjectItemId', 'user_id', 'project_id', 'project_item_id'),
#     )
#
#     user_id = Column(db.ForeignKey('u_user.id'), nullable=False)
#     id = Column(db.Integer, primary_key=True)
#     project_id = Column(db.ForeignKey('p_project.id'), nullable=False, index=True)
#     project_item_id = Column(db.ForeignKey('p_project_items.id'), nullable=False, index=True)
#
#     project = relationship('PProject', primaryjoin='PUserProject.project_id == PProject.id', backref='p_user_projects')
#     project_item = relationship('PProjectItem', primaryjoin='PUserProject.project_item_id == PProjectItem.id', backref='p_user_projects')
#     user = relationship('UUser', primaryjoin='PUserProject.user_id == UUser.id', backref='p_user_projects')