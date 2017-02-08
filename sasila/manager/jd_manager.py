#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import uuid
import datetime
import json
from sasila.manager.database.jd_database import *

reload(sys)
sys.setdefaultencoding('utf-8')


class JdResponse(object):
    def __init__(self, code, code_description, cellphonenumber, token, message):
        self.code = code
        self.code_description = code_description
        self.data = dict()
        self.data["cellphonenumber"] = cellphonenumber
        self.data["collect_website"] = "JD"
        self.data["supportresetpassword"] = False
        self.data["token"] = token
        self.message = message


class JdManager(object):
    def __init__(self):
        self.database = JdDatabase()

    def init_process(self, company_account, name, identity_card_number, cell_phone_number, process_code):
        '''
        申请认证令牌
        :param company_account:
        :param name:
        :param identity_card_number:
        :param cell_phone_number:
        :return:
        '''
        if self._validate_data(company_account, name, identity_card_number, cell_phone_number):
            collect_token = self._create_collect_token()
            start_time = datetime.datetime.now()
            expire_time = start_time + datetime.timedelta(minutes=10)
            new_process = Process(
                    start_time=start_time,
                    expire_time=expire_time,
                    collect_token=collect_token,
                    company_account=company_account,
                    name=name,
                    identity_card_number=identity_card_number,
                    cell_phone_number=cell_phone_number,
                    process_code=0
            )
            session = self.database.create_session()
            session.add(new_process)
            session.commit()
            session.close()

            return json.dumps(
                    JdResponse(0, "APPLICANT_SUCCESS", cell_phone_number, collect_token, "成功").__dict__).decode(
                    "unicode-escape")
        else:
            pass

    def _validate_data(self, company_account, name, identity_card_number, cell_phone_number):
        '''
        校验数据
        :param company_account:
        :param name:
        :param identity_card_number:
        :param cell_phone_number:
        :return:
        '''
        return True

    def _create_collect_token(self):
        token = str(uuid.uuid1())
        return token


manager = JdManager()
print manager.init_process("xyebank", "毛靖文", "510122198902080290", "13408415919", 0)
