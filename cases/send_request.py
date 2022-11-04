#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/01/24
# @Author　: zhangt

"""
提供给其他方法调用通过小程序端接口发送请求
"""


import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import uuid
from datetime import datetime
from faker import Faker
import random
import requests
import json
from base import Db
from base import Log
import time


log = Log.TestLog(logger='send_request').get_log()
db_ware = Db.OperationDb(name_db='zk_data_warehouse', user_db='zkdatawarehouse', passwd_db='Q#5UCAmaqb7p')  # 实例化大数据库
odb = Db.OperationDb()  # 实例化数据库操作类
fake = Faker(locale='zh_CN')


param_save_order = {
    "REGISTERLOGID":"C9DB302F-37DB-48B3-BA3A-864204B44ABB",
    "CUST_CODE":"CFFE53C8-FCA7-4B6C-B209-83F6F3C292CB",
    "CUST_IDENTITY_CARD":"34122219940228144X",
    "CUST_NAME":"纪文静",
    "ORDER_CUSTFACE_URL":"http://117.71.53.199:50021/group1/M00/11/32/CgUEPGHuQeCAXYh8AACn6dLKayQ244.jpg",
    "CUST_HOME_ADDRESS":"安徽省太和县旧县镇于苗村纪庄1号",
    "ORDERID":"1E60A30A-BA41-4423-AD27-A74CD1862CEA",
    "ORDER_NO":"",
    "CUSTID":"3DC2CCD6-BDC8-4546-8725-D714DE4671F7",
    "ORDER_AUTHORIZATION_URL":"http://117.71.53.199:50021/group2/M00/07/88/CgUEPmHuQgaAHUWKAAcEMxYvu94068.png",
    "ORDER_LOAN_AMOUNT":"28",
    "ORDER_LOAN_PURPOSE":"1",
    "ORDER_LOAN_PURPOSEDESC":"www",
    "ORDER_PREPARIED_TIME":"202206",
    "BUSINESSLIST":[
        {
            "showDelete":0,
            "isChose":0,
            "plantType":"批发和零售业>装卸搬运和仓储业>谷物、棉花等农产品仓储>谷物仓储",
            "businessScale":"28万元",
            "ORDER_BUSINESS_SECTOR":"批发和零售业-装卸搬运和仓储业-谷物、棉花等农产品仓储-谷物仓储",
            "ORDER_BUSINESS_PERIOD":"3年",
            "showunit":0,
            "showyear":0,
            "UNITDESC":"上一年度销售额",
            "ORDER_BUSINESS_SCALENUMS":"28",
            "ORDER_BUSINESS_SCALEUNIT":"万元",
            "ORDERID":"1E60A30A-BA41-4423-AD27-A74CD1862CEA",
            "ORDER_BUSINESSID":"92B7CF86-3D7D-4ADA-98DB-A1BC32859E44"
        }
    ],
    "ORDER_PROVINCE":"34",

    "ORDER_CITY":"340100000000",
    "ORDER_COUNTY":"340103000000",
    "ORDER_TOWN":"340103003000",
    "ORDER_BANK":"102361000242",
    "ORDER_DISTRICT":"合肥市-庐阳区-杏林街道",

    "ORDER_SIGN_URL":"http://117.71.53.199:50021/group1/M00/11/32/CgUEPGHuQgOAQipyAABR_fsd3_o779.png",
    "ORDER_FACE_STATUS":"0",
    "ORDER_REPAYMENT_STATE":"0",
    "APPTYPEID":"1",
    "ORDER_PHONE":"17612182745",
    "ORDER_OPERATOR_PHONE":"17612182745",
    "ORDER_LOANTHEME":"秋收助农活动",
    "ORDER_LOANLIMIT":"1",
    "ORDER_CREATE_TIME":"2022-01-24 14:07:02",
    "ORDER_RESOURCE":"1",
    "ORDER_CUSTBACK_URL":"http://117.71.53.199:50021/group2/M00/07/88/CgUEPmHuQeiAfebvAABivr4ATjE067.jpg",
    "ORDER_EFFECTIVE_TIME":"2006.05.29-2026.05.29"
}

