#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')


class JdResponse(object):
    def __init__(self):
        self.code = None
        self.code_description = None
        self.data = dict()
        self.data["cellphonenumber"] = None
        self.data["collect_website"] = None
        self.data["supportresetpassword"] = None
        self.data["token"] = None
        self.message = None


class JdManager(object):
    def __init__(self):
        self.process_dict = dict()

    def init_process(self, company_account, name, identity_card_number, cell_phone_number):
        '''
        申请认证令牌
        :param company_account:
        :param name:
        :param identity_card_number:
        :param cell_phone_number:
        :return:
        '''
        if self._validate_data(company_account, name, identity_card_number, cell_phone_number):
            token = self._create_token()
            self.process_dict[token] = None
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

    def _create_token(self):
        token = str(uuid.uuid1())
        return token
