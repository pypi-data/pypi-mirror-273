"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/12 13:19:00
"""
import configparser
from datetime import datetime
import json
import os
from functools import wraps
from inspect import getmembers, isfunction

from zjbbintest.Actuator.bin_test_case.bin_test_case import BinTestCase
from zjbbintest.Actuator.bin_test_exception.bin_test_exception import BTFuncFormatCheckException, \
    BTAssertFormatCheckException, \
    BTActionFormatCheckException, BTCaseNotLoadException
from zjbbintest.Actuator.utils.processing_path import get_json_files_in_directories
from zjbbintest.Analysis.har2json import save_json, have_easy_har, analysis_har_list, \
    parse_har_list
from zjbbintest.Analysis.replace_values import get_req_bt_str_map, get_resp_bt_str_map, save_conf_var, \
    get_conf_bt_str_map, case_json_replace_bintest_var
from zjbbintest.Template.bintest_template import render_report
from zjbbintest.bintest_data import BinTestData
import logging


# config_dict = {}
# func_dict = {}
# assert_dict = {}
# action_dict = {}
# run_case_list = []
# case_load_flag = False


def bt_func(*args):
    """
    装饰器，进行函数入参和返回值的判断，入参个数必须与args的长度相等，且类型必须与args对应
    :param args:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            converted_args = []
            all_args = list(func_args) + list(func_kwargs.values())
            if len(args) != len(all_args):
                raise BTFuncFormatCheckException(
                    f'{func.__name__}方法需要{len(args)}个参数，实际传入{len(all_args)}个参数')

            for a, b in zip(args, all_args):
                try:
                    converted_args.append(a(b))
                except Exception:
                    raise BTFuncFormatCheckException(f'{func.__name__}方法的参数 {b} 无法转为 {a.__name__} 类型')
            result = func(*converted_args, **func_kwargs)
            if result is None:
                raise BTFuncFormatCheckException(f'{func.__name__}方法必须有返回值')
            return result

        wrapper.is_bt_func = True
        return wrapper

    return decorator


def bt_action(*args):
    """
    装饰器，进行函数入参和返回值的判断，入参个数必须与args的长度相等，且类型必须与args对应，无返回值
    :param args:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            converted_args = []
            all_args = list(func_args) + list(func_kwargs.values())
            if len(args) != len(all_args):
                raise BTActionFormatCheckException(
                    f'{func.__name__}方法需要{len(args)}个参数，实际传入{len(all_args)}个参数')

            for a, b in zip(args, all_args):
                try:
                    converted_args.append(a(b))
                except Exception:
                    raise BTFuncFormatCheckException(f'{func.__name__}方法的参数 {b} 无法转为 {a.__name__} 类型')
            # for i, (a, b) in enumerate(zip(args, all_args)):
            #     if not isinstance(b, a):
            #         raise BTActionFormatCheckException(
            #             f'{func.__name__}方法的第{i + 1}个参数类型应为{a.__name__}，实际为{type(b).__name__}')
            result = func(*converted_args, **func_kwargs)
            if result is not None:
                raise BTActionFormatCheckException(f'{func.__name__}方法必须无返回值')
            return result

        wrapper.is_bt_action = True
        return wrapper

    return decorator


def bt_assert(func):
    """
    装饰器，进行函数入参和返回值的判断，入参个数为2个，返回值必须为boolean类型
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检查入参个数
        arg_count = len(args) + len(kwargs)
        if arg_count != 2:
            raise BTAssertFormatCheckException(f"{func.__name__}方法需要2个参数，实际传入{arg_count}个参数")

        # 执行函数并获取返回值
        result = func(*args, **kwargs)

        # 检查返回值是否为boolean类型
        if not isinstance(result, bool):
            raise BTAssertFormatCheckException(f"{func.__name__}方法返回值必须为boolean类型")

        return result

    # 标记为bt_assert
    func.is_bt_assert = True
    return wrapper


