"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/10 16:00:00
"""
from jsonschema import validate, ValidationError

from zjbbintest.Actuator.bin_test_exception.bin_test_exception import FormatCheckException

case_json_schema = {
    "type": "object",
    "properties": {
        "caseName": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "priority": {
            "type": "integer",
        },
        "testSteps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step": {
                        "type": "integer"
                    },
                    "request": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string"
                            },
                            "path": {
                                "type": "string"
                            },
                            "method": {
                                "type": "string",
                                "enum": ["GET", "POST", "PUT", "DELETE", "HEAD",
                                         "OPTIONS", "PATCH", "CONNECT", "TRACE",
                                         "get", "post", "put", "delete", "head",
                                         "options", "patch", "connect", "trace"]
                            },
                            "headers": {
                                "type": "object"
                            },
                            "params": {
                                "type": "object"
                            },
                            "body": {
                                "type": "object"
                            }
                        },
                        "required": ["url", "path", "method"]
                    },
                    "action": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "assert": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "expect": {
                                    "type": ["string", "number", "object", "array", "boolean", "null", "integer"]
                                },
                                "actual": {
                                    "type": ["string", "number", "object", "array", "boolean", "null", "integer"]
                                },
                                "operator": {
                                    "type": "string"
                                }
                            },
                            "required": ["expect", "actual", "operator"]
                        }
                    }
                },
                "required": ["step", "request"]
            }
        }
    },
    "required": ["caseName", "priority", "testSteps"]
}


def check_case(data, case_name):
    try:
        validate(instance=data, schema=case_json_schema)
        return True
    except ValidationError as e:
        print("Validation failed.")
        print(f"Message: {e.message}")
        print(f"Schema path: {'.'.join(e.relative_schema_path)}")
        print(f"Instance path: {'.'.join(map(str, e.relative_path))}")
        raise FormatCheckException(case_name, e.context)
