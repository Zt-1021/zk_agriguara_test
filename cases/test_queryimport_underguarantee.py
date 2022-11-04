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

log = Log.TestLog(logger='test_queryimport_underguarantee').get_log()

odb = Db.OperationDb()  # 实例化数据库操作类


@pytest.mark.test_queryimport_underguarantee
@pytest.mark.parametrize("args", ymal_util.yamlUtil("../data/queryimport_underguarantee.yaml").read_yaml())
class TestQueryImportUnderguarantee(object):
    def test_Underguarantee(self, begin_02,set_global_data, get_global_data,env_vars,args):
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
            total_amount = response01["data"][args['amount_data']]
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
            data_excel_amount = 0
            if args['amount_type'] == "贷款":
                for data in data_excel['贷款金额（元）']:
                    data_excel_amount += data/10000
            # elif args['amount_type'] == "代偿":
            #     for data in data_excel['代偿总额（元）']:   # 代偿总额（元）
            #         data_excel_amount += data/10000
            elif args['amount_type'] == "核销":
                for data in data_excel['核销金额(元)']:
                    data_excel_amount += data/10000

            if total_sum == data_excel_num:
                if numpy.allclose(total_amount, float(data_excel_amount)):
                    msg = ("【检查点3】列表与导出数据一致，共%s条，总金额%s万元" % (total_sum, total_amount))
                    log.info(msg)
                    assert 1 == 1

                else:
                    log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总金额%s万元；表格共%s条，总金额%s万元" % (
                    total_sum, total_amount, data_excel_num, data_excel_amount))
                    assert 0

            else:
                log.error("【FAIL】总数：列表与导出数据不一致，列表共%s条，总金额%s万元；表格共%s条，总金额%s万元" % (
                total_sum, total_amount, data_excel_num, data_excel_amount))
                assert 0

        else:
            log.error("【FAIL】" + args['interfaceName'] + "获取接口调用失败|%s" % str(response01))
            assert 0

    if __name__ == '__main__':
        pytest.main(["-ra", '-v', '-x', '-m test_queryimport_underguarantee', '--html=./report/report.html', '--capture=sys'])