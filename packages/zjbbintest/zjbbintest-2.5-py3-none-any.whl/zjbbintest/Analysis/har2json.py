"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/5/8 16:56:00
"""
import json
from urllib.parse import urlparse, parse_qs


def read_har(har_file_path):
    """
    读取har文件，返回json格式字符串
    :param har_file_path: har文件路径
    :return: json格式字符串
    """
    with open(har_file_path, 'r', encoding='utf-8') as f:
        return f.read()


# def analysis(har_file_path, res_file_path=None):
#     """
#     解析har文件，生成测试用例的json格式
#     :param har_file_path: har文件路径
#     :param res_file_path: 解析结果文件路径，如果为None，返回json格式字符串
#     """
#     with open(har_file_path, 'r', encoding='utf-8') as f:
#         har_json = f.read()
#     return analysis_json(har_json)


def analysis_har_list(har_list):
    """
    解析har文件列表，生成测试用例的json格式
    :param har_list:
    :return:
    """
    json_output = {
        "caseName": "",
        "description": "",
        "priority": 0,
        "testSteps": []
    }
    index = 0
    # 提取 request 信息
    for _, entry in enumerate(har_list):
        request = entry['request']
        parsed_url = urlparse(request['url'])
        url = parsed_url.scheme + '://' + parsed_url.netloc
        path = parsed_url.path
        params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        body = request.get('postData', {})
        if 'json' in body.get('mimeType', ''):  # 检查MIME类型是否为JSON
            body = json.loads(body.get('text', '{}'))  # 是则解析
        step = {
            "step": index,
            "request": {
                "url": url,
                "path": path,
                "method": request['method'],
                "headers": {header['name']: header['value'] for header in request['headers']},
                "param": params,
                "body": body
            },
            "action": [],
            "assert": [
                {
                    "expect": f"$BT[var($resp['{index}'].status_code)]",
                    "actual": 200,
                    "operator": "=="
                }
            ]
        }
        json_output['testSteps'].append(step)
        index += 1

    return json_output


# def analysis_json(har_json):
#     """
#     解析har文件，生成测试用例的json格式
#     :param har_json:
#     :return:
#     """
#
#     har_dict = json.loads(har_json)
#     json_output = {
#         "caseName": "",
#         "description": "",
#         "priority": 0,
#         "testSteps": []
#     }
#
#     index = 0
#     # 提取 request 信息
#     for _, entry in enumerate(har_dict['log']['entries']):
#         if entry.get('_resourceType') != 'xhr':
#             continue
#         request = entry['request']
#         parsed_url = urlparse(request['url'])
#         url = parsed_url.scheme + '://' + parsed_url.netloc
#         path = parsed_url.path
#         params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
#         body = request.get('postData', {})
#         if 'json' in body.get('mimeType', ''):  # 检查MIME类型是否为JSON
#             body = json.loads(body.get('text', '{}'))  # 是则解析
#         step = {
#             "step": index,
#             "request": {
#                 "url": url,
#                 "path": path,
#                 "method": request['method'],
#                 "headers": {header['name']: header['value'] for header in request['headers']},
#                 "param": params,
#                 "body": body
#             },
#             "action": [],
#             "assert": [
#                 {
#                     "expect": "",
#                     "actual": "",
#                     "operator": ""
#                 }
#             ]
#         }
#         json_output['testSteps'].append(step)
#         index += 1
#
#     return json_output
#     # # 输出结果
#     # res_str = json.dumps(json_output, indent=4)
#     # if res_file_path:
#     #     with open(res_file_path, 'w', encoding='utf-8') as f:
#     #         f.write(res_str)
#     #     return res_str
#     # else:
#     #     return res_str


def parse_har_list(har_list):
    """
    解析HAR文件列表，返回一个字典，包含请求和响应的键值对
    :param har_list: HAR文件列表
    :return: 请求和响应的字典
    """
    # 初始化请求和响应字典
    req_dict = {}
    resp_dict = {}

    for entry in har_list:
        request = entry['request']
        response = entry['response']
        request_id = str(len(req_dict))

        # 提取请求的URL和路径
        url = request['url']
        parsed_url = urlparse(url)
        path = parsed_url.path

        # 提取请求方法
        method = request['method']

        # 提取请求头
        headers = request['headers']
        headers_dict = {}
        for header in headers:
            headers_dict[header['name']] = header['value']

        # 提取查询参数
        params = {}
        if 'queryString' in request:
            for param in request['queryString']:
                params[param['name']] = param['value']

        # 提取请求体
        body = {}
        if 'postData' in request:
            post_data = request['postData']
            if 'text' in post_data:
                try:
                    body = json.loads(post_data['text'])
                except json.JSONDecodeError:
                    body = post_data['text']

        # 提取响应状态码和文本
        status_code = response['status']
        text = response['content']['text'] if 'content' in response and 'text' in response['content'] else None
        if text is None:
            json_data = None
        else:
            try:
                json_data = json.loads(text)
            except json.JSONDecodeError:
                json_data = text

        # 将提取的信息添加到字典中
        req_dict[request_id] = {
            'url': parsed_url.netloc,
            'path': path,
            'method': method,
            'headers': headers_dict,
            'params': params,
            'body': body
        }

        resp_dict[request_id] = {
            'status_code': status_code,
            'text': json_data
        }

    return req_dict, resp_dict


