# -*- coding: utf-8 -*-
class Quantity:  # 1
    """
    描述符协议的类
    """
    def __init__(self, storage_name):
        self.storage_name = storage_name # 2

    def __set__(self, instance, value): # 3 尝试为托管属性赋值时，会调用__set__方法
        """
        self 是描述符实例
        instance 是托管实例
        """
        if value > 0:
            instance.__dict__[self.storage_name] = value  # 4  必须直接处理托管实例的__dict__属性；如果使用内置的setattr,
                                                          # 会再次触发__set__方法，导致无限递归
        else:
            raise ValueError('value must be > 0')


class LineItem:
    """
    托管类：把描述符实例声明为类属性的类
    """
    weight = Quantity('weight')  # 存储属性   # 5
    price = Quantity('price')   # 存储属性  6

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price