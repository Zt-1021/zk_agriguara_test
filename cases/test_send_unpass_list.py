#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/1 0:33
# @Author　: wanghr
"""
测试发送黑名单业务流程
小程序发送黑名单->web后台未通过主体(未通过类型)
"""

import pytest
from cases import send_request
from base import Db
from base import Log
from time import sleep

log = Log.TestLog(logger='test_send_black_list').get_log()
odb = Db.OperationDb()  # 实例化数据库操作类


@pytest.mark.test_send_unpass_list
class TestSendUnPassList(object):

    def test_creat_order(self):
        global EXPECT_ORDER_ISBLACK,result_mini_program,result_cust_id
        # 测试预期结果
        EXPECT_ORDER_ISBLACK = "13"

        log.info("======【流程1】调用小程序接口发送初筛不通过数据======")
        result_mini_program = send_request.send_order_by_mini_program("2")  # 调用小程序接口发送初筛不通过数据
        result_cust_id = send_request.get_cust_id(result_mini_program)  # 获取cust id

    def test_send_unpass_list(self):
        if result_mini_program:
            # 检查数据库数据正确性
            sleep(1)
            result_obd = odb.select_one('SELECT * FROM t_agriguarantee_order WHERE CUSTID="%s"' % str(result_cust_id))
            if result_obd['code'] == "0000":  # 查询成功
                msg = "【检查点1】t_agriguarantee_order表ORDER_ISBLACK状态正确，实际是【%s】" % str(result_obd['data']['ORDER_ISBLACK'])
                log.info(msg)
                assert result_obd['data']['ORDER_ISBLACK'] == EXPECT_ORDER_ISBLACK, msg
            else:
                log.error("【FAIL】查询数据库数据失败")
                assert 0
        else:
            log.error("【FAIL】获取CUSTID数据失败")
            assert 0
