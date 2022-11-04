#!/usr/bin/python3.8
# -*- coding:utf-8 -*-


import yaml
import os

class yamlUtil():
    def __init__(self, yaml_file):

        '''
        通过init把文件传入到这个类
        :param yaml_file:
        '''

        self.yaml_file = yaml_file

    #读取ymal文件
    def read_yaml(self):

        '''
        读取yaml，将yaml反序列化，就是把我们yaml格式转换成dict格式
        :return:
        '''

        with open(self.yaml_file) as f:
            # value = yaml.safe_load(f.read()) #文件流，加载方式
            value = yaml.load(f, Loader=yaml.FullLoader)  # 文件流，加载方式
            return value


if __name__ == "__main__":
    data = yamlUtil("../data/queryimport_verified.yaml").read_yaml()

    print(data)
    # print(data[0]['payload'])
    # yamlUtil(r"D:\zt\WorkWord\farmAgr\ProcessAuto\zk_agriguara_test\data\queryimport_verified.yaml").read_yaml()