#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/2 19:42
# @Author　: wanghr


import pytest
from datetime import datetime
random_time = datetime.now().strftime('%Y%m%d%H%M%S')


if __name__ == '__main__':

    # pytest.main(["-v"])  # 执行所有case
    # pytest.main(["-q", "-s", "-ra", "main.py"])
    # pytest.main(["-ra", '-v', '-x', '-k=test_begin', '--html=./report/report.html', '--capture=sys'])  # 运行指定标签用例
    # pytest.main(["-ra", '-v', '-x', '--html=./report/report.html', '--capture=sys'])  # 默认格式报告
    # pytest.main(["-ra", '-v', '-x', '--html=./report/report_%s.html' % random_time, '--capture=sys'])  # 带时间格式报告
    # pytest.main(['-v', '-q', '--alluredir', './report1.html'])
    # pytest.main(["-ra", '-v', '-x', '-m=test_send_uncheck_list', '--html=./report/report.html', '--capture=sys'])
    pytest.main(["-ra", '-v', '-x', '-m test_queryimport', '--html=./report/report.html', '--capture=sys'])
    # pytest.main(["-ra", '-v', '-x', '-m test_send_verified_unpass', '--html=./report/report.html', '--capture=sys'])