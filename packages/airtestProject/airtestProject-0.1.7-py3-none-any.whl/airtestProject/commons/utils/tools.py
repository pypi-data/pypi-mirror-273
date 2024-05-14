#!-*- coding = utf-8 -*-
# @Time : 2024/4/7 2:44
# @Author : 苏嘉浩
# @File : OperateBase.py
# @Software : PyCharm
import os


def get_folder_path_up(current_path, folder_name):
    """
    向上寻找文件夹路径，找到后返回对应路径。
    :param current_path: 当前文件路径
    :param folder_name: 需要寻找的文件夹名字
    :return: 返回找到的文件夹
    """
    result_path = os.path.dirname(os.path.abspath(current_path))
    while True:
        if os.path.exists(os.path.join(result_path, folder_name)):
            # 当前文件路径下有对应文件夹路径
            result_path = os.path.join(result_path, folder_name)
            break
        elif result_path == os.path.dirname(result_path):
            # 去到根目录还未找到文件夹路径
            raise Exception(f"未找到 '{folder_name}' 文件夹，需要在根目录下创建{folder_name}文件夹")
        else:
            # 向上查找文件夹路径
            result_path = os.path.dirname(result_path)
    return result_path


def get_folder_path_down(current_path, folder_name):
    # 检查当前路径下是否有 'img' 文件夹
    if folder_name in os.listdir(current_path):
        return os.path.join(current_path, folder_name)

    # 在每个子目录中递归查找
    for subdir in os.listdir(current_path):
        full_subdir = os.path.join(current_path, subdir)
        if os.path.isdir(full_subdir):
            result = get_folder_path_down(current_path, folder_name)
            if result is not None:
                return result

    # 如果在当前路径及其所有子目录中都没有找到 'img' 文件夹，返回 None
    return None
