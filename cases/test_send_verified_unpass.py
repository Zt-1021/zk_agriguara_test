#!/usr/bin/python3.8
# -*- coding:utf-8 -*-

"""
测试发送待核验订单，核验不通过
小程序发送订单->web后台待核验主体列表
"""
# 解决uncode编码警告：在unicode等价比较中，把两个参数同时转换为unicode编码失败。中断并认为他们不相等。
#
# windows下的字符串str默认编码是ascii，而python编码是utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pytest
import time
from cases import send_request
from base import Db
from base import Log
from base import common
from time import sleep


log = Log.TestLog(logger='test_send_').get_log()

odb = Db.OperationDb()  # 实例化数据库操作类


@pytest.mark.test_send_verified_unpass
class TestSendVerified(object):
    def test_create_order(self,set_global_data):
        log.info("======【流程3】调用小程序接口发送待核验数据======")
        result_mini_program = send_request.send_order_by_mini_program("3")
        result_cust_id = send_request.get_cust_id(result_mini_program)

        sleep(1)
        result_obd = odb.select_one('SELECT * FROM t_agriguarantee_order WHERE CUSTID="%s"' % str(result_cust_id))
        set_global_data("order_isblcak",result_obd['data']['ORDER_ISBLACK'])
        if result_obd['code'] == "0000":  # 查询成功
            pass
        else:
            assert 0, "【FAIL】查询t_agriguarantee_order表数据失败"

        set_global_data("CUST_NAME", send_request.param_save_order['CUST_NAME'])
        set_global_data("CUST_IDENTITY_CARD", send_request.param_save_order['CUST_IDENTITY_CARD'])
        set_global_data("CUST_HOME_ADDRESS", send_request.param_save_order['CUST_HOME_ADDRESS'])
        set_global_data("ORDERID", result_obd['data']['ORDERID'])

    def test_order_isblack(self,begin,get_global_data):
        """
        检查ORDER_ISBLACK字段状态
        :return:
        """
        EXPECT_ORDER_ISBLACK = "1"
        order_isblcak = get_global_data("order_isblcak")

        msg = "【检查点1】t_agriguarantee_order表ORDER_ISBLACK字段状态正确，预期是【%s】，实际是【%s】" \
              % (str(EXPECT_ORDER_ISBLACK), str(order_isblcak))
        log.info(msg)
        assert order_isblcak == EXPECT_ORDER_ISBLACK, msg

    def test_check_remark_on_verified_page(self,get_global_data):
        """
        检查待核验主体页面是否有该数据
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/getPassOrderList"
        payload = {"custIdentityCard":"", "custName": "", "loanAmountOrder": "", "orderCity": "", "orderCounty": "('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')",
                    "orderCreateTimeEnd": "", "orderCreateTimeOrder": "desc", "orderCreateTimeStart": "", "orderIsblack": "(1)",
                    "orderPrepariedTimeEnd": "", "orderPrepariedTimeStart": "", "orderTown": "", "pageNum": 1, "pageSize": 10,
                    "registerName": "18226604614"}
        payload['custIdentityCard'] = get_global_data("CUST_IDENTITY_CARD")  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            # set_global_data("verified_data", response)
            msg = "【检查点2】待核验主体中存在订单【%s】数据" % str(get_global_data("ORDERID"))
            log.info(msg)
            assert response['data']['content'][0]['orderId'] == get_global_data("ORDERID"), msg
        else:
            log.error("【FAIL】待核验主体页面查询接口调用失败|%s" % str(response))
            assert 0

    def test_request_revokepaas_order(self,get_global_data):
        """
        待核验主体提交不通过请求
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/h/hkm-service/hkm/revokePaasOrder"
        payload = {"agriobjCorpnTp": "","busEntityLevel": "","busEntityType": "","busLicenseNo": "","businessType": "1",
                   "createTime": time.time(),"currentAddrDistrict": "","currentAddrProvince": "","currentAddrTown": "","custName": get_global_data("CUST_NAME"),
                    "financialSubsidyAmt": "","financialSupportAmt": "","grainGrowerAddr": get_global_data("CUST_HOME_ADDRESS"),"idInvalidDt": "2006.05.29-2026.05.29","isAgriculturalIns": "",
                    "isPartyMember": "","isQualityCertification": "","isRegistered": "","isRegisteredTrademark": "","list": [],"loanIdNo": get_global_data("CUST_IDENTITY_CARD"),
                    "loanName": get_global_data("CUST_NAME"),"loanSupportAmt": "","loansubAddrCity": "","loansubAddrDistrict": "","loansubAddrProvince": "","loansubAddrTown": "",
                    "operator": "吴杰","operatorAccount": "wuj","opestaModelStatus": "","orderDesc": "自动化测试不通过","orderId": get_global_data("ORDERID"),"orderIsblack": "2",
                    "orderRemarkid": "F0DF37D5-D79A-4189-9AE4-C19C8ECACFAE","other": "测试Add","tableImportType": "2","totalRevenueYear": "",}

        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        msg = "【检查点3】订单【%s】核验不通过" % str(get_global_data("ORDERID"))
        log.info(msg)
        assert response['msg'] == "退回项目成功！", msg

    def test_data_getNoPassOrderList(self,get_global_data):
        """
        检查未通过主体存在有数据
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/getNoPassOrderList"
        payload = {"custIdentityCard": get_global_data("CUST_IDENTITY_CARD"),"custName": get_global_data("CUST_NAME"),"loanAmountOrder": "","noPassType": "","orderBank": "","orderCity": "",
                    "orderCounty": "('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')",
                    "orderCreateTimeEnd": "","orderCreateTimeOrder": "desc","orderCreateTimeStart": "","orderPrepariedTimeEnd": "","orderPrepariedTimeStart": "",
                    "orderTown": "","pageNum": 1,"pageSize": 10,"registerName": "wuj","sourceType": ""}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            msg = "【检查点4】未通过主体中存在订单【%s】数据" % str(get_global_data("ORDERID"))
            log.info(msg)
            assert response['data']['content'][0]['orderid'] == get_global_data("ORDERID"), msg
        else:
            log.error("【FAIL】有效需求主体页面查询接口调用失败|%s" % str(response))
            assert 0
