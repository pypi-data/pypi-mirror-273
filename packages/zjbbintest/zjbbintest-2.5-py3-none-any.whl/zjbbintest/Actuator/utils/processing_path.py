"""
Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
This module provide configigure file management service in i18n environment.

Authors: zhangjiabin01
Date: 2024/4/22 17:41:21
"""
import os


def get_json_files_in_directories(path_list):
    # 初始化一个list来存储所有.json文件的绝对路径
    file_list = []

    for path in path_list:
        # 判断path是不是文件，如果是则直接添加到list
        if os.path.isfile(path) and os.path.splitext(path)[1] == '.json':
            file_list.append(path)
            continue

        # 使用os.walk遍历目录下所有子文件和子文件夹
        for dir_path, dir_names, filenames in os.walk(path):
            for filename in filenames:
                # 只有当文件是.json文件时，才添加文件的绝对路径到list中
                if os.path.splitext(filename)[1] == '.json':
                    file_list.append(os.path.join(dir_path, filename))

    return file_list

if __name__ == '__main__':
    path_list = ['/Users/zhangjiabin01/Downloads']
    print(get_json_files_in_directories(path_list))
