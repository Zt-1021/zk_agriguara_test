#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2022/01/24
# @Author　: zhangt

"""
模拟小程序端发起不同类型的项目申请，解决从小程序走耗时
"""


import sys
import os

from typing import Dict, Any, Union

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

# 解决uncode编码警告：在unicode等价比较中，把两个参数同时转换为unicode编码失败。中断并认为他们不相等。
#
# windows下的字符串str默认编码是ascii，而python编码是utf8

reload(sys)
sys.setdefaultencoding('utf-8')


db_ware = Db.OperationDb(name_db='zk_data_warehouse',user_db='zkdatawarehouse',passwd_db = 'Q#5UCAmaqb7p')  # 实例化大数据库
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
    "ORDER_LOAN_AMOUNT":"150",
    "ORDER_LOAN_PURPOSE":"1",
    "ORDER_LOAN_PURPOSEDESC":"www",
    "ORDER_PREPARIED_TIME":"202210",
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

    "ORDER_CITY":"341200000000",              # 340500000000                  # 340100000000                        # 341200000000
    "ORDER_COUNTY":"341282000000",            # 340521000000                  # 340103000000                       # 341282000000
    "ORDER_TOWN":"341282101000",              # 340521402000                  # 340103003000                          # 341282101000
    "ORDER_BANK":"105362050023",              # 103361099995                  # 102361000242                      # 105362050023     # 403361000006
    "ORDER_DISTRICT":"阜阳市-界首市-泉阳镇",   # 马鞍山市-当涂县-当涂大青山李白文化旅游区       # 合肥市-庐阳区-杏林街道       # 阜阳市-界首市-泉阳镇

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
}  # type: Dict[Union[str, Any], Union[str, Any]]



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


