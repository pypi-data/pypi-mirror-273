"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/10 20:25:00
"""
from urllib.parse import urljoin
import requests
import json

from zjbbintest.Actuator.bin_test_exception.bin_test_exception import RequestException
from zjbbintest.Actuator.utils.string_dynamic_run import StringDynamicRun


class RequestObject:
    """
    将请求封装成一个对象，方便后续处理
    """

    def __init__(self, url, path, method, headers={}, params={}, body={}):
        self.url = url
        self.path = path
        self.method = method.upper()
        self.headers = convert_to_str(headers)
        self.params = convert_to_str(params)
        self.body = body

    @staticmethod
    def create_obj_by_dict(request_dict):
        """
        根据字典创建RequestObject对象
        :param request_dict:
        :return: RequestObject
        """
        url = request_dict.get("url")
        path = request_dict.get("path")
        method = request_dict.get("method")
        headers = convert_to_str(request_dict.get("headers"))
        params = convert_to_str(request_dict.get("params"))
        body = request_dict.get("body")
        return RequestObject(url, path, method, headers, params, body)

    def replace(self, case_var_dict, req_dict, resp_dict):
        """
        替换url、path、headers、params、body中的动态变量
        :return: dict
        """
        # 执行url中的动态变量
        executed_url, _ = StringDynamicRun(self.url, case_var_dict, req_dict, resp_dict).run()
        headers = self.headers
        # 执行headers中的动态变量
        executed_headers = {}
        for key, value in headers.items():
            executed_key, _ = StringDynamicRun(key, case_var_dict, req_dict, resp_dict).run()
            executed_value, _ = StringDynamicRun(value, case_var_dict, req_dict, resp_dict).run()
            executed_headers[executed_key] = executed_value
        params = self.params
        # 执行params中的动态变量
        executed_params = {}
        if params:
            for key, value in params.items():
                executed_key, _ = StringDynamicRun(key, case_var_dict, req_dict, resp_dict).run()
                executed_value, _ = StringDynamicRun(value, case_var_dict, req_dict, resp_dict).run()
                executed_params[executed_key] = executed_value
        body = self.body
        # 执行body中的动态变量
        executed_body = {}
        if body:
            for key, value in body.items():
                if isinstance(key, str):
                    executed_key, _ = StringDynamicRun(key, case_var_dict, req_dict, resp_dict).run()
                else:
                    executed_key = key
                if isinstance(value, str):
                    executed_value, _ = StringDynamicRun(value, case_var_dict, req_dict, resp_dict).run()
                else:
                    executed_value = value
                executed_body[executed_key] = executed_value
        self.url = executed_url
        self.path = self.path
        self.method = self.method
        self.headers = executed_headers
        self.params = executed_params
        self.body = executed_body

    def send(self, case_var_dict, req_dict, resp_dict):
        """
        发送请求，返回响应对象
        :return: ResponseObject
        """
        self.replace(case_var_dict, req_dict, resp_dict)
        url = urljoin(self.url, self.path)
        try:
            print(f"发起请求，请求信息为:{self}")
            response = requests.request(self.method, url, headers=self.headers,
                                        params=self.params, data=json.dumps(self.body))
        except Exception as e:
            raise RequestException(f"请求{self}失败，失败原因:{e}")
        response = ResponseObject(response.status_code, response.text, response.content, response.headers)
        print(f"请求成功，响应信息为:{response}")
        return response

    def __str__(self):
        # return f"RequestObject(url={self.url},path={self.path}," \
        #        f"method={self.method},headers={json.dumps(self.headers)}," \
        #        f"params={json.dumps(self.params)},body={json.dumps(self.body)}) "
        return f"""
{{
    "RequestObject" : {{
        "url": "{self.url}",
        "path": "{self.path}",
        "method": "{self.method}",
        "headers": {json.dumps(self.headers)},
        "params": {json.dumps(self.params)},
        "body": {json.dumps(self.body)}
    }}
}}
"""

    def obj_to_dict(self):
        """
        将对象转化为字典
        :return: dict
        """
        return {
            "url": self.url,
            "path": self.path,
            "method": self.method,
            "headers": self.headers,
            "params": self.params,
            "body": self.body
        }


class ResponseObject:
    """
    将响应封装成一个对象，方便后续处理
    """

    def __init__(self, status_code, text, content, response_headers):
        self.status_code = status_code
        self.text = text
        self.content = content
        self.response_headers = dict(response_headers)

    def __repr__(self):
        return f"""
            {{
                "ResponseObject": {{
                    "status_code": {self.status_code},
                    "text": "{self.text}",
                    "content": "{self.content}",
                    "response_headers": {json.dumps(self.response_headers)}
            }}
            """

    def __str__(self):
        # return f"ResponseObject(status_code={self.status_code},text={self.text}," \
        #        f"content={self.content},response_headers={json.dumps(self.response_headers)})"
        return f"""
            {{
                "ResponseObject": {{
                    "status_code": {self.status_code},
                    "text": "{self.text}",
                    "content": "{self.content}",
                    "response_headers": {json.dumps(self.response_headers)}
            }}
            """

    def obj_to_dict(self):
        """
        将对象转化为字典
        :return: dict
        """
        if isinstance(self.content, bytes):
            self.content = self.content.decode("utf-8")
        if isinstance(self.text, bytes):
            self.text = self.text.decode("utf-8")
        try:
            self.content = json.loads(self.content)
            self.text = json.loads(self.text)
        except Exception as e:
            print(f"解析响应内容失败，原因：{e}")
            pass
        return {
            "status_code": self.status_code,
            "text": self.text
            # "content": self.content,
            # "response_headers": self.response_headers
        }


def convert_to_str(dictionary):
    """
    将字典中的key和value都转化为字符串
    :param dictionary:
    :return:
    """
    if dictionary is None:
        return {}
    new_dict = {}
    for key, value in dictionary.items():
        new_key = str(key) if not isinstance(key, str) else key
        new_value = str(value) if not isinstance(value, str) else value
        new_dict[new_key] = new_value
    return new_dict


class Requestor:
    """
    请求器，用于发送请求
    """

    def send(self, request_dict):
        """
        发送请求，返回响应对象
        :param request_dict: 请求信息
        :return: ResponseObject
        """


if __name__ == '__main__':
    pass
