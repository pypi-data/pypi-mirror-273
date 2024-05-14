"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/5/9 10:26:00
"""
import configparser
import copy
import json



def replace_values(json_obj, replace_dict):
    """
    替换json中的内容，替换
    :param json_obj:
    :param replace_dict:
    :return:
    """
    if isinstance(json_obj, dict):
        return {k: replace_values(v, replace_dict) for k, v in json_obj.items()}
    elif isinstance(json_obj, list):
        return [replace_values(element, replace_dict) for element in json_obj]
    else:
        return replace_dict.get(json_obj, json_obj)


def save_conf_var(ini_file):
    """
    根据ini文件，生成一个dict，用于替换json中的变量
    :param ini_file:
    :return:
    """
    conf_dict = {}
    config = configparser.ConfigParser()
    config.read(ini_file)
    for section in config.sections():
        conf_dict[section] = {}
        for key, value in config.items(section):
            conf_dict[section][key] = value
    return conf_dict


def generate_value_to_jsonpath_map(obj, path='$'):
    """
    根据json对象，生成一个dict,存放value和jsonpath的映射关系，key为value，value为jsonpath
    :param obj:
    :param path:
    :return:
    """
    value_to_path = {}

    def safe_key(key):
        # 如果键是数字或者以特殊字符开头，使用方括号和引号
        if key[0].isdigit() or not key.replace('_', '').isalnum():
            return f'["{key}"]'
        else:
            return key

    if isinstance(obj, dict):
        for key, value in obj.items():
            safe_key_str = safe_key(key)
            new_path = f'{path}.{safe_key_str}' if path != '$' else f'${safe_key_str}'
            if isinstance(value, (dict, list)):
                nested_paths = generate_value_to_jsonpath_map(value, new_path)
                for val, paths in nested_paths.items():
                    if val not in value_to_path:
                        value_to_path[val] = []
                    value_to_path[val].extend(paths)
            else:
                if value not in value_to_path:
                    value_to_path[value] = []
                value_to_path[value].append(new_path)

    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = f'{path}[{index}]'
            if isinstance(value, (dict, list)):
                nested_paths = generate_value_to_jsonpath_map(value, new_path)
                for val, paths in nested_paths.items():
                    if val not in value_to_path:
                        value_to_path[val] = []
                    value_to_path[val].extend(paths)
            else:
                if value not in value_to_path:
                    value_to_path[value] = []
                value_to_path[value].append(new_path)

    return value_to_path


def get_req_bt_str_map(req_dict):
    """
    获取请求的bt_str map
    :param req_dict:
    :return:
    """
    res_jsonpath_map = {}
    for req_key, req_value in req_dict.items():
        if isinstance(req_value, dict):
            # 请求中，生成key和jsonpath的映射关系只需要考虑body和param
            new_req_value = {}
            if 'body' in req_value:
                new_req_value['body'] = req_value.get('body')
            if 'params' in req_value:
                new_req_value['params'] = req_value.get('params')
            res_jsonpath_map[int(req_key)] = generate_value_to_jsonpath_map(new_req_value)
    for req_id, req_jsonpath_info in res_jsonpath_map.items():
        for req_key, jsonpath_list in req_jsonpath_info.items():
            # 生成bt字符串
            bt_str_list = map(lambda req_jsonpath: f"$BT[var($req['{req_id}'].{req_jsonpath[1:]})]",
                              jsonpath_list)
            res_jsonpath_map[req_id][req_key] = list(bt_str_list)
    return res_jsonpath_map


def get_resp_bt_str_map(resp_dict):
    """
    获取响应的bt_str map
    :param resp_dict:
    :return:
    """
    resp_jsonpath_map = {}
    for resp_key, resp_value in resp_dict.items():
        if isinstance(resp_value, dict):
            # 响应中，生成key和jsonpath的映射关系需要考虑status_code和text，刚好resp_value只有这两😄
            resp_jsonpath_map[int(resp_key)] = generate_value_to_jsonpath_map(resp_value)
    for resp_id, resp_jsonpath_info in resp_jsonpath_map.items():
        for resp_key, jsonpath_list in resp_jsonpath_info.items():
            # 生成bt字符串
            bt_str_list = map(lambda resp_jsonpath: f"$BT[var($resp['{resp_id}'].{resp_jsonpath[1:]})]",
                              jsonpath_list)
            resp_jsonpath_map[resp_id][resp_key] = list(bt_str_list)
    return resp_jsonpath_map


def get_conf_bt_str_map(conf_dict):
    """
    获取配置的bt_str map
    :param conf_dict:
    :return:
    """
    conf_jsonpath_map = generate_value_to_jsonpath_map(conf_dict)
    for conf_key, jsonpath_list in conf_jsonpath_map.items():
        # 生成bt字符串
        # lambda表达式的作用是将$dev.ak转为$BT[var($conf.dev.ak)]
        bt_str_list = map(lambda conf_jsonpath: f"$BT[var($conf.{conf_jsonpath[1:]})]",
                          jsonpath_list)
        conf_jsonpath_map[conf_key] = list(bt_str_list)
    return conf_jsonpath_map


def case_json_replace_bintest_var(case_json, conf_bt_str_map, res_bt_str_map, resp_bt_str_map):
    """
    替换case_json中的变量
    :param case_json:
    :param conf_bt_str_map:
    :param res_bt_str_map:
    :param resp_bt_str_map:
    :return:
    """
    new_case = {
        'caseName': case_json.get('caseName'),
        'description': case_json.get('description'),
        'priority': case_json.get('priority')
    }
    new_case_steps = []
    case_steps = case_json.get('testSteps')
    pre_step_bt_str_map = copy.deepcopy(conf_bt_str_map)
    for step in case_steps:
        step_id = step.get('step')
        # 先处理pre_step_bt_str_map
        if step_id > 0:
            pre_step_bt_str_map = merge_dict(pre_step_bt_str_map,
                                             res_bt_str_map.get(step_id - 1)
                                             if res_bt_str_map.get(step_id - 1) else {})
            pre_step_bt_str_map = merge_dict(pre_step_bt_str_map,
                                             resp_bt_str_map.get(step_id - 1)
                                             if resp_bt_str_map.get(step_id - 1) else {})
        # print(pre_step_bt_str_map)
        request_json = step.get('request')
        # 这些内容只替换和conf的配置做替换
        new_request_json = {
            'url': request_json.get('url'),
            'path': request_json.get('path'),
            'method': request_json.get('method'),
            # 'params': request_json.get('params'),
            'headers': request_json.get('headers')
        }
        new_request_json = replace_nested_values(new_request_json, conf_bt_str_map)
        # param和body和所有做替换
        param_json = request_json.get('param')
        body_json = request_json.get('body')
        new_param_json = replace_nested_values(param_json, pre_step_bt_str_map)
        new_body_json = replace_nested_values(body_json, pre_step_bt_str_map)
        new_request_json['param'] = new_param_json
        new_request_json['body'] = new_body_json

        new_step = {
            'step': step_id,
            'request': new_request_json,
            'action': step.get('action'),
            'assert': step.get('assert')
        }
        new_case_steps.append(new_step)
    new_case['testSteps'] = new_case_steps
    return new_case


def merge_dict(dict1, dict2):
    """
    合并两个字典
    :param dict1:
    :param dict2:
    :return:
    """
    # 创建一个新的字典，用于存储合并后的键值对
    merged_dict = {}

    # 遍历两个字典的键值对，合并相同的键
    for k, v in dict1.items():
        # 如果这个键在第二个字典中也存在，则合并列表
        if k in dict2:
            merged_dict[k] = v + dict2[k]  # 合并两个列表
        else:
            merged_dict[k] = v  # 如果dict2中没有这个键，直接使用dict1中的值

    # 遍历第二个字典，添加dict1中不存在的键
    for k, v in dict2.items():
        if k not in merged_dict:
            merged_dict[k] = v

    return merged_dict


def replace_nested_values(original_dict, replacement_dict):
    """
    替换嵌套字典中的值
    :param original_dict:
    :param replacement_dict:
    :return:
    """
    if isinstance(original_dict, dict):
        new_dict = {}
        for key, value in original_dict.items():
            if isinstance(value, dict):
                new_dict[key] = replace_nested_values(value, replacement_dict)
            elif isinstance(value, list):
                new_dict[key] = [
                    replace_nested_values(item, replacement_dict) if isinstance(item, (dict, list)) else item for item
                    in value]
            elif value in replacement_dict:
                # 使用整个列表作为替换值
                # 如果replacement_dict[value]只有一个元素，则直接使用这个元素替换
                # 如果replacement_dict[value]有多个元素，则使用列表作为替换值，判断是否>10个元素，只取前10个
                new_values = None
                if len(replacement_dict[value]) == 1:
                    new_values = replacement_dict[value][0]
                elif len(replacement_dict[value]) >= 10:
                    new_values = replacement_dict[value][:10]
                else:
                    new_values = replacement_dict[value]
                new_dict[key] = {
                    value: new_values
                }
            else:
                new_dict[key] = value
        return new_dict
    elif isinstance(original_dict, list):
        return [replace_nested_values(item, replacement_dict) for item in original_dict]
    else:
        return original_dict


if __name__ == '__main__':
    # req_dict, resp_dict = parse_har_file(
    #     '/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/机器人搜索.har')
    # # print(req_dict)
    # # print(json.dumps(req_dict))
    # # print(json.dumps(resp_dict))
    # res_jsonpath_map = get_req_bt_str_map(req_dict)
    # print(json.dumps(res_jsonpath_map))
    # resp_jsonpath_map = get_resp_bt_str_map(resp_dict)
    # print(json.dumps(resp_jsonpath_map))
    # req_jsonpath_map = get_req_jsonpath_map(req_dict)
    # print(json.dumps(req_jsonpath_map))

    # conf_dict = save_conf_var('/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/test.ini')
    # # print(json.dumps(conf_dict))
    # conf_jsonpath_map = get_conf_bt_str_map(conf_dict)
    # # print(json.dumps(conf_jsonpath_map))
    #
    # case_json = analysis('/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/机器人搜索.har')
    # # print(json.dumps(case_json))
    #
    # new_case = case_json_replace_bintest_var(case_json, conf_jsonpath_map, res_jsonpath_map, resp_jsonpath_map)
    # print(json.dumps(new_case))
    pass