sql_old_ag_project_base = "INSERT INTO `zk_data_warehouse`.`old_ag_project_base`" \
                     "(`uuid`, `project_uuid`, `project_uuid_focus`, `base_uuid`, `enterprise_uuid`, `project_uuid_assure`," \
                     "`order_no`, `mainsubject_name`, `operator_name`, `id_card`,`village`,`link_telephone`,`loan_limit`, " \
                     "`suggest_limit`, `remark`, `borrower_type_code`, `borrower_type_name`, `project_name`, " \
                     "`project_code`, `input_status_code`, `input_status_name`, `pass_status_code`, `pass_status_name`, " \
                     "`reject_reason`, `check_status_code`, `check_status_name`, `is_same_code`, `is_same_name`, `guana_info`, " \
                     "`GROWING_GRAIN_AREA`, `WOODLAND_AREA`, `GRASSLAND_AREA`, `WATER_SURFACE_AREA`, `OTHER_LAND_INFO`, " \
                     "`guana_info_repeat`, `guana_info_final`, `risk_audit_idea`, `credit_money`, `credit_money_repeat`,`credit_money_guana`," \
                     "`credit_bank_money`, `is_credit`, `is_credit_audit_code`, `is_credit_audit_name`, `relation_check_uuid`,`loan_fee`," \
                     "`subject_category_code`, `subject_category_name`, `no_load_land`, `pass_audit_code`, `pass_audit_name`, " \
                     "`dis_loan_money`, `dis_loan_date`, `dis_loan_user_id`, `dis_loan_user_name`,`online_loan_money`,`toal_loan_money`," \
                     "`toal_repayment_money`, `loan_balance`, `loan_startdate`, `loan_enddate`, `top_contract_no`, `replace_contract_no`, " \
                     "`bank_loan`, `audit_idea`, `audit_remark`, `bank_name`, `bank_id`, `industry_category_code`, " \
                     "`industry_category_name`, `limit_date`, `run_info`, `run_info_range`, `relation_ent`, `credit_info`, " \
                     "`assest_lia_info`, `other_info`, `proof_use_info`, `figth_loan_anay`, `special_condition`, `project_base_info`, " \
                     "`risk_audit_info`, `project_base_desc`, `project_base_limit`, `project_condition`, `auditer_idea`, `risk_audit_relation_id`, " \
                     "`revi_report_relation_id`, `check_relation_id`, `other_relation_id`, `audit_content_6`, `audit_confirm_6`, `audit_remark_6`, " \
                     "`flow_status_code`, `flow_status_name`, `top_contract_type`, `business_uuid`, `processinstid`, `processdefid`, " \
                     "`node_status_code`, `node_status_name`, `jd_status_code`, `jd_status_name`, `confirm_status_code`, `confirm_status_name`, " \
                     "`copr_bank_uuid`, `copr_bank_name`, `copr_banktype_code`, `copr_banktype_name`, `create_time`, `operate_time`, " \
                     "`manager_name`, `manager_id`, `coun_guaran_step`, `person_type`, `confing_date`, `audit_confirm_date`, " \
                     "`province_code_pb`, `province_name_pb`, `city_code_pb`, `city_name_pb`, `town_code_pb`, `town_name_pb`, " \
                     "`street_code_pb`, `street_name_pb`, `top_contract_name`, `bank_contract_name`, `bank_contract_uuid`, `audit_config_date`, " \
                     "`is_first_audit`, `area_manager_id`, `area_manager_name`, `replace_repay_code`, `guana_info_relation_id`, `dis_confirm_date`, " \
                     "`abort_reason`, `yktype`, `product_type_code`, `product_type_name`, `product_spsd_code`, `product_spsd_name`, " \
                     "`product_wlxl_code`, `product_wlxl_name`, `product_hj_code`, `product_hj_name`, `product_business_code`, `product_business_name`, " \
                     "`if_extension`, `borrow_loan_type`, `person_list_uuid`, `borrowview_uuid`, `apply_limit_date`, `contact_status`, " \
                     "`single_contract_no`, `single_contract_name`, `business_type`, `business_name`, `abort_name`, `abort_time`, " \
                     "`abort_id`, `premiumRate`, `dcbgExport`, `isMSME`, `MSME_relation_id`, `person_business_relation_id`, " \
                     "`bank_industry`, `jbBank`, `spring_type`, `node_status_code_spring`, `node_status_name_spring`)" \
                     "VALUES(%s, 'ceshiADD', '', '', '', '', '1', %s, %s, %s, '', '', null, null, '','1','家庭经营户', '', '', "\
                          "'1','未录入', '1', '已出保', '', '1', '未稽查', null, '', '', '', '', '', null, null, '30.000000', null,"\
                          "'1','1','','',null,'','','','2', '已出保', null, null, null, '', '0.000000', '300000.00', '0.00', "\
                          "'300000.00', '2021-07-01', '2024-07-01', '【2021】邮银皖SN001', '2021年皖农担字第ZC003440号', null, '', '', "\
                          "'中国邮政储蓄银行股份有限公司明光市支行', '1422', '', '', '36', '', '', '', '', '', '', '', '', '', '', '','',"\
                          "'','','','','','','','',null,'',null,'','','',null,null,null,'',null,'',null,'',null,'','05', '邮储银行', "\
                          " NOW(), null, '测试', '265', '', '2', null, null, '340000','安徽省','341100','滁州市','341182','明光市','341182105',"\
                          "'涧溪镇','合作协议','', '', '2021-06-29 00:00:00', '', '265', '测试', null, '', null, '', '','','','','','','','','',"\
                          "null,'',null,null,'','','',null,'','',null,'','',null,'','0.8000', null, null, '', '', '', '', '2', '100', '尽调流程结束')"


content = "\n请输入以下类型的数据：\n 0    待审核项目有复核(年龄超标)\n 1    自动通过项目\n 2    黑名单项目\n 3    待审核项目无复核\n 4    待审核项目有复核(用途超标)\n exit    退出\n"


