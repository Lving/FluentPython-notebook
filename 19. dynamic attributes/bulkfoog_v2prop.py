# -*- coding: utf-8 -*-


def quantity(stoarge_name):

    def qty_getter(instance):
        return instance.__dict__[stoarge_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[stoarge_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, des, weight, price):
        self.des = des
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
    print(nutmeg.weight)
    print(nutmeg.price)

    print(vars(nutmeg))



