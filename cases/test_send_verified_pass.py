#!/usr/bin/python3.8
# -*- coding:utf-8 -*-

"""
测试发送待核验订单，核验通过
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


@pytest.mark.test_send_verified_pass
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
        set_global_data("CUST_ID", result_cust_id)
        set_global_data("ORDER_PHONE", send_request.param_save_order['ORDER_PHONE'])
        set_global_data("CUST_HOME_ADDRESS", send_request.param_save_order['CUST_HOME_ADDRESS'])
        set_global_data("ORDERID", result_obd['data']['ORDERID'])
        set_global_data("ORDERNO", result_obd['data']['ORDER_NO'])
        set_global_data("ORDER_COUNTRY", result_obd['data']['ORDER_COUNTY'])

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

    def test_check_remark_on_verified_page(self,set_global_data,get_global_data):
        """
        检查待核验主体页面是否有该数据
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/getPassOrderList"
        payload = {"custIdentityCard":"", "custName": "", "loanAmountOrder": "", "orderCity": "", "orderCounty": "('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')",
                    "orderCreateTimeEnd": "", "orderCreateTimeOrder": "desc", "orderCreateTimeStart": "", "orderIsblack": "(1)",
                    "orderPrepariedTimeEnd": "", "orderPrepariedTimeStart": "", "orderTown": "", "pageNum": 1, "pageSize": 10,
                    "registerName": "18226604614"}
        payload['custIdentityCard'] = get_global_data("CUST_IDENTITY_CARD")  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'token': get_global_data('token_wuj'),
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

    def test_request_add_order_remark_page(self,get_global_data):
        """
        待核验主体提交核验请求
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/addOrderRemark"
        payload = {"businessType":"1","loanSupportAmt":"","isRegisteredTrademark":"","financialSupportAmt":"","loansubAddrProvince":"",
                   "loansubAddrCity":"","loansubAddrDistrict":"","loansubAddrTown":"","busEntityLevel":"","busEntityType":"","busLicenseNo":"",
                   "opestaModelStatus":"","isPartyMember":"","other":"测试Add","grainGrowerAddr":get_global_data("CUST_HOME_ADDRESS"),
                   "isQualityCertification":"","isAgriculturalIns":"","financialSubsidyAmt":"","agriobjCorpnTp":"","isRegistered":"",
                   "totalRevenueYear":"","list":[],"tableImportType":"2","orderRemarkid":"11553F28-DA4C-4DCE-80FE-06D64FEF23BE",
                   "orderId":get_global_data("ORDERID"),"operator":"吴杰","idInvalidDt":"2006.05.29-2026.05.29",
                   "currentAddrProvince":"","currentAddrDistrict":"","currentAddrTown":"","operatorAccount":"wuj","loanName":get_global_data("CUST_NAME"),
                   "loanIdNo":get_global_data("CUST_IDENTITY_CARD"),"createTime":time.time(),"custName":get_global_data("CUST_NAME")}

        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'token': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        msg = "【检查点3】订单【%s】核验通过" % str(get_global_data("ORDERID"))
        log.info(msg)
        assert response['code'] == 1, msg

    def test_data_getPassOrderList(self,get_global_data):
        """
        检查有效需求主体存在有数据
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/getPassOrderList"
        payload = {"orderIsblack":"(3,4)","custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')",
                   "orderTown":"","orderCity":"","registerName":"18226604614","custIdentityCard":"632222194305296807","sourceType":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","dictItemCode":""}
        payload['custIdentityCard'] = get_global_data("CUST_IDENTITY_CARD")  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            msg = "【检查点4】有效需求主体中存在订单【%s】数据" % str(get_global_data("ORDERID"))
            log.info(msg)
            assert response['data']['content'][0]['orderId'] == get_global_data("ORDERID"), msg
        else:
            log.error("【FAIL】有效需求主体页面查询接口调用失败|%s" % str(response))
            assert 0

    def test_data_queryProjectTodoList(self,get_global_data):
        """
        检查待处理项目存在有数据且有处理标识
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/queryProjectTodoList"
        payload = {"orderIsblack":"(12)","custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')",
                   "orderTown":"","orderCity":"","registerName":"18226604614","custIdentityCard":"140881195104112898","sourceType":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":""}
        payload['custIdentityCard'] = get_global_data("CUST_IDENTITY_CARD")  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1140',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            order_id = response['data']['content'][0]['orderId']  # 订单编号
            # set_global_data("order_no", response['data']['content'][0]['orderNo'])
            # global ORDER_NO
            # ORDER_NO = response['data']['content'][0]['orderNo']

            if order_id == get_global_data("ORDERID"):
                msg = "【检查点5】待处理项目中存在订单【%s】和处理标识，预期结果【12】实际结果【%s】" % (
                order_id, str(response['data']['content'][0]['orderStatus']))
                log.info(msg)
                assert response['data']['content'][0]['orderStatus'] == '12', msg
            else:
                log.error("【FAIL】订单编号不匹配，接口订单编号为%s,数据表中订单编号为%s" % (str(order_id), str(get_global_data("ORDERID"))))
        else:
            log.error("【FAIL】待通过项目页面查询接口调用失败|%s" % str(response))
            assert 0

    def test_get_id_by_order_no(self,get_global_data):
        """
        通过orderNo获取身份证、姓名、订单号
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/details/getIdByOrderNo"
        payload = {'orderNo': get_global_data("ORDERNO")}
        # payload['orderNo'] = get_global_data('token_wuj')  # 替换OrderNo
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '37',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点6】待处理详情页面通过getIdByOrderNo接口获取成功"
            log.info(msg)
            assert response['data']['orderId'] == get_global_data("ORDERID"), msg
        else:
            log.error("【FAIL】待处理详情页面getIdByOrderNo调用失败|%s" % str(response))
            assert 0

    def test_query_commercial_information(self,get_global_data):
        """
        查询审核页面贷款主体信息，申请人+工商主体名称
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/common/queryCommercialInformation"
        payload = {"loanName": get_global_data("CUST_NAME"), "loanIdNo": get_global_data("CUST_IDENTITY_CARD"), "orderId": get_global_data("ORDERID")}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            busEntityName = [data['busEntityName'] for data in response['data']]  # 贷款主体名称列表
            if busEntityName[0] == get_global_data("CUST_NAME"):
                msg = "【检查点7】审核页面贷款主体接口queryCommercialInformation返回首个数据是申请人【%s】"\
                  % str(busEntityName[0])
                log.info(msg)
                assert busEntityName[0] == get_global_data("CUST_NAME"), msg
            else:
                log.error("【FAIL】待处理详情页面queryCommercialInformation返回数据错误|%s" % str(response))
                assert 0
            log.info(msg)
            assert busEntityName, msg
        else:
            log.error("【FAIL】待处理详情页面queryCommercialInformation调用失败|%s" % str(response))
            assert 0

    def test_get_user_bank(self,get_global_data):
        """
        查询审核页面贷款银行
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/bank/queryLoanBankBySpecialOrderNo"
        payload = {"countyCode": get_global_data("ORDER_COUNTRY"), "orderNo": get_global_data("ORDERNO"), "registerName": "18226604614"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            bankName = [data['bankName'] for data in response['data']]  # 贷款名称列表
            result_BANKNAME = odb.select_all('SELECT BANK_NAME from t_agriguarantee_bank where BANK_CODE in (select BANK_CODE from t_agriguarantee_bank_region where COUNTY_CODE in (%s,000000000000) and ENABLE = "1" and USER_TYPE in ("2","3"))' % str(get_global_data("ORDER_COUNTRY")))
            BANKNAME = [data['BANK_NAME'] for data in result_BANKNAME['data']]
            if set(bankName) == set(BANKNAME):
                msg = "【检查点8】审核页面银行接口getUserBank返回贷款银行信息【%s】" % str(bankName)
                log.info(msg)
                assert 1, msg
            else:
                log.error("【FAIL】审核页面银行返回数据错误")
        else:
            log.error("【FAIL】待处理详情页面getUserBank调用失败|%s" % str(response))

    def test_pass_guarantee(self,get_global_data):
        """
        提交审核（个人+邮储银行+贷款10w+利率1%）--> 线上项目
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/passGuarantee"
        payload = {"loanApplicantId":get_global_data("CUST_IDENTITY_CARD"),"loanBankCode":"403361000006","loanGuaranteeAmount":"10",
                   "loanGuaranteeRate":"0.01","paymentType":"0","orderId":get_global_data("ORDERID"),
                   "orderNo":get_global_data("ORDERNO"),"loanApplicantPhone":get_global_data("ORDER_PHONE"),
                   "loanApplicantIdcard":get_global_data("CUST_IDENTITY_CARD"),"loanSubmmitter":"wuj","custName":get_global_data("CUST_NAME"),
                   "countyCode":get_global_data("ORDER_COUNTRY"),"loanApplicantName":get_global_data("CUST_NAME"),"busEntityType":"1"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点9】审核页面提交订单【%s】审核通过" % get_global_data("ORDERID")
            log.info(msg)
            assert 1, msg
        else:
            log.error("【FAIL】审核页面审核接口passGuarantee调用失败|%s" % str(response))
            assert 0


    def test_query_to_send_project_online(self,get_global_data):
        """
        检查线上审核项目中是否有提交审核的数据
        :param get_global_data:
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/queryToSendProject"
        payload = {"pageNum":1,"pageSize":10,"loanApplicantName":get_global_data("CUST_NAME"),"loanApplicantIdcard":get_global_data("CUST_IDENTITY_CARD"),"paymentTypeCode":"",
                   "loanBankCode":"","personalType":"1","orderStatus":"7"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点10】线上项目页面存在订单【%s】数据" % get_global_data("ORDERID")
            log.info(msg)
            assert response['data']['content'][0]['loanApplicantPhone'] == get_global_data("ORDER_PHONE"), msg
        else:
            log.error("【FAIL】线上项目页面接口queryToSendProject调用失败|%s" % str(response))
            assert 0

    def test_modify_to_send_project(self,get_global_data):
        """
        修改担保信息（个人+工商）
        :param get_global_data:
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/modifyToSendProject"
        payload = {"busEntityType": "2","countyCode": get_global_data("ORDER_COUNTRY"),"custName": get_global_data("CUST_NAME"),"loanApplicantId": get_global_data("CUST_IDENTITY_CARD"),
                   "loanApplicantName": get_global_data("CUST_NAME"),"loanBankCode": "102361000242","loanGuaranteeAmount": "22","loanGuaranteeRate": "0.003",
                   "loanSubmmitter": "chiq","orderNo": get_global_data("ORDERNO"),"paymentType": "0"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_chiq'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点11】修改担保信息修改成功【%s】数据" % get_global_data("ORDERID")
            log.info(msg)
            assert 1, msg
        else:
            log.error("【FAIL】修改担保信息modifyToSendProject调用失败|%s" % str(response))
            assert 0

    def test_query_to_send_project_offline(self,set_global_data,get_global_data):
        """
        检查线下审核项目中是否有提交审核的数据
        :param get_global_data:
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/queryToSendProject"
        payload = {"pageNum":1,"pageSize":10,"loanApplicantName":get_global_data("CUST_NAME"),"loanApplicantIdcard":get_global_data("CUST_IDENTITY_CARD"),"paymentTypeCode":"",
                   "loanBankCode":"","personalType":"2","orderStatus":"7"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点12】线下项目页面存在订单【%s】数据" % get_global_data("ORDERID")
            log.info(msg)
            assert response['data']['content'][0]['loanApplicantPhone'] == get_global_data("ORDER_PHONE"), msg
        else:
            log.error("【FAIL】线下项目页面接口queryToSendProject调用失败|%s" % str(response))
            assert 0

    def test_generate_batch_project(self,get_global_data):
        """
        检查批量生成接口
        :param get_global_data:
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/generateBatchProject"
        payload = {"loanSubmmitter": "chiq"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_chiq'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        msg = "【检查点13】线下项目页面订单【%s】批量生成数据" % get_global_data("ORDERID")
        log.info(msg)
        assert response['code'] == 1, msg

    def test_query_bank_progress(self,get_global_data):
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/queryBankProgress"
        payload = {"bankCode": "","classCode": "","loanApplicantIdcard": "","loanApplicantName": get_global_data("CUST_NAME"),"orderStatus": "","pageNum": 1,
                   "pageSize": "10","paymentTypeCode": "","sourceType": ""}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_chiq'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        msg = "【检查点14】已发送项目页面存在订单%s" % get_global_data("ORDERID")
        log.info(msg)
        assert response['data']["content"][0]["orderStatusName"] == "担保已发送", msg


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-ra", "test_send_verified_pass.py"])