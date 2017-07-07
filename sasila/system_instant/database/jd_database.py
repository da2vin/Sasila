#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

reload(sys)
sys.setdefaultencoding('utf-8')

# 创建对象的基类:
Base = declarative_base()


class Process(Base):
    # 表的名字:
    __tablename__ = 'crawler_flow_info'
    # 表的结构:
    collect_token = Column(String(100), primary_key=True)
    customer_id = Column(String(100))
    token_valid_time = Column(Integer)
    token_create_time = Column(Integer)
    status = Column(String(10))
    cookies = Column(String(5000))


class JdDatabase(object):
    def __init__(self):
        # 初始化数据库连接:
        self.engine = create_engine('mysql+mysqlconnector://root:root@192.168.3.210:3306/hiveengine')
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)
        self._create_all()

    def _create_all(self):
        '''
        创建从Base派生的所有表,如果数据表存在则忽视
        :return:
        '''
        Base.metadata.create_all(self.engine)

    def _drop_all(self):
        '''
        删除DB中所有的表
        :return:
        '''
        Base.metadata.drop_all(self.engine)

    def create_session(self):
        return self.DBSession()

    def query_cookie(self, collect_token):
        session = self.DBSession()
        cookies = session.query(Process).filter(Process.collect_token == collect_token).first().cookies
        session.close()
        return cookies

    def update_cookie(self, collect_token, cookies):
        session = self.DBSession()
        session.query(Process).filter(Process.collect_token == collect_token).update({
            Process.cookies: cookies
        })
        session.close()