url_bussies = "http://218.78.117.176:8887/wx/hkm/queryCommercialAndFinicialInfo"
url_custom  = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/imporCustHouseFromCustomerService"
url_importAddCustHouse = "http://101.91.192.161:8081/proxy-218_78_117_176-custom/hkm-service/hkm/addCustHouse"
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


if __name__ == '__main__':
    value = str(input(content))
    while value != "exit":
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

        elif value == "0":  # 待审核项目有复核(年龄不满足)
            param_save_order['CUST_IDENTITY_CARD'] = fake.ssn(min_age=70, max_age=90)  # 修改年龄为100岁
            response_data = requests.request("POST", url=url_bussies, headers=headers,
                                             data=json.dumps({"LOAN_NAME":param_save_order['CUST_NAME'],"CUST_IDENTITY_CARD":param_save_order['CUST_IDENTITY_CARD']}))
            if response_data.text == '{"code":1,"msg":"查询工商和财政补贴数据","data":null,"status":null}':
                pass
            else:
                print("【FAIL】调取工商接口数据失败：%s" % str(response_data))

        elif value == "1":

            # 修改逻辑，取消家庭农场库的判断

            # 存量客户新增一条数据
            data = [(get_random(), param_save_order['CUST_NAME'], param_save_order['CUST_NAME'], param_save_order['CUST_IDENTITY_CARD'])]
            result = db_ware.insert_data(sql_old_ag_project_base, data)
            if result['code'] == '0000':
                pass
            else:
                print("【FAIL】添加存量客户数据失败：%s" % str(result))
                value = str(input(content))
                continue

            '''
            # 家庭农场库新增一条数据
            data = [(get_random(), param_save_order['CUST_NAME'], param_save_order['CUST_IDENTITY_CARD'][:10]+"****"+param_save_order['CUST_IDENTITY_CARD'][14:])]
            result = db_ware.insert_data(sql_loan_info_base, data)
            if result['code'] == '0000':
                pass
            else:
                print("【FAIL】添加家庭农场名录数据失败：%s" % str(result))
                value = str(input(content))
                continue
            
            '''

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
                                             data=json({"list":[{"isShowFour":0,"corpnTpA":"C","corpnTpB":"14","corpnTpC":"141","corpnTpD":"1411","corpnSc":"21","corpnVarUnit":"万元","createTime":"2022-03-14 09:10:38"}],
                                                              "loansubAddrDistrict":"庐阳区","loansubAddrTown":"逍遥津街道","loansubAddrCity":"合肥市","loanName":param_save_order['CUST_NAME'],"loanIdNo":param_save_order['CUST_IDENTITY_CARD'],
                                                              "tableImportType":"1","createTime":"2022-03-14 09:10:38"}))

            if response_data.text == '{"code":1,"msg":"新增成功","data":null,"status":"success"}':
                pass
            else:
                print("【FAIL】调取业务员导入接口数据失败：%s" % str(response_data))
                value = str(input(content))
                continue
            
            
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
            param_save_order['ORDER_LOAN_PURPOSEDESC'] = '自动化测试' + get_random(type=5)
            response_data = requests.request("POST", url=url_bussies, headers=headers,
                                             data=json.dumps({"LOAN_NAME":param_save_order['CUST_NAME'],"CUST_IDENTITY_CARD":param_save_order['CUST_IDENTITY_CARD']}))
            if response_data.text == '{"code":1,"msg":"查询工商和财政补贴数据","data":null,"status":null}':
                pass
            else:
                print("【FAIL】调取工商接口数据失败：%s" % str(response_data))
        else:
            value = str(input(content))
            continue

        # 发送请求
        print("【提交贷款申请参数】：%s" % str(param_save_order))
        response_save_order = requests.request("POST", url=url_save_order, headers=headers,
                                               data=json.dumps(param_save_order))
        if response_save_order.text == '{"code":1,"msg":"新增成功","data":null,"status":null}':
            print("【新增项目成功】：" + response_save_order.text)
        else:
            print("【FAIL】新增项目失败：" + response_save_order.text)

        value = str(input(content))

