# -*- coding: utf-8 -*-

class LineItem:
    """
    >> ll = LineItem('some', 2, 3)
    >> ll.weight = 2

    >> ll.weight = 5
    >> ll.weight = 5  __weight 屏蔽了weight?
    """
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property   # 装饰读值方法
    def weight(self):
        return self.__weight

    @weight.setter  # 被装饰的方法有 .setter属性；这个装时期把读值方法和设值方法绑定在一起
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')
