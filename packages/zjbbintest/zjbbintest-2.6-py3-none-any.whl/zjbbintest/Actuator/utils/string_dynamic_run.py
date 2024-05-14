"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/12 19:18:00
"""
import itertools

from zjbbintest.Actuator.bin_test_exception.bin_test_exception import FormatBTStringException, BTFuncNotFoundException, \
    BTActionNotFoundException
from zjbbintest.bintest_data import BinTestData
from jsonpath_rw import parse
import logging


class StringDynamicRun:
    """
    字符串动态执行方法
    主要处理$BT[]中的conf()、func()和var()，通过run方法将字符串变为单纯的纯文本字符串
    """

    def __init__(self, source_str, case_var_dict={}, req_dict={}, resp_dict={}):
        """
        :param source_str: 源字符串
        """
        # 源字符串，类似https://$BT[conf(ip)]:$BT[conf(host)]/$BT[conf(path)]?name=$BT[func(var(rebotId))]
        self.source_str = source_str if source_str else ''
        # case执行过程中的变量都存在这个字典中
        self.case_var_dict = case_var_dict
        # case执行过程中的请求列表
        self.req_dict = req_dict
        # case执行过程中的响应列表
        self.resp_dict = resp_dict
        # 不可执行字符串list
        self.__inoperable_str_list = []
        # 可执行字符串list
        self.__operable_str_list = []
        # 执行后的字符串list
        self.__operated_str_list = []
        # 最后的结果字符串，我们需要的是这个
        self.res_str = ''

    def run(self):
        """
        执行字符串动态替换
        :return: 第一个是完全替换后的字符串，第二个是case的变量字典
        """
        if type(self.source_str) != str:
            return self.source_str, self.case_var_dict
        self.__get_bintest_string()
        self.__batch_replace()
        self.__restore_str()
        return self.res_str, self.case_var_dict

    def __get_bintest_string(self):
        """
        获取字符串
        """
        # TODO: 有问题，再看看
        # source_str_len = len(self.source_str)
        # if source_str_len < 5:
        #     raise FormatBTStringException(f'字符串"{self.source_str}"格式存在问题，请检查字符串内容')
        stack = []
        index_list = []
        try:
            # 丑陋，但是有效
            new_str = self.source_str.replace("$BT[", "…")
            new_str_len = len(new_str)
            for index in range(new_str_len):
                if new_str[index] == '[' or new_str[index] == '…':
                    stack.append(index)
                elif new_str[index] == ']':
                    left = stack.pop()
                    if new_str[left] == '…':
                        right = index
                        index_list.append((left, right))
            self.__split_str(new_str, index_list)
        except Exception as e:
            print(e)
            raise FormatBTStringException(f'字符串"{self.source_str}"格式存在问题，请检查括号[]是否匹配')

    def __batch_replace(self):
        """
        批量替换字符串
        :return:
        """
        str_dynamic_run_tool = StringDynamicRunTool(self.case_var_dict, self.req_dict, self.resp_dict)
        self.__operated_str_list = [str_dynamic_run_tool.run(operable_str)
                                    for operable_str in self.__operable_str_list]

    def __restore_str(self):
        """

        :return:
        """
        if self.__inoperable_str_list == ["", ""] and len(self.__operated_str_list) == 1:
            self.res_str = self.__operated_str_list[0]
        else:
            paired = itertools.zip_longest(self.__inoperable_str_list, self.__operated_str_list, fillvalue='')
            self.res_str = ''.join([i + (j if j is not None else '') for i, j in paired])

    def __split_str(self, new_str, index_list):
        """
        切割字符串，把要动态执行的字符串切割出来，放在一个列表中，剩余部分也放在一个列表中，这个两个列表就是返回值
        丑陋，但是有效
        :param new_str:
        :param index_list:
        :return:
        """
        mid_list = [-1, ]
        for (left, right) in index_list:
            mid_list.append(left)
            mid_list.append(right)
        mid_list.append(len(new_str))
        len_mid = len(mid_list)
        source_index_list = [(mid_list[i], mid_list[i + 1]) for i in range(0, len_mid, 2)]
        # print(source_index_list)
        # print(index_list)
        for (left, right) in index_list:
            self.__operable_str_list.append(new_str[left + 1: right])
        for (left, right) in source_index_list:
            self.__inoperable_str_list.append(new_str[left + 1: right])


class StringDynamicRunTool:
    """
    字符串动态执行工具类
    初始化时需要传入一个
    字典类型case_var_dict，代表该条case的变量
    dict类型req_dict，表示该条case的请求信息
    dict类型resp_dict，表示该条case的响应信息
    """

    def __init__(self, case_var_dict, req_dict, resp_dict):
        """
        :param case_var_dict: case级变量字典
        """
        self.case_var_dict = case_var_dict
        self.req_dict = req_dict
        self.resp_dict = resp_dict

    def run(self, operable_str):
        """
        传入可以执行的字符串如func()、var()、set()，执行具体动作，返回执行后的字符串和case级变量字典
        :param operable_str:
        :return:
        """
        logging.debug(f'动态执行字符串：{operable_str}')
        if operable_str is None or operable_str == '':
            return ''
        operable_str = operable_str.strip()
        # if operable_str.startswith("conf(") and operable_str.endswith(")"):
        #     new_str = operable_str[5:-1]
        #
        #     value_str = self.run(new_str)
        #     value_path = value_str.split('.')
        #     res_str = BinTestData.config_dict
        #     for value_path_item in value_path:
        #         res_str = res_str.get(value_path_item)
        #     return res_str
        if operable_str.startswith("func(") and operable_str.endswith(")"):
            new_str = operable_str[5:-1]
            value_str = self.run(new_str)
            func_name = value_str.split('(')[0]
            func_args = value_str[len(func_name) + 1: len(value_str) - 1].split(',')
            func_args = [self.run(arg) for arg in func_args]
            try:
                if func_args is None or func_args == [] or func_args == [""]:
                    logging.debug(f'执行无参方法{func_name}')
                    res_str = BinTestData.func_dict.get(func_name)()
                else:
                    logging.debug(f'执行有参方法{func_name}，参数为:{func_args}')
                    res_str = BinTestData.func_dict.get(func_name)(*func_args)
            except TypeError:
                raise BTFuncNotFoundException(func_name)
            return res_str
        elif operable_str.startswith("var(") and operable_str.endswith(")"):
            # TODO 换成jsonpath的方式获取变量
            # DONE 2024-5-9
            new_str = operable_str[4:-1]
            value_str = self.run(new_str)
            if value_str.startswith("$var"):
                # 获取用户自定义变量
                data_source = self.case_var_dict
                json_path = '$' + value_str[4:]
                logging.debug(f'从变量中获取内容，jsonpath为:{json_path}；变量字典为:{data_source}')
            elif value_str.startswith("$req"):
                # 获取请求响应变量
                data_source = self.req_dict
                json_path = '$' + value_str[4:]
                logging.debug(f'从请求中获取内容，jsonpath为:{json_path}；请求字典为:{data_source}')
            elif value_str.startswith("$resp"):
                # 获取请求响应变量
                data_source = self.resp_dict
                json_path = '$' + value_str[5:]
                logging.debug(f'从响应中获取内容，jsonpath为:{json_path}；响应字典为:{data_source}')
            elif value_str.startswith("$conf"):
                # 获取配置文件变量
                data_source = BinTestData.config_dict
                json_path = '$' + value_str[5:]
                logging.debug(f'从配置文件中获取内容，jsonpath为:{json_path}；配置字典为:{data_source}')
            else:
                return None
            # value_path = value_str.split('.')
            # if len(value_path) == 0:
            #     return None
            # if value_path[0] == "$var":
            #     # 获取用户自定义变量
            #     data_source = self.case_var_dict
            #     json_path = '$' + value_str[4:]
            #     logging.debug(f'从变量中获取内容，jsonpath为:{json_path}；变量字典为:{data_source}')
            # elif value_path[0] == "$req":
            #     # 获取请求响应变量
            #     data_source = self.req_list
            #     json_path = '$' + value_str[4:]
            #     logging.debug(f'从请求中获取内容，jsonpath为:{json_path}；请求字典为:{data_source}')
            # elif value_path[0] == "$resp":
            #     # 获取请求响应变量
            #     data_source = self.resp_list
            #     json_path = '$' + value_str[5:]
            #     logging.debug(f'从响应中获取内容，jsonpath为:{json_path}；响应字典为:{data_source}')
            # elif value_path[0] == "$conf":
            #     # 获取配置文件变量
            #     data_source = BinTestData.config_dict
            #     json_path = '$' + value_str[5:]
            #     logging.debug(f'从配置文件中获取内容，jsonpath为:{json_path}；配置字典为:{data_source}')
            # else:
            #     return None
            expr = parse(json_path)
            result = expr.find(data_source)
            if result:
                res_list = []
                for match in result:
                    res_list.append(match.value)
                if len(res_list) == 1:
                    return res_list[0]
                else:
                    return res_list
            else:
                return None
            # for value_path_item in value_path[1:]:
            #     if value_path_item.isdigit():
            #         try:
            #             data_source = data_source[int(value_path_item)]
            #         except IndexError:
            #             return None
            #     else:
            #         data_source = data_source.get(value_path_item)
            # return data_source
        elif operable_str.startswith("set(") and operable_str.endswith(")"):
            new_str = operable_str[4:-1]
            # 获取变量名和值
            index = new_str.find(',')
            var_key = new_str[:index]
            var_value = new_str[index + 1:]
            var_value = self.run(var_value)
            self.case_var_dict[var_key] = var_value
            logging.debug(f'设置变量{var_key}为{var_value}')
            return ''
        elif operable_str.startswith("action(") and operable_str.endswith(")"):
            new_str = operable_str[7:-1]
            value_str = self.run(new_str)
            action_name = value_str.split('(')[0]
            action_args = value_str[len(action_name) + 1: len(value_str) - 1].split(',')
            action_args = [self.run(arg) for arg in action_args]
            try:
                if action_args is None or action_args == [] or action_args == [""]:
                    logging.debug(f'执行无参动作{action_name}')
                    BinTestData.action_dict.get(action_name)()
                else:
                    logging.debug(f'执行有参动作{action_name}，参数为{action_args}')
                    BinTestData.action_dict.get(action_name)(*action_args)
            except TypeError as e:
                raise BTActionNotFoundException(action_name)
            return ''
        else:
            return operable_str
