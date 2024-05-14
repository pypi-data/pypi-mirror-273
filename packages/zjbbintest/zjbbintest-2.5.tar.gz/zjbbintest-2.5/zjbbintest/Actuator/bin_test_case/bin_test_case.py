"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/21 16:56:00
"""
import logging

from zjbbintest.Actuator.bin_test_exception import bin_test_exception as bt_exception
from zjbbintest.Actuator.utils.action_execution import BatchActionExecutor
from zjbbintest.Actuator.utils.assert_execution import BatchAssertExecutor
from zjbbintest.Actuator.utils.format_check import check_case
from zjbbintest.Actuator.utils.requestor import RequestObject
from enum import Enum
import json


class CaseRunStatus(Enum):
    """
    case执行状态枚举，
    0：未执行，属于未执行状态
    200：case执行通过，属于成功状态
    500：case未执行通过，断言失败，属于失败状态
    501：请求异常，属于失败状态
    401：case格式检查异常，属于跳过状态
    402：case中的BT字符串格式异常，属于跳过状态
    403：case中bt-func未找到异常，属于跳过状态
    404：case中bt-action未找到异常，属于跳过状态
    405: case中bt-assert未找到异常，属于跳过状态
    406: case中bt-func格式检查异常，属于跳过状态
    407：case中bt-action格式检查异常，属于跳过状态
    408：case中bt-assert格式检查异常，属于跳过状态
    409：case的assert的dict格式存在问题，属于跳过状态
    410：case信息为空，属于跳过状态
    999：其他异常，属于跳过状态
    """
    NOT_RUNNING = 0
    PASS = 200
    FAIL = 500
    REQUEST_EXCEPTION = 501
    CASE_FORMAT_CHECK_ERROR = 401
    BT_STRING_FORMAT_ERROR = 402
    BT_FUNC_NOT_FOUND = 403
    BT_ACTION_NOT_FOUND = 404
    BT_ASSERT_NOT_FOUND = 405
    BT_FUNC_FORMAT_CHECK_ERROR = 406
    BT_ACTION_FORMAT_CHECK_ERROR = 407
    BT_ASSERT_FORMAT_CHECK_ERROR = 408
    ASSERT_DICT_FORMAT_ERROR = 409
    CASE_INFO_IS_EMPTY = 410
    OTHER_EXCEPTION = 999


class BinTestCase:
    """
    case的执行空间，case的执行依靠这个对象
    case空间的内容有几部分
    1.case_name: case名称
    2.case_desc: case详情
    3.case_steps: case执行步骤，主要逻辑都在里面
    4.case_var_dict: case执行过程中记录的变量
    """

    def __init__(self, case_name="", case_desc="", priority="", case_mack_labels=[], case_steps=[],
                 case_run_status=CaseRunStatus.NOT_RUNNING, case_run_msg="未执行",
                 case_var_dict={}, req_dict={}, resp_dict={}):
        self.case_name = case_name
        self.case_desc = case_desc
        self.priority = priority
        self.case_mack_labels = case_mack_labels
        self.case_steps = case_steps
        # 下面四个是在创建之初没有的，在执行过程中会添加进去
        self.case_run_status = case_run_status
        self.case_run_msg = case_run_msg
        self.case_var_dict = case_var_dict
        self.req_dict = req_dict
        self.resp_dict = resp_dict

    @staticmethod
    def create_obj_by_dict(case_space_dict):
        """
        根据字典创建caseSpace对象
        :param case_space_dict:
        :return:
        """
        # 1.格式检查
        case_name = case_space_dict.get("caseName") if case_space_dict.get("caseName") else "QAQ case名称不存在"
        try:
            check_case(case_space_dict, case_name)
        except bt_exception.FormatCheckException as e:
            case_run_status = CaseRunStatus.CASE_FORMAT_CHECK_ERROR
            case_run_msg = str(e.message)
            return BinTestCase(case_name=case_name, case_run_status=case_run_status, case_run_msg=case_run_msg)
        case_desc = case_space_dict.get("description")
        priority = case_space_dict.get("priority")
        case_mack_labels = case_space_dict.get("mark")
        case_steps = case_space_dict.get("testSteps")
        case_step_list = []
        for case_step in case_steps:
            case_step_obj = CaseStep.create_obj_by_dict(case_step)
            case_step_list.append(case_step_obj)
        return BinTestCase(case_name=case_name, case_desc=case_desc, priority=priority,
                           case_mack_labels=case_mack_labels, case_steps=case_step_list)

    def run(self):
        """
        执行case
        :return:
        """
        logging.debug(f"开始执行case: {self.case_name}")
        # 判断case是否可以执行
        if self.case_run_status != CaseRunStatus.NOT_RUNNING:
            logging.info(f"case: {self.case_name} 已经执行过了，不能重复执行")
            # 不是未执行状态，说明执行过（有问题），不能重复执行
            return
        # 初始化case_var_dict
        self.case_var_dict = {}
        # 请求和响应的list
        self.req_dict = {}
        self.resp_dict = {}
        case_step_run_res = {}
        # print(self.case_steps)
        exception_flag = False
        # 执行case步骤
        logging.debug(f"------------------开始执行case步骤-----------------------")
        try:
            for case_step in self.case_steps:
                # TODO 执行case步骤的时候，需要把case_var_dict传进去，也需要请求和响应的list，这里需要补充一下
                # DONE 2024-05-05
                run_res, self.case_var_dict, self.req_dict, self.resp_dict = case_step.run(self.case_var_dict,
                                                                                           self.req_dict,
                                                                                           self.resp_dict)
                logging.debug(f"case_step: {case_step.step_id} 执行结果为：{run_res}")
                logging.debug(f"case_var_dict: {self.case_var_dict}")
                logging.debug(f"req_list: {self.req_dict}")
                logging.debug(f"resp_list: {self.resp_dict}")
                case_step_run_res[case_step.step_id] = run_res

        except (bt_exception.AssertFailException, AssertionError) as e:
            self.case_run_status = CaseRunStatus.FAIL
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.RequestException as e:
            self.case_run_status = CaseRunStatus.REQUEST_EXCEPTION
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.FormatCheckException as e:
            self.case_run_status = CaseRunStatus.BT_STRING_FORMAT_ERROR
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTFuncNotFoundException as e:
            self.case_run_status = CaseRunStatus.BT_FUNC_NOT_FOUND
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTActionNotFoundException as e:
            self.case_run_status = CaseRunStatus.BT_ACTION_NOT_FOUND
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTAssertNotFoundException as e:
            self.case_run_status = CaseRunStatus.BT_ASSERT_NOT_FOUND
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTFuncFormatCheckException as e:
            self.case_run_status = CaseRunStatus.BT_FUNC_FORMAT_CHECK_ERROR
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTActionFormatCheckException as e:
            self.case_run_status = CaseRunStatus.BT_ACTION_FORMAT_CHECK_ERROR
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTAssertFormatCheckException as e:
            self.case_run_status = CaseRunStatus.BT_ASSERT_FORMAT_CHECK_ERROR
            self.case_run_msg = str(e.message)
            exception_flag = True
        except bt_exception.BTAssertDictFormatException as e:
            self.case_run_status = CaseRunStatus.ASSERT_DICT_FORMAT_ERROR
            self.case_run_msg = str(e.message)
            exception_flag = True
        except Exception as e:
            exception_flag = True
            logging.exception(e)
            self.case_run_status = CaseRunStatus.OTHER_EXCEPTION
            self.case_run_msg = str(e)
        if not exception_flag:
            if len(case_step_run_res.items()) == len(self.case_steps) \
                    and all(case_step_run_res.values()):
                self.case_run_status = CaseRunStatus.PASS
                self.case_run_msg = "执行成功"
            else:
                self.case_run_status = CaseRunStatus.FAIL
                self.case_run_msg = "执行失败"
        return {
            "case_name": self.case_name,
            "case_desc": self.case_desc,
            "priority": self.priority,
            "mark": self.case_mack_labels,
            "run_status": self.case_run_status.value,
            "run_msg": self.case_run_msg
        }


class CaseStep:
    """
    case单个步骤对象
    case单个步骤的内容有几部分
    1.请求:dict
    2.动作:list
    3.断言:list
    """

    def __init__(self, step_id, request_obj, action_list, assert_list):
        self.step_id = step_id
        self.request_obj = request_obj
        self.action_list = action_list
        self.assert_list = assert_list

    def __str__(self):
        # return f"CaseStep(request_obj={str(self.request_obj)}, " \
        #        f"action_list={str(self.action_list)}, " \
        #        f"assert_list={str(self.assert_list)})"
        return f"""
            {{
                "CaseStep": {{
                    "request_obj" : {str(self.request_obj)},
                    "action_list" : {json.dumps(self.action_list)},
                    "assert_list" : {json.dumps(self.assert_list)}
                }}
            }}"""

    @staticmethod
    def create_obj_by_dict(case_step_dict):
        """
        根据字典创建caseStep对象
        :param case_step_dict:
        :return:
        """
        step_id = case_step_dict.get("step")
        request_dict = case_step_dict.get("request")
        request_obj = RequestObject.create_obj_by_dict(request_dict)
        actions = case_step_dict.get("action")
        action_list = BatchActionExecutor(actions)
        asserts = case_step_dict.get("assert")
        assert_list = BatchAssertExecutor(asserts)
        return CaseStep(step_id, request_obj, action_list, assert_list)

    def run(self, case_var_dict, req_dict, resp_dict):
        """
        执行case步骤
        :return:
        """
        # 请求
        bt_resp = self.request_obj.send(case_var_dict, req_dict, resp_dict)
        # 此时，self.request_obj已经完成了其中变量的替换，可以使用obj_to_dict()将其转为字典
        req_dict[str(self.step_id)] = self.request_obj.obj_to_dict()
        req_dict[str(self.step_id)] = bt_resp.obj_to_dict()
        # 动作
        case_var_dict = self.action_list.execute(case_var_dict, req_dict, resp_dict)
        # 断言
        # TODO 断言的执行也需要case_var_dict, req_list, resp_list
        # DONE 2024-05-05
        step_run_res = self.assert_list.execute(case_var_dict, req_dict, resp_dict)
        return step_run_res, case_var_dict, req_dict, resp_dict


if __name__ == '__main__':
    # request = RequestObject("https://aiob-open.baidu.com", "/aiob-server/api/v2/getToken", "POST",
    #                         {'Content-Type': 'application/json'}, {}, {
    #                             "accessKey": "dfc272b758fb451cb5d409d6bf04b40e",
    #                             "secretKey": "561f119cea874a37a81a1e83c9e1b92d"
    #                         })
    # request_dict = request.obj_to_dict()
    # print(request_dict)
    # step_dict = {}
    # step_dict["request"] = request_dict
    # step_dict["action"] = ["", ""]
    # step_dict["assert"] = [
    #     {
    #         "expect": 200,
    #         "actual": 200,
    #         "operator": "=="
    #     },
    #     {
    #         "expect": "success",
    #         "actual": "success",
    #         "operator": "=="
    #     },
    #     {
    #         "expect": {
    #             "key": "value"
    #         },
    #         "actual": {
    #             "key": "value"
    #         },
    #         "operator": "=="
    #     }
    # ]
    # json_data = json.dumps(step_dict)
    # step = CaseStep.create_obj_by_dict(step_dict)
    # print(step.run({}))
    json_data = """{
  "caseName": "测试案例1",
  "description": "这是测试案例描述",
  "priority": 0,
  "testSteps": [
    {
      "step": 1,
      "request": {
        "url": "https://aiob-open.baidu.com",
        "path": "/aiob-server/api/v2/getToken",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "param": {
          
        },
        "body": {
          "accessKey": "dfc272b758fb451cb5d409d6bf04b40e",
          "secretKey": "561f119cea874a37a81a1e83c9e1b92d"
        }
      },
      "action": [
        "",
        ""
      ],
      "assert": [
        {
          "expect": 200,
          "actual": 200,
          "operator": "=="
        },
        {
          "expect": "success",
          "actual": "success",
          "operator": "=="
        },
        {
          "expect": {
            "key": "value"
          },
          "actual": {
            "key": "value"
          },
          "operator": "=="
        }
      ]
    }
  ]
}"""
    data = json.loads(json_data)
    bt_case = BinTestCase.create_obj_by_dict(data)
    bt_case.run()
    print(bt_case.case_run_status)
    print(bt_case.case_run_msg)
