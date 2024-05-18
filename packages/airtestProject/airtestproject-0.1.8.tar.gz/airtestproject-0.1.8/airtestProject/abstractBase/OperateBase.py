#!-*- coding = utf-8 -*-
# @Time : 2024/4/7 2:44
# @Author : 苏嘉浩
# @File : OperateBase.py
# @Software : PyCharm
from abc import ABC, abstractmethod

"""
airtest核心api的二次封装，操作具体基类
"""


class OperateABC(ABC):

    @abstractmethod
    def click(self, value, *args, **kwargs):
        """
        :param value:
        :param args:
        :param kwargs: ocrPlus=True,可以开启二值化
        :return:
        """
        pass

    @abstractmethod
    def exists(self, pos, **kwargs):
        pass

    @abstractmethod
    def sleep(self, secs):
        pass

    @abstractmethod
    def swipe(self, value, v2=None, vector_direction=None, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def pinch(self, in_or_out, pos=None, *args, **kwargs):
        pass

    @abstractmethod
    def set_text(self, pos, text, *args, **kwargs):
        pass

    @abstractmethod
    def wait(self, pos, timeout=None, *args, **kwargs):
        pass

    @abstractmethod
    def wait_disappear_element(self, pos, *args, **kwargs):
        """
        等待元素消失
        :param pos: 元素
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def wait_element_appear(self, pos, *args, **kwargs):
        pass

    @abstractmethod
    def persistent_element_exists(self, pos):
        pass

    def set_dict(self, script_root, project):
        pass

    @abstractmethod
    def wait_for_any(self, pos_list: list, timeout=30):
        pass

    @abstractmethod
    def wait_for_all(self, pos_list: list, timeout=30):
        pass

    @abstractmethod
    def wait_next_element(self, last_click_pos, next_pos):
        pass

    @abstractmethod
    def get_text(self, pos, *args, **kwargs):
        pass

# class OperateClass:
#     def __init__(self, operate: OperateABC):
#         self.operate = operate
