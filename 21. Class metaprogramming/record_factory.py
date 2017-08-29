# -*- coding: utf-8 -*-


def record_factory(cls_name, field_names):
    """
    :param cls_name:
    :param field_names:
    :return:

    >>> Dog = record_factory('Dog', 'name weight owner')
    >>> rex = Dog('Rex', 30, 'Bob')
    >>> rex
    Dog(name='Rex', weight=30, owner='Bob')
    >>> Dog.__mro__
    (<class 'factories.Dog'>, <class 'object'>)

    """
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass

    field_names = tuple(field_names)

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):  # 所有的self都不是这个函数的self, 而是即将要构造的类中的self
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ", ".join('{}={!r}'.format(*i) for i
                           in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    # 组建类属性字典
    cls_attrs = dict(
        __slots__=field_names,
        __init__=__init__,
        __iter__=__iter__,
        __repr__=__repr__
    )

    return type(cls_name, (object, ), cls_attrs)  # cls_attrs  构造返回的类的方法
    # MyClass= type('MyClass', (MySuperClass, MyMixin), {'x': 42, 'x2': lambda self: self.x*2})