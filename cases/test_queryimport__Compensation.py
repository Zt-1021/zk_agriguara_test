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

log = Log.TestLog(logger='test_queryimport_Compensation').get_log()

odb = Db.OperationDb()  # 实例化数据库操作类


@pytest.mark.test_queryimport_Compensation
@pytest.mark.parametrize("args", ymal_util.yamlUtil("../data/queryimport_Compensation.yaml").read_yaml())
class TestQueryImportCompensation(object):
    def test_Underguarantee_Compensation(self, begin_02,env_vars,args):
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
            total_sum = response01["data"]["total"]
            total_amount = response01["data"]["amount"]   # 代偿总额万元
            total_amount_1 = total_amount*10000   # 代偿总额元
            # total_amount_2 = response01["data"]["compensationOffInfoAmount"]   # 追偿总额

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
            data_excel_amount_1 = 0
            # data_excel_amount_2 = 0
            for data in data_excel['代偿总额（元）']:
                data_excel_amount_1 += data
            # for data_02 in data_excel['已追偿代偿金额（元）']:
            #     if data_02 == "nan":
            #         continue
            #     else:
            #         data_excel_amount_2 += data_02/10000

            if total_sum == data_excel_num:
                if numpy.allclose(total_amount_1, float(data_excel_amount_1)):
                    # if numpy.allclose(total_amount_2, float(data_excel_amount_2)):
                    #     msg = ("【检查点3】列表与导出数据一致，共%s条，总代偿金额%s万元，总追偿金额%s万元" % (total_sum, total_amount_1,total_amount_2))
                    #     log.info(msg)
                    #     assert 1 == 1
                    #
                    # else:
                    #     log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总追偿金额%s万元；表格共%s条，总追偿金额%s万元" % (
                    #         total_sum, total_amount_2, data_excel_num, data_excel_amount_2))
                    #     assert 0

                    msg = ("【检查点3】列表与导出数据一致，共%s条，总代偿金额%s元" % (total_sum, total_amount_1))
                    log.info(msg)
                    assert 1 == 1

                else:
                    log.error("【FAIL】总金额：列表与导出数据不一致，列表共%s条，总代偿金额%s元；表格共%s条，总代偿金额%s元" % (
                     total_sum, total_amount_1, data_excel_num, data_excel_amount_1))
                    assert 0

            else:
                log.error("【FAIL】总数：列表与导出数据不一致，列表共%s条，总代偿金额%s元；表格共%s条，总代偿金额%s元" % (
                    total_sum, total_amount_1, data_excel_num, data_excel_amount_1))
                assert 0

        else:
            log.error("【FAIL】" + args['interfaceName'] + "获取接口调用失败|%s" % str(response01))
            assert 0

    if __name__ == '__main__':
        pytest.main(["-ra", '-v', '-x', '-m test_queryimport_Compensation', '--html=./report/report.html', '--capture=sys'])