# def parse_har_file(har_file_path):
#     """
#     解析HAR文件，返回一个字典，包含请求和响应的键值对
#     :param har_file_path: HAR文件路径
#     :return: 请求和响应的字典
#     """
#     # 读取HAR文件
#     with open(har_file_path, 'r') as file:
#         har_data = json.load(file)
#
#         # 初始化请求和响应字典
#         req_dict = {}
#         resp_dict = {}
#
#         # 遍历HAR文件中的每个条目
#         for entry in har_data['log']['entries']:
#             if entry.get('_resourceType') != 'xhr':
#                 continue
#             request = entry['request']
#             response = entry['response']
#             request_id = str(len(req_dict))
#
#             # 提取请求的URL和路径
#             url = request['url']
#             parsed_url = urlparse(url)
#             path = parsed_url.path
#
#             # 提取请求方法
#             method = request['method']
#
#             # 提取请求头
#             headers = request['headers']
#             headers_dict = {}
#             for header in headers:
#                 headers_dict[header['name']] = header['value']
#
#             # 提取查询参数
#             params = {}
#             if 'queryString' in request:
#                 for param in request['queryString']:
#                     params[param['name']] = param['value']
#
#             # 提取请求体
#             body = {}
#             if 'postData' in request:
#                 post_data = request['postData']
#                 if 'text' in post_data:
#                     try:
#                         body = json.loads(post_data['text'])
#                     except json.JSONDecodeError:
#                         body = post_data['text']
#
#             # 提取响应状态码和文本
#             status_code = response['status']
#             text = response['content']['text'] if 'content' in response and 'text' in response['content'] else None
#             if text is None:
#                 json_data = None
#             else:
#                 try:
#                     json_data = json.loads(text)
#                 except json.JSONDecodeError:
#                     json_data = text
#
#             # 将提取的信息添加到字典中
#             req_dict[request_id] = {
#                 'url': parsed_url.netloc,
#                 'path': path,
#                 'method': method,
#                 'headers': headers_dict,
#                 'params': params,
#                 'body': body
#             }
#
#             resp_dict[request_id] = {
#                 'status_code': status_code,
#                 'text': json_data
#             }
#
#     return req_dict, resp_dict


def save_json(dict_data, file_path):
    """
    将数据保存为JSON文件
    :param dict_data: 数据
    :param file_path: 文件路径
    :return: None
    """
    res_str = json.dumps(dict_data, indent=4)
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(res_str)


def have_easy_har(har_file_path):
    """
    获取简化的har内容，通过交互式操作，选出要保留的请求和响应
    :param har_file_path:
    :return:
    """
    # 读取HAR文件
    with open(har_file_path, 'r') as file:
        har_data = json.load(file)

    easy_json_list = []
    index = 0
    for entry in har_data['log']['entries']:
        if entry.get('_resourceType') != 'xhr':
            continue
        index += 1
        url = entry['request']['url']
        pass_flag = False
        while pass_flag is False:
            user_input = input(f'第{index}个接口  {url} 是否需要保留？y/n:')
            if user_input.upper() in ['Y', 'YES']:
                easy_json_list.append(entry)
                pass_flag = True
            elif user_input.upper() in ['N', 'NO']:
                pass_flag = True
            else:
                print('输入错误，请重新输入，y表示保留，n表示舍弃')
    return easy_json_list


if __name__ == '__main__':
    # analysis('/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/机器人搜索.har',
    #          '/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/机器人搜索.json')
    # req_dict, resp_dict = parse_har_file(
    #     '/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/机器人搜索.har')
    # print(json.dumps(req_dict))
    # print(json.dumps(resp_dict))
    print(json.dumps(
        have_easy_har('/Users/zhangjiabin01/Desktop/new_auto/baidu/kefu-qa/bintest/har/通知机器人测一测.har')))
