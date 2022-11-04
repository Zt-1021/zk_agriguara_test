#!/usr/bin/python3.8
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pytest
import pandas
import numpy
from base import Db
from base import Log
from base import common
from base import ymal_util

log = Log.TestLog(logger='test_queryimport_PremiumBank').get_log()

odb = Db.OperationDb()  # 实例化数据库操作类


@pytest.mark.test_queryimport_PremiumBank
@pytest.mark.parametrize("args", ymal_util.yamlUtil("../data/queryimport_PremiumBank.yaml").read_yaml())
class TestQueryImportPremiumBank(object):
    def test_PremiumBank(self, begin_02,env_vars,args):
        """
        检查列表数据与导出数据一致
        :return:
        """
        url_list = env_vars[0] + args['url_list']
        url_export = env_vars[0] + args['url_export']

        args['payload']['registerName'] = begin_02[1]
        payload = args['payload']

        headers = {
            'Host': env_vars[1],
            'Content-Length': '1134',
            'Authorization': begin_02[0],
            'Content-Type': 'application/json;charset=UTF-8'
        }

        response01 = common.send_http(url=url_list, method="POST", headers=headers, data=payload)
        response02 = common.send_http(url=url_export, method="POST", headers=headers, data=payload)

        if response01['status'] == "success":  # 接口请求成功
            total_sum = response01["data"]["total"]
            total_amount_Credit = response01["data"]["totalCreditLimit"]   # 授信额度
            total_amount_Expend = response01["data"]["totalExpendLimit"]   # 支用额度
            total_amount_Payment = response01["data"]["totalPaymentAmount"]   # 总缴费金额

            msg = "【检查点1】" + args['interfaceName'] + "获取接口调用成功"
            log.info(msg)
            assert response01['code'] == 1, msg

            if response02['status'] == "success":  # 接口请求成功
                msg = ("【检查点2】" + args['interfaceName'] + "导出接口调用成功,文件链接为%s" % response02['data'])
                log.info(msg)
                assert response02['data'] != "", msg
            else:
                log.error("【FAIL】" + args['interfaceName'] + "导出接口调用失败|%s" % str(response02))
                assert 0

            data_excel = pandas.read_excel(response02['data'])
            data_excel_num = data_excel.shape[0]
            data_excel_amount_Credit = 0
            data_excel_amount_Expend = 0
            data_excel_amount_Payment = 0

            for data in data_excel['授信额度(万元)']:
                data_excel_amount_Credit += data
            for data in data_excel['支用额度(万元)']:
                data_excel_amount_Expend += data
            for data in data_excel['缴费金额(元)']:
                data_excel_amount_Payment += data

            if total_sum == data_excel_num:
                if numpy.allclose(total_amount_Credit, float(data_excel_amount_Credit)):
                    if numpy.allclose(total_amount_Expend, float(data_excel_amount_Expend)):
                        if numpy.allclose(total_amount_Payment, float(data_excel_amount_Payment)):
                            msg = ("【检查点3】列表与导出数据一致，共%s条，支用额度%s万元，授信额度%s万元，缴费金额%s元" % (
                            total_sum, total_amount_Credit, total_amount_Expend,total_amount_Payment))
                            log.info(msg)
                            assert 1 == 1

                        else:
                            log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总缴费金额%s元；表格共%s条，总缴费金额%s万元" % (
                                total_sum, total_amount_Payment, data_excel_num, data_excel_amount_Payment))
                            assert 0

                    else:
                        log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总支用额度%s万元；表格共%s条，总支用额度%s万元" % (
                            total_sum, total_amount_Expend, data_excel_num, data_excel_amount_Expend))
                        assert 0

                else:
                    log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总授信额度%s万元；表格共%s条，总授信额度%s万元" % (
                     total_sum, total_amount_Credit, data_excel_num, data_excel_amount_Credit))
                    assert 0

            else:
                log.error("【FAIL】总数：列表与导出数据不一致，列表共%s条，支用额度%s万元，授信额度%s万元，缴费金额%s元；表格共%s条，支用额度%s万元，授信额度%s万元，缴费金额%s元" % (
                    total_sum, total_amount_Credit,total_amount_Expend, total_amount_Payment,data_excel_num, data_excel_amount_Credit,data_excel_amount_Expend,data_excel_amount_Payment))
                assert 0

        else:
            log.error("【FAIL】" + args['interfaceName'] + "获取接口调用失败|%s" % str(response01))
            assert 0

    if __name__ == '__main__':
        pytest.main(["-ra", '-v', '-x', '-m test_queryimport_PremiumBank', '--html=./report/report.html', '--capture=sys'])