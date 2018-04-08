# -*- coding: utf-8 -*-
class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        # 每个描述符实例的storage_name属性都是独一无二的，
        # 因为其值由描述符的名称和__counter属性的当前值构成 （_Quantity#0）
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1  # 这里是对类属性自增 而不是实例属性

    def __get__(self, instance, owner):
        """
         instance:
         owner:  托管类的引用， 通过描述符从托管类中获取属性时用得到
        """
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price