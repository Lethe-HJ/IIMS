# # coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from . import Base, metadata
#
#
# class RestAccesslog(Base):
#     __tablename__ = 'rest_accesslog'
#
#     Id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=True, default="NULL")
#     remote_addr = Column(String(255))
#     tm = Column(DateTime)
#     method = Column(String(255))
#     url = Column(String(255))
#     description = Column(String(255), nullable=True, default="NULL")
#     duration = Column(Integer, nullable=True, default=0)
#     status = Column(Integer, nullable=True, default=0)
#     length = Column(Integer, nullable=True, default=0)
#     error_message = Column(String(255))