sql_loan_info_base = "INSERT INTO `zk_data_warehouse`.`t_agriguarantee_loan_info_base`" \
                     "(`ID`, `TABLE_IMPORT_TYPE`, `TABLE_DATA_SOURCE`, `LOAN_NAME`, `LOAN_ID_NO`, `ID_INVALID_DT`," \
                     "`CURRENT_ADDR_PROVINCE`, `CURRENT_ADDR_CITY`, `CURRENT_ADDR_DISTRICT`, `CURRENT_ADDR_TOWN`, " \
                     "`GRAIN_GROWER_ADDR`, `MBL_NO`, `MBL_NO_A`, `BUS_ENTITY_NAME`, `LOANSUB_ADDR_PROVINCE`, " \
                     "`LOANSUB_ADDR_CITY`, `LOANSUB_ADDR_DISTRICT`, `LOANSUB_ADDR_TOWN`, `LOANSUB_ADDR`, `CORPN_TP_A`, " \
                     "`CORPN_TP_B`, `CORPN_TP_C`, `CORPN_TP_D`, `CORPN_SC`, `CORPN_VAR_UNIT`, `CULTIVATED_AREA`, " \
                     "`GROWING_GRAIN_AREA`, `WOODLAND_AREA`, `GRASSLAND_AREA`, `WATER_SURFACE_AREA`, `OTHER_LAND_INFO`, " \
                     "`CORPN_AGE_LIMIT`, `BUSINESS_YEAR`, `TOTAL_REVENUE_YEAR`, `FINANCIAL_SUBSIDY_STANDARD`, " \
                     "`FINANCIAL_SUBSIDY_AMT`, `IS_AGRICULTURAL_INS`, `AGRI_INSURANCE_TYPE`, `AGRI_INSURANCE_SCALE`, " \
                     "`OPESTA_MODEL_STATUS`, `IS_PARTY_MEMBER`, `AGRIOBJ_CORPN_TP`, `IS_REGISTERED`, `BUS_LICENSE_NO`, " \
                     "`IS_REGISTERED_TRADEMARK`, `IS_QUALITY_CERTIFICATION`, `FINANCIAL_SUPPORT_YEAR`, " \
                     "`FINANCIAL_SUPPORT_AMT`, `LOAN_SUPPORT_YEAR`, `LOAN_SUPPORT_AMT`, `REMARKS`, `OTHER`, `OPERATOR`, " \
                     "`OPERATOR_ACCOUNT`, `IP_ADDR`, `CREATE_TIME`, `UPDATE_TIME`) " \
                     "VALUES(%s, '3', '家庭农场名录', %s, %s, '', '', '', '', '', '', '182****9078', '', " \
                     "'繁昌县孙村镇马冲粮油种植家庭农场', '安徽省', '芜湖市', '繁昌区', '孙村镇', " \
                     "'安徽省芜湖市繁昌区孙村镇汪洋村', '', '', '', '', '271.6', '亩', 272.00, 272.00, 0.00, 0.00, " \
                     "0.00, 0.00, '', '2020', 37.0000, '', NULL, '1', '', '', '0', '', '1', '1', '', '0', '0', '2020', " \
                     "0.0000, '2020', 0.0000, NULL, '', NULL, NULL, NULL, NOW(), NOW())"

content = "\n请输入以下类型的数据：\n 0    待审核项目有复核(年龄超标)\n 1    自动通过项目\n 2    黑名单项目" \
          "\n 3    待审核项目无复核\n 4    待审核项目有复核(用途超标)\n exit    退出\n"

url_bussies = "http://218.78.117.176:8887/wx/hkm/queryCommercialAndFinicialInfo"
url_custom  = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/imporCustHouseFromCustomerService"
url_importAddCustHouse = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm/addCustHouse"
url_save_order = 'http://218.78.117.176:8887/wx/hkm/insertOrderInfo'
headers = {"content-type": "application/json"}


def get_random(type=0):
    """
    获取随机数据
    :param type: 整数类型
    :return: 字符串类型数据
    """
    if type == 0:  # 大写UUID
        value = (str(uuid.uuid4())).upper()
    elif type == 1:  # 随机姓名
        value = fake.name()
    elif type == 2:  # 随机身份证,最大63岁
        value = fake.ssn(min_age=18, max_age=64)
    elif type == 3:  # 固定时间格式
        value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif type == 4:  # 手机号码
        value = fake.phone_number()
    elif type == 5:  # 含有敏感词的文案
        value = random.choice(['买房', '买车', '消费', '医疗', '上学'])
    elif type == 6:  # 地址
        value = fake.address()
    else:  # 时间戳
        value = datetime.now().strftime('%Y%m%d%H%M%S')
    return value


def get_cust_id(card):
    result_sql = odb.select_one('SELECT CUSTID FROM t_agriguarantee_cust WHERE CUST_IDENTITY_CARD="%s"' % str(card))
    if result_sql['code'] == "0000":
        return result_sql['data']['CUSTID']
    else:
        log.error("【FAIL】通过身份证号从t_agriguarantee_cust表获取CUSTID失败|%s" % str(result_sql))
        return 0


