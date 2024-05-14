"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/10 16:00:00
"""


class RequestException(Exception):
    """
    RequestException class.
    请求过程中异常
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FormatCheckException(Exception):
    """
    FormatCheckException class.
    case格式检查异常
    """

    def __init__(self, case_name, context):
        self.message = f'case: {case_name} 格式检查失败，请检查case的格式是否正确，具体信息如下：{context}'
        super().__init__(self.message)


class FormatBTStringException(Exception):
    """
    FormatBTStringException class.
    字符串格式异常
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BTFuncNotFoundException(Exception):
    """
    BTFuncNotFoundException class.
    bt_func方法未找到异常
    """

    def __init__(self, func_name):
        self.message = f'方法"{func_name}"不存在，请先使用@bt_func进行方法注册'
        super().__init__(self.message)


class BTActionNotFoundException(Exception):
    """
    BTActionNotFoundException class.
    bt_action方法未找到异常
    """

    def __init__(self, action_name):
        self.message = f'动作"{action_name}"不存在，请先使用@bt_action进行动作注册'
        super().__init__(self.message)


class BTAssertNotFoundException(Exception):
    """
    BTAssertNotFoundException class.
    bt_assert方法未找到异常
    """

    def __init__(self, assert_name):
        self.message = f'断言方法"{assert_name}"不存在，请先使用@bt_assert进行断言方法注册'
        super().__init__(self.message)


class BTFuncFormatCheckException(Exception):
    """
    BTFuncFormatCheckException class.
    bt_func方法格式检查异常
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BTActionFormatCheckException(Exception):
    """
    BTActionFormatCheckException class.
    bt_action方法格式检查异常
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BTAssertFormatCheckException(Exception):
    """
    BTAssertFormatCheckException class.
    bt_assert方法格式检查异常
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AssertFailException(Exception):
    """
    AssertFailException class.
    断言失败异常
    """

    def __init__(self, expect_data, actual_data, assert_name):
        self.message = f'执行"{assert_name}"断言失败' \
                       f'\nexpect: {expect_data}' \
                       f'\nassert: {actual_data}'
        super().__init__(self.message)


class BTAssertDictFormatException(Exception):
    """
    BTAssertDictFormatException class.
    Assert的dict格式存在问题，可能是缺少expect、actual、operator中的某些字段
    """

    def __init__(self, assert_dict, missing_item):
        self.message = f'断言 {assert_dict} 格式存在问题，缺少字段"{missing_item}"'
        super().__init__(self.message)


class BTCaseNotLoadException(Exception):
    """
    BTCaseNotLoadException class.
    case文件不存在异常
    """
    def __init__(self):
        self.message = 'case文件为加载，请先使用bintest.case_load()加载'
        super().__init__(self.message)
