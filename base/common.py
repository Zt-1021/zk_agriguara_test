#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/2 15:46
# @Author　: wanghr


import requests
import json
from base import Log
import traceback

log = Log.TestLog(logger='common').get_log()


def send_http(url, method, headers, data):
    if method == 'POST':
        response = requests.request(url=url, method="POST", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            try:
                response_json = json.loads(response.text)
                return response_json
            except Exception as error:
                log.error(traceback.format_exc())
        else:
            log.error("【FAIL】HTTP请求失败|%s" % str(response))


def login(url,host,name, pwd):
    url = url+"/hkm-auth/server/auth/login"
    payload = {"username": name, "password": pwd}
    headers = {
        'Host': host,
        'Content-Type': 'application/json;charset=UTF-8'
    }
    response = send_http(url=url, method="POST", headers=headers, data=payload)
    print(response)
    if response['success'] == True :
        token = response['data']['token']
        # registname = response['data']['username']
        return token
    else:
        log.error("【FAIL】登录请求失败|%s" % str(response))
        return 0


class ReportBank(object):

    def __init__(self):
        self.default = {"Opt": "query.900", "Args": "", "AdapterType": "sysintergrateuser1", "RowState": "1"}

    def decrypt_str(self, data):
        """
        解密接口
        :return:
        """
        url = "http://223.247.210.27:8082/encrytion/decryptStr"
        headers = {
            'Content-Type': 'text/plain'
        }
        response = send_http(url=url, method="POST", headers=headers, data=data)
        if response['retMsg'] == "成功了":
            return 1
        else:
            log.error("【FAIL】调用接口接口失败|%s" % str(response))
            return 0

    def encode_str(self, data):
        """
        加密接口
        :param data:
        :return:
        """
        url = "http://223.247.210.27:8082/encrytion/encodeStr"
        headers = {
            'Content-Type': 'application/json'
        }
        response = send_http(url=url, method="POST", headers=headers, data=data)
        return response

    def report_bank(self, encode_str, report_type=0):
        """
        发送解密数据到银行接口,返回解密后是否成功
        :param encode_str:
        :param report_type:
        :return:1-成功 0-失败
        """
        self.default['Args'] = encode_str
        if report_type == 0:  # 推送贷款申请
            self.default['Opt'] = "query.900"
        elif report_type == 1:  # 向银行反馈贷款信息
            self.default['Opt'] = "query.901"
        elif report_type == 2:  # 向银行推送逾期信息
            self.default['Opt'] = "query.902"
        else:
            log.error("【FAIL】推送到银行数据类型错误，只允许0，1，2")
            return 0
        url = "http://223.247.210.27:5936/CommonFrontAgent/ReportInfo"
        headers = {
            'Content-Type': 'application/json'
        }
        response = send_http(url=url, method="POST", headers=headers, data=self.default)
        return self.decrypt_str(response)
