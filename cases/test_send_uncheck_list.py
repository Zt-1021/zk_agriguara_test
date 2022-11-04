#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/1 0:33
# @Author　: wanghr
"""
测试发送待核验流程
小程序发送点订单->web后台未通过主体中有复核标识
"""
# 解决uncode编码警告：在unicode等价比较中，把两个参数同时转换为unicode编码失败。中断并认为他们不相等。
#
# windows下的字符串str默认编码是ascii，而python编码是utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pytest
from cases import send_request
from base import Db
from base import Log
from base import common
from time import sleep


log = Log.TestLog(logger='test_send_uncheck_list').get_log()

odb = Db.OperationDb()  # 实例化数据库操作类

# 测试预期结果
EXPECT_ORDER_ISBLACK = "0"
EXPECT_ORDER_DESC = "年龄大于64岁"
EXPECT_NO_PASS_TYPE = "applicant_age"
ORDER_NO = ""
CUST_ID = ""  # 用户id
CUST_NAME = ""  # 姓名
ORDER_ID = ""  # 订单号
ORDER_PHONE = ""  # 手机号


@pytest.mark.test_send_uncheck_list
class TestSendUncheckList(object):

    def create_order(self):
        # 执行前置操作
        log.info("======【流程2】调用小程序接口发送未通过主体(年龄不符)+有复核标识数据======")
        result_mini_program = send_request.send_order_by_mini_program("0")  # 调用小程序接口发送初筛不通过数据
        result_cust_id = send_request.get_cust_id(result_mini_program)  # 通过身份证号获取cust id

        sleep(1)
        result_obd = odb.select_one('SELECT * FROM t_agriguarantee_order WHERE CUSTID="%s"' % str(result_cust_id))
        if result_obd['code'] == "0000":  # 查询成功
            pass
        else:
            assert 0, "【FAIL】查询t_agriguarantee_order表数据失败"


    def test_order_isblack(self):
        """
        检查ORDER_ISBLACK字段状态
        :return:
        """
        msg = "【检查点1】t_agriguarantee_order表ORDER_ISBLACK字段状态正确，预期是【%s】，实际是【%s】" \
              % (str(EXPECT_ORDER_ISBLACK), str(result_obd['data']['ORDER_ISBLACK']))
        log.info(msg)
        assert result_obd['data']['ORDER_ISBLACK'] == EXPECT_ORDER_ISBLACK, msg

    def test_order_desc(self):
        """
        检查ORDER_DESC字段状态
        :return:
        """
        msg = "【检查点1】t_agriguarantee_order表ORDER_DESC字段状态正确，预期是【%s】，实际是【%s】" \
              % (str(EXPECT_ORDER_DESC), str(result_obd['data']['ORDER_DESC']))
        log.info(msg)
        assert result_obd['data']['ORDER_DESC'] == EXPECT_ORDER_DESC, msg

    def test_no_pass_type(self):
        """
        检查NO_PASS_TYPE字段状态
        :return:
        """
        msg = "【检查点1】t_agriguarantee_order表NO_PASS_TYPE字段状态正确，预期是【%s】，实际是【%s】" \
              % (str(EXPECT_NO_PASS_TYPE), str(result_obd['data']['NO_PASS_TYPE']))
        log.info(msg)
        assert result_obd['data']['NO_PASS_TYPE'] == EXPECT_NO_PASS_TYPE, msg

    def test_fuhe_remark_on_no_pass_page(self, set_global_data, get_global_data):
        """
        检查未通过主体页面该数据是否有复核标识
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/getNoPassOrderList"
        payload = {"custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')","orderTown":"","orderCity":"","registerName":"wuj","custIdentityCard":"510402194102155605","sourceType":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","noPassType":""}
        payload['custIdentityCard'] = result_mini_program  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            set_global_data("fuhe_remark", response)
            msg = "【检查点2】未通过主体中存在复核标识，预期结果【1】实际结果【%s】" % str(response['data']['content'][0]['sourceType'])
            log.info(msg)
            assert response['data']['content'][0]['sourceType'] == '1', msg

        else:
            log.error("【FAIL】未通过主体页面查询接口调用失败|%s" % str(response))
            assert 0

    def test_request_fuhe_from_no_pass_page(self, get_global_data):
        """
        检查未通过主体页面提交复核请求
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/order/recheck/passRecheckOrder"
        payload = {"orderid": "","custName": ""}
        response = get_global_data('fuhe_remark')
        payload['orderid'] = response['data']['content'][0]['orderid']  # 替换订单编号
        payload['custName'] = response['data']['content'][0]['custName']  # 替换姓名
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        msg = "【检查点3】订单【%s】提交复核成功" % str(payload['orderid'])
        log.info(msg)
        assert response['code'] == 1, msg

    def test_data_on_pass_page(self, get_global_data):
        """
        检查有效需求主体存在有数据
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/getPassOrderList"
        payload = {"orderIsblack":"(3,4)","custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')","orderTown":"","orderCity":"","registerName":"wuj","custIdentityCard":"632222194305296807","sourceType":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","dictItemCode":""}
        payload['custIdentityCard'] = result_mini_program  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            order_id = response['data']['content'][0]['orderId']  # 订单编号
            msg = "【检查点4】有效需求主体中存在订单【%s】数据" % str(order_id)
            log.info(msg)
            assert response['status'] == "success", msg
        else:
            log.error("【FAIL】未通过主体页面查询接口调用失败|%s" % str(response))
            assert 0

    def test_data_on_project_to_do_page(self, set_global_data, get_global_data):
        """
        检查待处理项目存在有数据且有处理标识
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/queryProjectTodoList"
        payload = {"orderIsblack":"(12)","custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')","orderTown":"","orderCity":"","registerName":"wuj","custIdentityCard":"140881195104112898","sourceType":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":""}
        payload['custIdentityCard'] = result_mini_program  # 替换身份证号
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
            global ORDER_NO
            ORDER_NO = response['data']['content'][0]['orderNo']
            msg = "【检查点5】待处理项目中存在订单【%s】和处理标识，预期结果【12】实际结果【%s】" % (order_id, str(response['data']['content'][0]['orderStatus']))
            log.info(msg)
            assert response['data']['content'][0]['orderStatus'] == '12', msg
        else:
            log.error("【FAIL】待通过项目页面查询接口调用失败|%s" % str(response))
            assert 0

    def test_get_id_by_order_no(self, get_global_data):
        """
        通过orderNo获取身份证、姓名、订单号
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/details/getIdByOrderNo"
        payload = {'orderNo': ORDER_NO}
        # payload['orderNo'] = get_global_data('token_wuj')  # 替换OrderNo
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '37',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            global CUST_ID, CUST_NAME, ORDER_ID, ORDER_PHONE
            CUST_ID = response['data']['custIdentityCard']  # 身份证号
            CUST_NAME = response['data']['custName']  # 姓名
            ORDER_ID = response['data']['orderId']  # 订单号
            ORDER_PHONE = response['data']['orderPhone']  # 订单手机号
            msg = "【检查点6】待处理详情页面通过getIdByOrderNo接口获取OrderNo【%s】获取身份证【%s】姓名【%s】订单号【%s】"\
                  % (ORDER_NO, CUST_ID, CUST_NAME, ORDER_ID)
            log.info(msg)
            assert CUST_ID, msg
        else:
            log.error("【FAIL】待处理详情页面getIdByOrderNo调用失败|%s" % str(response))
            assert 0

    def test_query_commercial_information(self, get_global_data):
        """
        查询审核页面贷款主体信息，应该只有工商主体
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/common/queryCommercialInformation"
        payload = {"loanName": CUST_NAME, "loanIdNo": CUST_ID, "orderId": ORDER_ID}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            busEntityName = [data['busEntityName'] for data in response['data']]  # 工商主体名称列表
            busLicenseNoFirst = response['data'][0]['busLicenseNo']  # 第一个工商主体编号
            msg = "【检查点7】审核页面贷款主体接口queryCommercialInformation返回工商信息【%s】"\
                  % str(busEntityName)
            log.info(msg)
            assert len(response['data']) == 3, msg
        else:
            log.error("【FAIL】待处理详情页面queryCommercialInformation调用失败|%s" % str(response))
            assert 0

    def test_get_user_bank(self, get_global_data):
        """
        查询审核页面贷款银行
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/bank/getUserBank"
        payload = {"registerName": "wuj", "countyCode": "340103000000"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            bankName = [data['bankName'] for data in response['data']]  # 贷款名称列表
            msg = "【检查点7】审核页面银行接口getUserBank返回贷款银行信息【%s】" % str(bankName)
            log.info(msg)
            assert len(response['data']) == 12, msg
        else:
            log.error("【FAIL】待处理详情页面getUserBank调用失败|%s" % str(response))

    def test_pass_guarantee(self, get_global_data):
        """
        提交审核（安徽皖信投资管理有限责任公司+邮储银行+贷款10w+利率1%）--> 线下项目
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/passGuarantee"
        payload = {"loanApplicantId":"91340100MA2U4JGY1G","loanBankCode":"403361000006","loanGuaranteeAmount":"10",
                   "loanGuaranteeRate":"0.01","paymentType":"0","orderId":ORDER_ID,
                   "orderNo":ORDER_NO,"loanApplicantPhone":ORDER_PHONE,
                   "loanApplicantIdcard":CUST_ID,"loanSubmmitter":"wuj","custName":CUST_NAME,
                   "countyCode":"340103000000","loanApplicantName":"安徽皖信投资管理有限责任公司","busEntityType":"1"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点8】审核页面提交订单【%s】审核通过" % ORDER_ID
            log.info(msg)
            assert 1, msg
        else:
            log.error("【FAIL】审核页面审核接口passGuarantee调用失败|%s" % str(response))
            assert 0

    def test_query_to_send_project_offline(self, get_global_data):
        """
        检查线下审核项目中是否有提交审核的数据
        :param get_global_data:
        :return:
        """
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/guarantee/queryToSendProject"
        payload = {"pageNum":1,"pageSize":10,"loanApplicantName":"","loanApplicantIdcard":"","paymentTypeCode":"",
                   "loanBankCode":"","personalType":"2","orderStatus":"7"}
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '102',
            'Authorization': get_global_data('token_wuj'),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['code'] == 1:  # 接口请求成功
            msg = "【检查点9】线下项目页面存在订单【%s】数据" % ORDER_ID
            log.info(msg)
            assert response['data']['content'][0]['loanApplicantPhone'] == ORDER_PHONE, msg
        else:
            log.error("【FAIL】线下项目页面接口queryToSendProject调用失败|%s" % str(response))
            assert 0

    def test_generate_batch_project(self, get_global_data):
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
        msg = "【检查点10】线下项目页面订单【%s】批量生成数据" % ORDER_ID
        log.info(msg)
        assert response['code'] == 1, msg

