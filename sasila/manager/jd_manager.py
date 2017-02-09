#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import uuid
import datetime
import json
from sasila.manager.database.jd_database import *
from sasila.imspider.jd_imspider.imspider import JdImSpider

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
        self.imspider = JdImSpider()
        self.imspider.init_pool()

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

    def process_login(self, collect_token, account, password):
        session = self.database.create_session()
        process = session.query(Process).filter(Process.collect_token == collect_token).first()
        if process:
            if datetime.datetime.now() < process.expire_time:
                # collect_token 过期
                pass
            else:
                result = self.imspider.login(account, password, process.process_cookie)
                if result.has_login:
                    return '已经登录'
                else:
                    if result.login_success:
                        session.query(Process).filter(Process.collect_token == collect_token).update({
                            Process.account: account,
                            Process.password: password,
                            Process.process_cookie: cookies
                        })
                        return '登录成功'
                    else:
                        if result.need_sms_captch:
                            session.query(Process).filter(Process.collect_token == collect_token).update({
                                Process.account: account,
                                Process.password: password,
                                Process.process_cookie: cookies
                            })
                            return '需要验证码'
                        else:
                            return '登录失败' + result.message
        else:
            # 没有申请collect_token
            return 'collect_token 无效'

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

# print manager.init_process("xyebank", "毛靖文", "510122198902080290", "13408415919", 0)
#
print manager.process_login('2be44e80-edcd-11e6-9', "13408415919", 'dElete2405')
