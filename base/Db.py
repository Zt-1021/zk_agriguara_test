#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
# @DateTime　　: 2021/12/15 09:35
# @Author　: wanghr
"""
定义对mysql数据库基本操作的封装
1.包括基本的单条语句操作，删除、修改、更新
2.独立的查询单条、查询多条数据
3.独立的添加多条数据
"""

import pymysql
from base import Log
import traceback

log = Log.TestLog(logger='op_mysql').get_log()


class OperationDb(object):
    # 定义初始化连接数据库
    def __init__(self, host_db='218.78.116.81', user_db='zkagriguaratest', passwd_db='8Pp4@Kf3mRj6', name_db='zk_agriguara_test',
                 port_db=33894, link_type=0):
        self.db = name_db
        """
        :param host_db: 数据库服务主机
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 端口号，整型数字
        :param link_type: 链接类型，用于输出数据是元祖还是字典，默认是字典，link_type=0
        :return:游标
        """
        try:
            if link_type == 0:
                # 创建数据库链接,返回字典
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
            else:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8', autocommit=True)  # 创建数据库链接，返回元祖
            self.cur = self.conn.cursor()
        except pymysql.Error as e:
            log.error(traceback.format_exc())

    # 获取单个库.表结构
    def get_single_table_alter(self, db_table, columns=[]):
        """
        获取指定表指定列的属性
        :param table_name: 表名
        :param columns: 列名组成的列表
        :return: 字段属性组成的列表
        """
        alter = []
        table_name = db_table.split('.')[1]
        sql = 'desc %s.%s;' % (self.db, table_name)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        for i in result:
            if (not columns) or i['Field'] in columns:  # 默认取全部字段 or 指定字段
                alter.append({'Field': db_table+'.'+i['Field'], 'Type': i['Type'], 'Null': i['Null'], 'Key': i['Key'], 'Default': i['Default']})
            else:
                pass

        # sqllist = 'show table status where NAME="%s";' % (table_name)
        # self.cur.execute(sqllist)
        # result = self.cur.fetchall()
        # tablecomment = result[0]['Comment']
        # [item.update(TableComment=tablecomment) for item in td]
        # sqllist = 'show full columns from %s;' % (table_name)
        # self.cur.execute(sqllist)
        # result = self.cur.fetchall()
        # for item in td:
        #     for item1 in result:
        #         if item['Field'] == item1['Field']:
        #             item['Extra'] = item1['Extra']
        #             break
        return alter

    def get_multi_table_alter(self, *table_column):
        """
        获取多张表的结构
        :param table_column: (表名，字段元组),(表名，字段元组)
        :return: 多张表的多个字段构成的结构，字段前带上表名
        """
        result_multi_table = []
        for value in table_column:
            result_multi_table += self.get_single_table_alter(value[0], value[1])
        return result_multi_table

    # 定义单条数据操作，包含删除、更新操作
    def op_sql(self, condition):
        """
        :param condition: sql语句,该通用方法可用来替代updateone，deleteone
        :return:字典形式
        """
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            self.cur.execute(condition)  # 执行sql语句
            self.conn.commit()  # 提交游标数据
            result = {'code': '0000', 'message': '执行通用操作成功', 'data': []}
        except Exception:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
            log.info(traceback.format_exc())
        return result

    # 查询表中单条数据
    def select_one(self, condition):
        """
        :param condition: sql语句
        :return: 字典形式的单条查询结果
        """
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            rows_affect = self.cur.execute(condition)
            self.conn.commit()  # 提交游标数据
            if rows_affect > 0:  # 查询结果返回数据数大于0
                results = self.cur.fetchone()  # 获取一条结果
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': []}
        except pymysql.Error:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行单条查询异常', 'data': []}
            log.error(traceback.format_exc())
        return result

    # 查询表中多条数据
    def select_all(self, condition):
        """
        :param condition: sql语句
        :return:字典形式的批量查询结果
        """
        try:
            log.info("SQL:%s" % condition)
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            rows_affect = self.cur.execute(condition)
            self.conn.commit()  # 提交游标数据
            if rows_affect > 0:  # 查询结果返回数据数大于0
                self.cur.scroll(0, mode='absolute')  # 光标回到初始位置
                results = self.cur.fetchall()  # 返回游标中所有结果
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': []}
        except Exception:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行批量查询异常', 'data': []}
            log.error(traceback.format_exc())
        return result

    # 定义表中插入数据操作
    def insert_data(self, condition, params):
        """
        :param condition: insert语句
        :param params: insert数据，列表形式[('3','Tom','1 year 1 class','6'),('3','Jack','2 year 1 class','7'),]
        :return:字典形式的批量插入数据结果
        """
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            results = self.cur.executemany(condition, params)  # 返回插入的数据条数
            self.conn.commit()
            result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': results}
        except Exception:
            self.conn.rollback()  # 执行回滚操作
            result = {'code': '9999', 'message': '执行批量插入异常', 'data': []}
            log.error(traceback.format_exc())
        return result

    # 定义一次获取多张表数据
    def get_data_by_multi_table(self, *conditions):
        """
        根据多个sql获取每个sql的结果，返回数据中按找传入sql顺序返回
        :param conditions: 多个sql
        :return:
        """
        results = []
        for condition in conditions:
            result_select = self.select_all(condition=condition)
            data_condition = result_select['data']
            results.append(data_condition)
        return {'code': '0000', 'message': '获取多个sql结果成功', 'data': results}

    # 数据库关闭
    def __del__(self):
        if self.cur is not None:
            self.cur.close()  # 关闭游标
        if self.conn is not None:
            self.conn.close()  # 释放数据库资源


# if __name__ == '__main__':
#     odt = OperationDbInterface(host_db='172.16.16.28', user_db='root', passwd_db='zkml123!@#', name_db='interface_auto_test', port_db=3306)
#     a = odt.insert_data('INSERT INTO t_response(`id_task`, `id_request`, `response`, `result`, `deail`, `create_time`) VALUES (%s, %s, %s, %s, %s, %s)', [(2, 2, "{'success': True, 'data': {'businessFlowNo': 'px', 'globalFlowNo': 'QJ1363055261132132352', 'serverIp': '172.16.0.245'}, 'msg': '开通子账户成功！', 'errCode': None, 'message': '开通子账户成功！'}", 1, '[pass]预期结果在返回包中,[pass]接口请求参数值与数据库字段值一致', '2021-02-20 17:17:54')])
#     # b = odt.insert_data('INSERT INTO t_response(`id_task`, `id_request`, `response`, `result`, `deail`) VALUES (%s, %s, %s, %s, %s)', [(2,3,'2',1,'2')])
#     # a = odt.get_single_table_alter('tog_statistics_apply_day', ['from_organ_id', 'service_organ_id'])
#     # b = odt.get_single_table_alter('tog_base_apply_order')
#     # log.info(a)
#     # log.info(b)