#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/3/2 23:48
# @Author　: wanghr

import pytest
import yaml
from base import ymal_util
from base import common
from base import Log
from configparser import ConfigParser

log = Log.TestLog(logger='test_begin').get_log()

# 定义一个全局变量，用于存储内容
global_data = {}


@pytest.fixture(scope="session")
def set_global_data():
    """
    设置全局变量，用于关联参数
    :return:
    """

    def _set_global_data(key, value):
        global_data[key] = value

    return _set_global_data


@pytest.fixture(scope="session")
def get_global_data():
    """
    从全局变量global_data中取值
    :return:
    """

    def _get_global_data(key):
        return global_data.get(key)

    return _get_global_data


@pytest.fixture(scope="session")
def begin(set_global_data):
    log.info("=========开始测试=========")
    token_wuj = common.login("wuj", "4ebef2f51752812a34a6f1a11823e9fc")  # 业务员wuj登录，获取token
    token_chiq = common.login("chiq", "c2e8e2a4a977539e5b2e253751ea7d5d")  # 管理员chiq登录，获取token
    if token_wuj and token_chiq:
        set_global_data('token_wuj', token_wuj)
        set_global_data('token_chiq', token_chiq)
    else:
        log.error("【FAIL】业务员/管理员登录失败")


def pytest_configure(config):
    marker_list = ["test_send_uncheck_list", "test_send_unpass_list","test_send_verified"]
    for markers in marker_list:
        config.addinivalue_line("markers",markers)


@pytest.fixture(scope="session")
def config():
    conf = ymal_util.yamlUtil("../conf.yaml").read_yaml()
    return conf


@pytest.fixture(scope="session")
def env_vars(config):
    env = config["env"]
    mapping = {
        "test":{
            "project_url":"http://101.91.192.161:8081/proxy-218_78_117_176-custom",
            "Host":"101.91.192.161:8081"
        },
        "prod":{
            "project_url": "https://farmwarrant.luoex.xin:8086",
            "Host": "farmwarrant.luoex.xin:8086"
        }
    }

    project_url = mapping[env]["project_url"]
    host = mapping[env]["Host"]
    return project_url,host


@pytest.fixture(scope="session")
def begin_02(config,env_vars):
    log.info("=========开始测试=========")
    url = env_vars[0]
    host = env_vars[1]
    username = config["username"]
    password = config["password"]

    token = common.login(url,host,username, password)
    # if token_wuj and token_chiq:
    #     set_global_data('token_wuj', token_wuj)
    #     set_global_data('token_chiq', token_chiq)
    # else:
    #     log.error("【FAIL】业务员/管理员登录失败")

    return token,username
