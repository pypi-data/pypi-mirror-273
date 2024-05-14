"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/20 17:33:00
"""
from zjbbintest.Actuator.utils.string_dynamic_run import StringDynamicRun
from zjbbintest.bintest_data import BinTestData
from zjbbintest.Actuator.bin_test_exception.bin_test_exception import AssertFailException, BTAssertNotFoundException, BTAssertDictFormatException


class AssertDict:
    """
    常见断言字典
    """
    EQUALS = ["=", "==", "相等", "等于", "一致", "一样"]
    NOT_EQUALS = ["!=", "不等于", "不等", "不一致", "不一样"]
    GREATER = [">", "大于"]
    LESS = ["<", "小于"]
    GREATER_EQUALS = [">=", "大于等于"]
    LESS_EQUALS = ["<=", "小于等于"]
    IN = ["in", "包含", "属于"]
    NOT_IN = ["not in", "不包含", "不属于"]


class AssertExecutor:
    """
    断言执行器，执行单个断言
    """

    def __init__(self, expect_data, actual_data, assert_name):
        self.expect_data = expect_data
        self.actual_data = actual_data
        self.assert_name = assert_name

    def execute(self):
        """
        执行单个断言
        :return:
        """
        try:
            if self.assert_name in AssertDict.EQUALS:
                assert self.expect_data == self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                             f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.NOT_EQUALS:
                assert self.expect_data != self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                             f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.GREATER:
                assert self.expect_data > self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                            f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.LESS:
                assert self.expect_data < self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                            f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.GREATER_EQUALS:
                assert self.expect_data >= self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                             f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.LESS_EQUALS:
                assert self.expect_data <= self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                             f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.IN:
                assert self.expect_data in self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                             f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            elif self.assert_name in AssertDict.NOT_IN:
                assert self.expect_data not in self.actual_data, f"进行'{self.assert_name}'断言失败" \
                                                                 f"，期望值：{self.expect_data}，实际值：{self.actual_data}"
            else:
                try:
                    assert_res = BinTestData.assert_dict.get(self.assert_name)(self.expect_data, self.actual_data)
                    if not assert_res:
                        raise AssertFailException(self.expect_data, self.actual_data, self.assert_name)
                    else:
                        return assert_res
                except TypeError as e:
                    raise BTAssertNotFoundException(self.assert_name)
            return True
        except AssertionError as e:
            raise AssertFailException(self.expect_data, self.actual_data, self.assert_name)

    def __str__(self):
        """
        :return:
        """
        return f"expect: {self.expect_data}, actual: {self.actual_data}, assert: {self.assert_name}"

    def replace(self, case_var_dict, req_dict, resp_dict):
        """
        替换断言中的变量
        :param case_var_dict:
        :param req_dict:
        :param resp_dict:
        :return:
        """
        self.expect_data, _ = StringDynamicRun(self.expect_data, case_var_dict, req_dict, resp_dict).run()
        self.actual_data, _ = StringDynamicRun(self.actual_data, case_var_dict, req_dict, resp_dict).run()

    @staticmethod
    def create_obj_by_dict(assert_dict):
        """
        根据断言字典创建断言对象
        :param assert_dict:
        :return:
        """
        assert_name = assert_dict.get("operator")
        expect_data = assert_dict.get("expect")
        actual_data = assert_dict.get("actual")
        if expect_data is None or expect_data == "":
            raise BTAssertDictFormatException(assert_dict, "expect")
        if assert_name is None or assert_name == "":
            raise BTAssertDictFormatException(assert_dict, "operator")
        if actual_data is None or actual_data == "":
            raise BTAssertDictFormatException(assert_dict, "actual")
        return AssertExecutor(expect_data, actual_data, assert_name)


class BatchAssertExecutor:
    """
    批量断言执行器
    处理一个测试用例中一个步骤里的多条断言
    """

    def __init__(self, assert_list):
        self.__assert_list = assert_list

    def execute(self, case_var_dict, req_dict, resp_dict):
        """
        批量执行断言
        :return:
        """
        execute_res_list = []
        for assert_dict in self.__assert_list:
            # 1.创建单个断言执行对象
            assert_executor = AssertExecutor.create_obj_by_dict(assert_dict)
            # 2.替换变量
            assert_executor.replace(case_var_dict, req_dict, resp_dict)
            # 3.执行
            assert_res = assert_executor.execute()
            # 4.内容存放
            execute_res_list.append(assert_res)
        return all(execute_res_list)
