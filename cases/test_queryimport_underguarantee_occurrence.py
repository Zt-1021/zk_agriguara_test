#!/usr/bin/python3.8
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pytest
import pandas
import numpy
import xlwings
from base import Db
from base import Log
from base import common
from base import ymal_util

log = Log.TestLog(logger='test_queryimport_underguarantee_occurrence').get_log()

odb = Db.OperationDb()  # 实例化数据库操作类


@pytest.mark.test_queryimport_underguarantee_occurrence
@pytest.mark.parametrize("args", ymal_util.yamlUtil("../data/queryimport_underguarantee_occurrence.yaml").read_yaml())
class TestQueryImportUnderguaranteeOccurrence(object):
    def test_Underguarantee_Occurrence(self, begin_02,set_global_data, get_global_data,env_vars,args):
        """
        检查列表数据与导出数据一致
        :return:
        """
        url_list = env_vars[0] + args['url_list']
        url_export = env_vars[0] + args['url_export']

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
            # set_global_data("passorderlist", response01)
            total_sum = response01["data"]["total"]
            total_amount_1 = response01["data"]['totalLoanRctAmt'] # 贷款金额
            total_amount_2 = response01["data"]['totalLoanBalance']  # 贷款余额
            msg = "【检查点1】" + args['interfaceName'] + "获取接口调用成功"
            log.info(msg)
            assert response01['code'] == 1, msg

            if response02['status'] == "success":  # 接口请求成功
                msg = ("【检查点2】" + args['interfaceName'] + "导出接口调用成功,文件链接为%s" % response02['data'])
                log.info(msg)
                assert response02['data'] != "", msg
            else:
                log.error("【FAIL】" + args['interfaceName'] + "导出接口调用失败|%s" % str(response01))
                assert 0

            data_excel = pandas.read_excel(response02['data'])
            data_excel_num = data_excel.shape[0]
            data_excel_amount_1 = 0  # 贷款金额
            data_excel_amount_2 = 0  # 贷款余额
            if args['amount_type'] == "贷款":
                for data in data_excel['贷款金额(元)']:
                    data_excel_amount_1 += data/10000
                for data in data_excel['贷款余额(元)']:
                    data_excel_amount_2 += data/10000
            elif args['amount_type'] == "解保":
                for data in data_excel['贷款金额(元)']:
                    data_excel_amount_1 += data / 10000
                for data in data_excel['解保金额(元)']:
                    data_excel_amount_2 += data / 10000
            data_excel_amount_1 = format(data_excel_amount_1, '.6f')
            data_excel_amount_2 = format(data_excel_amount_2, '.6f')

            if total_sum == data_excel_num:
                if numpy.allclose(float(total_amount_1), float(data_excel_amount_1)):
                    if numpy.allclose(float(total_amount_2), float(data_excel_amount_2)):
                        msg = ("【检查点3】列表与导出数据一致，共%s条，总金额1为%s万元，总金额2为%s万元" % (total_sum, total_amount_1,total_amount_2))
                        log.info(msg)
                        assert 1 == 1

                    else:
                        log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总金额%s万元；表格共%s条，总金额%s万元" % (
                            total_sum, total_amount_2, data_excel_num, data_excel_amount_2))
                        assert 0

                else:
                    log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总金额%s万元；表格共%s条，总金额%s万元" % (
                    total_sum, total_amount_1, data_excel_num, data_excel_amount_1))
                    assert 0

            else:
                log.error("【FAIL】总数：列表与导出数据不一致，列表共%s条，总金额%s万元；表格共%s条，总金额%s万元" % (
                total_sum, total_amount_1, data_excel_num, data_excel_amount_1))
                assert 0

        else:
            log.error("【FAIL】" + args['interfaceName'] + "获取接口调用失败|%s" % str(response01))
            assert 0

    if __name__ == '__main__':
        pytest.main(["-ra", '-v', '-x', '-m test_queryimport_underguarantee_occurrence', '--html=./report/report.html', '--capture=sys'])