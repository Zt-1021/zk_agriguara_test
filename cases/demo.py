#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/2 15:18
# @Author　: wanghr

import pytest

"""
def test_send_uncheck_list():
    if result_cust_id and token_wuj:
        log.info("======【流程2】调用小程序接口发送未通过主体(年龄不符)+有复核标识数据======")
        sleep(1)
        # 检查数据库数据正确性
        result_obd = odb.select_one('SELECT * FROM t_agriguarantee_order WHERE CUSTID="%s"' % str(result_cust_id))
        if result_obd['code'] == "0000":  # 查询成功
            # 检查ORDER_ISBLACK字段状态
            msg = "【检查点1】【PASS】t_agriguarantee_order表ORDER_ISBLACK字段状态正确，预期是【%s】，实际是【%s】" \
                  % (str(EXPECT_ORDER_ISBLACK), str(result_obd['data']['ORDER_ISBLACK']))
            log.info(msg)
            assert result_obd['data']['ORDER_ISBLACK'] == EXPECT_ORDER_ISBLACK, msg

            # 检查ORDER_DESC字段状态
            msg = "【检查点1】【PASS】t_agriguarantee_order表ORDER_DESC字段状态正确，预期是【%s】，实际是【%s】" \
                  % (str(EXPECT_ORDER_DESC), str(result_obd['data']['ORDER_DESC']))
            log.info(msg)
            assert result_obd['data']['ORDER_DESC'] == EXPECT_ORDER_DESC, msg

            # 检查NO_PASS_TYPE字段状态
            msg = "【检查点1】【PASS】t_agriguarantee_order表NO_PASS_TYPE字段状态正确，预期是【%s】，实际是【%s】" \
                  % (str(EXPECT_NO_PASS_TYPE), str(result_obd['data']['NO_PASS_TYPE']))
            log.info(msg)
            assert result_obd['data']['NO_PASS_TYPE'] == EXPECT_NO_PASS_TYPE, msg
        else:
            log.error("【FAIL】查询t_agriguarantee_order表数据失败")
            assert 0, "【FAIL】查询t_agriguarantee_order表数据失败"

        # 检查未通过主体页面该数据是否有复核标识
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/getNoPassOrderList"

        payload = {"custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')","orderTown":"","orderCity":"","registerName":"wuj","custIdentityCard":"510402194102155605","sourceType":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","noPassType":""}
        payload['custIdentityCard'] = result_mini_program  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'token': token_wuj,
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        if response['status'] == "success":  # 接口请求成功
            msg = "【检查点2】未通过主体中存在复核标识，预期结果【1】实际结果【%s】" % str(response['data']['content'][0]['sourceType'])
            log.info(msg)
            assert response['data']['content'][0]['sourceType'] == '1', msg

        else:
            log.error("【FAIL】未通过主体页面查询接口调用失败|%s" % str(response))
            assert 0, "【FAIL】未通过主体页面查询接口调用失败|%s" % str(response)

        # 提交复核请求
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/order/recheck/passRecheckOrder"
        payload = {"orderid": "","custName": ""}
        payload['orderid'] = response['data']['content'][0]['orderid']  # 替换订单编号
        payload['custName'] = response['data']['content'][0]['custName']  # 替换姓名
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'token': token_wuj,
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = common.send_http(url=url, method="POST", headers=headers, data=payload)
        msg = "【检查点3】订单【%s】提交复核成功|%s" % (str(payload['orderid']), str(response))
        log.info(msg)
        assert response['code'] == 1, msg

        # 检查有效需求主体是否有数据
        url = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/getPassOrderList"

        payload = {"orderIsblack":"(3,4)","custName":"","orderCounty":"('340103000000','340102000000','340111000000','340121000000','340122000000','340181000000','340123000000','340124000000','340202000000','340203000000','340207000000','340208000000','340221100000','340222000000','340223000000','340281000000','340802000000','340803000000','340811000000','340881000000','340882000000','340822000000','340825000000','340826000000','340827000000','340828000000','341524000000','341503000000','341522000000','341523000000','341504000000','341502000000','341525000000','341324000000','341322000000','341321000000','341323000000','341302000000','340421000000','340402000000','340403000000','340404000000','340406000000','340405000000','411330104000','340621000000','340603000000','340604000000','340602000000','340104000000','340172000000','340171000000')","orderTown":"","orderCity":"","registerName":"wuj","custIdentityCard":"632222194305296807","sourceType":"","loanAmountOrder":"","orderCreateTimeOrder":"desc","pageNum":1,"pageSize":10,"orderBank":"","orderPrepariedTimeStart":"","orderPrepariedTimeEnd":"","orderCreateTimeStart":"","orderCreateTimeEnd":"","dictItemCode":""}
        payload['custIdentityCard'] = result_mini_program  # 替换身份证号
        headers = {
            'Host': '101.91.192.161:8081',
            'Content-Length': '1134',
            'token': token_wuj,
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
            assert 0, "【FAIL】未通过主体页面查询接口调用失败|%s" % str(response)
    else:
        log.error("【FAIL】获取CUSTID数据失败")
        assert 0, "【FAIL】获取CUSTID数据失败"
"""


class TestDemo(object):

    @pytest.fixture(scope="class")
    def init_demo(self, login):
        a = login
        print(a)

    # def test_demo(self, login):
    #     a = login
    #     print(a)


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-ra", "demo.py"])