def send_order_by_mini_program(value="1"):
    # 调用小程序接口发送请求
    param_save_order['REGISTERLOGID'] = get_random()
    param_save_order['BUSINESSLIST'][0]['ORDERID'] = get_random()
    param_save_order['ORDER_NO'] = get_random()
    param_save_order['CUSTID'] = get_random()
    param_save_order['CUST_CODE'] = get_random()
    param_save_order['ORDERID'] = get_random()
    param_save_order['BUSINESSLIST'][0]['ORDER_BUSINESSID'] = get_random()
    param_save_order['BUSINESSLIST'][0]['ORDERID'] = param_save_order['ORDERID']
    param_save_order['CUST_IDENTITY_CARD'] = get_random(type=2)
    param_save_order['CUST_NAME'] = get_random(type=1)
    param_save_order['ORDER_CREATE_TIME'] = get_random(type=3)
    param_save_order['CUST_HOME_ADDRESS'] = get_random(type=6)
    param_save_order['ORDER_LOAN_PURPOSEDESC'] = '自动化测试' + get_random(type=999)

    if value == "2":  # 初筛不通过项目
        pass
        # param_save_order['ORDER_LOAN_PURPOSEDESC'] += get_random(type=5)

    elif value == "0":  # 待审核项目有复核(年龄不满足)
        param_save_order['CUST_IDENTITY_CARD'] = fake.ssn(min_age=70, max_age=90)  # 修改年龄为100岁
        response_data = requests.request("POST", url=url_bussies, headers=headers,
                                         data=json.dumps({"LOAN_NAME": param_save_order['CUST_NAME'],
                                                          "CUST_IDENTITY_CARD": param_save_order['CUST_IDENTITY_CARD']}))
        if response_data.text == '{"code":1,"msg":"查询工商和财政补贴数据","data":null,"status":null}':
            pass
        else:
            log.error("【FAIL】调取工商接口数据失败：%s" % str(response_data))
            return 0

    elif value == "1":  # 自动通过项目(家庭农场库有数据)
        # 家庭农场库新增一条数据
        data = [(get_random(), param_save_order['CUST_NAME'],
                 param_save_order['CUST_IDENTITY_CARD'][:10] + "****" + param_save_order['CUST_IDENTITY_CARD'][14:])]
        result = db_ware.insert_data(sql_loan_info_base, data)
        if result['code'] == '0000':
            pass
        else:
            log.error("【FAIL】添加家庭农场名录数据失败：%s" % str(result))
            return 0

    elif value == "3":  # 待审核项目无复核

        response_data = requests.request("POST", url=url_bussies, headers=headers,
                                         data=json.dumps({"LOAN_NAME": param_save_order['CUST_NAME'],
                                                          "CUST_IDENTITY_CARD": param_save_order[
                                                              'CUST_IDENTITY_CARD']}))
        if response_data.text == '{"code":1,"msg":"查询工商和财政补贴数据","data":null,"status":null}':
            pass
        else:
            print("【FAIL】调取工商接口数据失败：%s" % str(response_data))



        '''
         # 修改逻辑，取消客服新增库的判断，更改为业务员导入的判断

        response_data = requests.request("post", url=url_importAddCustHouse, headers=headers,
                                         data=json.dumps({"list": [{"isShowFour": 0, "corpnTpA": "C", "corpnTpB": "13", "corpnTpC": "131", "corpnTpD": "1312", "corpnSc": "333", "corpnVarUnit": "万元", "createTime": time.time()}],
                                                          "loansubAddrDistrict": "太湖县",
                                                          "loansubAddrTown": "晋熙镇",
                                                          "loansubAddrCity": "安庆市",
                                                          "loanName": param_save_order['CUST_NAME'],
                                                          "loanIdNo": param_save_order['CUST_IDENTITY_CARD'],
                                                          "tableImportType": "1",
                                                          "createTime": time.time()}))

        if response_data.text == '{"code":1,"msg":"新增成功","data":null,"status":"success"}':
            pass
        else:
            log.error("【FAIL】调取业务员导入接口数据失败：%s" % str(response_data))
            return 0
        
        '''


        '''
        客服新增库
        response_data = requests.request("post", url=url_custom, headers=headers, data=json.dumps(
            {"loanName": param_save_order['CUST_NAME'], "loanIdNo": param_save_order['CUST_IDENTITY_CARD'],
             "mblNo": "13899991111", "loansubAddrCity": "", "loansubAddrDistrict": "",
             "loansubAddrTown": "", "businessInfo": [], "other": ""}))

        if response_data.text == '{"code":1,"msg":"新增成功","data":null,"status":"success"}':
            pass
        else:
            log.error("【FAIL】调取客服新增接口数据失败：%s" % str(response_data))
            return 0
        
        '''

    elif value == "4":  # 待审核项目有复核(用途不满足)
        param_save_order['ORDER_LOAN_PURPOSEDESC'] += get_random(type=5)
        response_data = requests.request("POST", url=url_bussies, headers=headers,
                                         data=json.dumps({"LOAN_NAME": param_save_order['CUST_NAME'],
                                                          "CUST_IDENTITY_CARD": param_save_order[
                                                              'CUST_IDENTITY_CARD']}))
        if response_data.text == '{"code":1,"msg":"查询工商和财政补贴数据","data":null,"status":null}':
            pass
        else:
            log.error("【FAIL】调取工商接口数据失败：%s" % str(response_data))
            return 0
    else:
        log.error("【FAIL】暂不支持的请求类型：%s" % str(value))
        return 0

    # 发送请求
    log.info("【提交贷款申请参数】：%s" % str(param_save_order))
    response_save_order = requests.request("POST", url=url_save_order, headers=headers, data=json.dumps(param_save_order))
    if response_save_order.text == '{"code":1,"msg":"新增成功","data":null,"status":null}':
        log.info("【新增项目成功】：" + response_save_order.text)
        return param_save_order['CUST_IDENTITY_CARD']  # 返回唯一身份证标识
    else:
        log.error("【FAIL】新增项目失败：" + response_save_order.text)
        return 0