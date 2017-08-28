# -*- coding: utf-8 -*-
import keyword
from collections import abc


class FrozenJSON:
    """
    一个只读接口，使用属性标识访问JSON类对象
    """
    def __init__(self, mapping):
        self.data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.data[key] = value

    # __getattr__() is a special method function that you can define.
    # When a member lookup fails, this function will be called.
    def __getattr__(self, name): # 这个类有没有`name`属性？
        if hasattr(self.data, name):
            return getattr(self.data, name)
        else:   # 没有， 建造FrozenJSON对象
            return FrozenJSON.build(self.data[name])  # 将每一层嵌套都转换成一个FrozenJSON

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):  # 是映射，转换成FrozenJSON对象
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence): # 是列表，将列表的每一个元素进行转换，
            return [cls.build(item) for item in obj]
        else:
            return obj



