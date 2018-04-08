# -*- coding: utf-8 -*-
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight, set_weight)


if __name__ == '__main__':
    ll = LineItem('walnuts', 3, 10)
    print(id(ll.get_weight()))
    print(id(ll.weight))