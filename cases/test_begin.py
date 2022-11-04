#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/3 13:42
# @Author　: wanghr


# 解决uncode编码警告：在unicode等价比较中，把两个参数同时转换为unicode编码失败。中断并认为他们不相等。
#
# windows下的字符串str默认编码是ascii，而python编码是utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from base import common
from base import Log

log = Log.TestLog(logger='test_begin').get_log()


def test_begin(set_global_data):
    # log.info("=========开始测试=========")
    # token_wuj = common.login("wuj", "4ebef2f51752812a34a6f1a11823e9fc")  # 业务员wuj登录，获取token
    # token_chiq = common.login("chiq", "c2e8e2a4a977539e5b2e253751ea7d5d")  # 管理员chiq登录，获取token
    #
    # if token_wuj and token_chiq:
    #     set_global_data('token_wuj', token_wuj)
    #     set_global_data('token_chiq', token_chiq)
    # else:
    #     log.error("【FAIL】业务员/管理员登录失败")
    pass
