#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 导入:
from sqlalchemy import Column, String, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Process(Base):
    # 表的名字:
    __tablename__ = 'process_tbl'
    # 表的结构:
    token = Column(String(20), primary_key=True)
    company_account = Column(String(20))
    name = Column(String(20))
    identity_card_number = Column(String(20))
    cell_phone_number = Column(String(20))


class JdDatabase(object):
    def __init__(self):
        # 初始化数据库连接:
        self.engine = create_engine('mysql+mysqlconnector://root:root@192.168.3.210:3306/jd_manager')
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

    def insert(self, model):
        # 创建session对象:
        session = self.DBSession()
        # 添加到session:
        result = session.add(model)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
        return result

    def query(self, model):
        # 创建session对象:
        session = self.DBSession()
        # 添加到session:
        results = session.query(model).all()
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
        return results

    def update(self, model):
        # 创建session对象:
        session = self.DBSession()
        # 添加到session:
        results = session.query(model).update(model)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
        return results

    def delete(self, model):
        # 创建session对象:
        session = self.DBSession()
        # 添加到session:
        results = session.query(model).delete()
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
        return results


if __name__ == "__main__":
    database = JdDatabase()
    process = Process(token='asdfas', name='ddddddddddddddd')
    database.insert(process)
