# -*- coding: utf-8 -*-
import abc


class AutoStorage:  # 1
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = "_{}#{}".format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)  # 2


class Validated(abc.ABC, AutoStorage):  # 3
    """
    Quantity 和 NonBlank 都用到 __set__, 而__set__ 又会被委托给validate
    这两个继承AutoStorage后 只需要重写validate方法即可

    验证没问题， 通过super委托给基类处理

    妙啊
    """
    def __set__(self, instance, value):
        value = self.validate(instance, value) # 4
        super().__set__(instance, value)  # 5

    @abc.abstractclassmethod
    def validate(self, instance, value):    # 6 # 抽象方法
        """return validated value or raise ValueError"""


class Quantity(Validated):  # 7
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cant be empty or blank')
        return value  # 8