def conf_load(path):
    """
    读取配置文件，将配置文件中的内容存进config_dict中，以便全局使用
    path是个.ini文件，里面是配置的一些全局可以使用到的变量
    :param path:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(path)
    for section in config.sections():
        BinTestData.config_dict[section] = {}
        for key, value in config.items(section):
            BinTestData.config_dict[section][key] = value


def func_load(module):
    """
    根据模块名，将用户定义的函数加载到func_dict中，以便全局使用
    :param module:
    :return:
    """
    for name, obj in getmembers(module):
        if isfunction(obj) and getattr(obj, 'is_bt_func', False):
            BinTestData.func_dict[name] = obj


def action_load(module):
    """
    根据模块名，将用户定义的action加载到func_dict中，以便全局使用
    :param module:
    :return:
    """
    for name, obj in getmembers(module):
        if isfunction(obj) and getattr(obj, 'is_bt_action', False):
            BinTestData.action_dict[name] = obj


def assert_load(module):
    """
    根据模块名，将用户定义的断言函数加载到assert_dict中，以便全局使用
    :param module:
    :return:
    """
    for name, obj in getmembers(module):
        if isfunction(obj) and getattr(obj, 'is_bt_assert', False):
            BinTestData.assert_dict[name] = obj


def case_load(path_list, mark_labels=[], priority=[]):
    """
    加载case，只会加载制定case
    :param path_list: 路径列表，支持多个路径，递归加载路径下的所有case
    :param mark_labels: 加载指定标签的case，支持多个标签，比如['label1', 'label2']代表加载label1和label2的case
    :param priority: 加载指定优先级的case，支持多个优先级，比如[1, 2]代表加载1和2的case
    :return: 返回case列表，list中存的是BinTestCase对象
    """
    # 获取case文件
    case_path_list = get_json_files_in_directories(path_list)
    # 判断标签和优先级
    # for case_path in case_path_list:
    #     with open(case_path, 'r') as json_file:
    #         data = json.load(json_file)
    #     json_string = json.dumps(data)
    #     if not mark_labels and not priority:
    #         BinTestData.run_case_list.append(BinTestCase(json_string))
    #     elif mark_labels and priority:
    #         case_mark_labels = data.get('mark_label', [])
    #         case_priority = data.get('priority', 999)
    #         if set(case_mark_labels) & set(mark_labels) and case_priority in priority:
    #             BinTestData.run_case_list.append(BinTestCase(json_string))
    #     elif mark_labels and not priority:
    #         case_mark_labels = data.get('mark_label', [])
    #         if set(case_mark_labels) & set(mark_labels):
    #             BinTestData.run_case_list.append(BinTestCase(json_string))
    #     else:
    #         case_priority = data.get('priority', 999)
    #         if case_priority in priority:
    #             BinTestData.run_case_list.append(BinTestCase(json_string))
    # # 修改状态
    # BinTestData.case_load_flag = True
    # return
    for case_path in case_path_list:
        with open(case_path, 'r') as json_file:
            data = json.load(json_file)
        if not mark_labels and not priority:
            BinTestData.run_case_list.append(BinTestCase.create_obj_by_dict(data))
        elif mark_labels and priority:
            case_mark_labels = data.get('mark_label', [])
            case_priority = data.get('priority', 999)
            if set(case_mark_labels) & set(mark_labels) and case_priority in priority:
                BinTestData.run_case_list.append(BinTestCase.create_obj_by_dict(data))
        elif mark_labels and not priority:
            case_mark_labels = data.get('mark_label', [])
            if set(case_mark_labels) & set(mark_labels):
                BinTestData.run_case_list.append(BinTestCase.create_obj_by_dict(data))
        else:
            case_priority = data.get('priority', 999)
            if case_priority in priority:
                BinTestData.run_case_list.append(BinTestCase.create_obj_by_dict(data))
    # 修改状态
    BinTestData.case_load_flag = True
    return


def run(log_path, report_path):
    """
    执行测试用例，生成测试报告
    :param report_path: 测试报告路径
    :param log_path: 日志路径
    :return:
    """
    now_time = datetime.now()
    # 初始化日志
    if not os.path.exists(log_path):
        # 创建文件所在的目录
        dir_path = os.path.dirname(log_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 创建文件
        with open(log_path, 'w') as f:
            pass
        print(f"文件 {log_path} 已创建。")
    else:
        pass
    logging.basicConfig(filename=log_path, filemode='a', level=logging.DEBUG,
                        format='%(asctime)s - %(pathname)s - %(lineno)s - %(message)s')
    case_res_list = []
    if BinTestData.case_load_flag:
        # 执行测试用例
        for bin_case in BinTestData.run_case_list:
            case_res = bin_case.run()
            case_res_list.append(case_res)
        # 生成测试报告
        render_report(case_res_list, now_time, report_path)
    else:
        raise BTCaseNotLoadException()


def rebuild(har_file_path, conf_ini_file_path, case_dir_path=''):
    """
    根据har_file_path重建case，将其放在case_dir_path目录下
    case_dir_path目录下，应该存放三个文件
    1 替换后的case的json形式 xxx_case.json
    2 变量的bt_str映射关系 xxx_bt_str.json
    3 提取的请求和响应信息 xxx_req_resp.json
    :param har_file_path:
    :param conf_ini_file_path
    :param case_dir_path:
    :return: 
    """
    # 判断har_file_path是否存在
    if not os.path.exists(har_file_path):
        raise FileNotFoundError(f"har文件 {har_file_path} 不存在。")
    if not os.path.exists(conf_ini_file_path):
        raise FileNotFoundError(f"配置文件 {conf_ini_file_path} 不存在。")
    # 获取文件名
    file_name = os.path.basename(har_file_path)
    # 获取路径
    dir_name = os.path.dirname(har_file_path)
    # 获取基础名（不含后缀）
    base_name, _ = os.path.splitext(file_name)

    easy_har_list = have_easy_har(har_file_path)
    case_json = analysis_har_list(easy_har_list)
    req_dict, resp_dict = parse_har_list(easy_har_list)
    conf_dict = save_conf_var(conf_ini_file_path)
    req_bt_str_map = get_req_bt_str_map(req_dict)
    resp_bt_str_map = get_resp_bt_str_map(resp_dict)
    conf_bt_str_map = get_conf_bt_str_map(conf_dict)
    new_case_json = case_json_replace_bintest_var(case_json, conf_bt_str_map, req_bt_str_map, resp_bt_str_map)
    req_resp_json = {}
    for req_key, req in req_dict.items():
        req_resp_json[req_key] = {
            'request': req,
            'response': resp_dict.get(req_key)
        }
    bt_str_map_json = {
        'conf': conf_bt_str_map,
        'req': req_bt_str_map,
        'resp': resp_bt_str_map
    }
    if not case_dir_path:
        # 如果case_dir_path为空，则放在当前目录下的case目录下
        case_dir_path = dir_name + f'/{base_name}'
    case_full_path = case_dir_path + f'/{base_name}_case.json'
    bt_str_map_full_path = case_dir_path + f'/{base_name}_bt_str.json'
    req_resp_full_path = case_dir_path + f'/{base_name}_req_resp.json'
    # 创建case_dir_path目录
    if not os.path.exists(case_dir_path):
        os.makedirs(case_dir_path)
    # 保存
    save_json(new_case_json, case_full_path)
    save_json(bt_str_map_json, bt_str_map_full_path)
    save_json(req_resp_json, req_resp_full_path)





