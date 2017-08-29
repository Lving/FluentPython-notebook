# -*- coding: utf-8 -*-
print('<[100]> evalsupport module start')


def deco_alpha(cls):
    print('<[200]> deco_alpha')  # 在模块导入时，解释器会编译函数，但是不会执行定义体

    def inner_1(self):
        print('<[300]> deco_alpha:inner_1')

    cls.method_y = inner_1
    return cls


class MetaAleph(type):
    print('<[400]> MetaAleph body')

    def __init__(cls, name, bases, dic):
        """
        编写元类时，通常self参数改成cls,清楚的表明要构建的实例是类


        """
        print('<[500]> MetaAleph.__init__')  # 类在实例话的时候，才会执行到这里

        def inner_2(self):
            print('<[600]> MetaAleph.__init__:inner_2')

        cls.method_z = inner_2

print('<[700]> evalsupport module end')
