# -*- coding: utf-8 -*-


# 辅助函数
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


def print_args(name, *args):
    pseudo_args = ", ".join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


class Overriding:
    """数据描述符或强制描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """没有 __get__ 方法的覆盖性描述符"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    """非数据描述符或遮盖星描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    """
    1. 覆盖型描述符的行为：
    >>> obj = Managed()
    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>,<class Managed>)

    >>> Managed.over
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)

    >>> obj.over = 7
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)

    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>,<class Managed>)

    >>> obj.__dict__['over'] = 8
    >>> vars(obj)
    {"over": 8}

    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

    2. 没有 __get__ 方法的覆盖性描述符
    >>> obj.over_no_get
    <__main__.OverridingNoGet object at 0x665bcc>

    >>> Managed.over_no_get
    __main__.OverridingNoGet object at 0x665bcc>

    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>)

    >>> obj.over_no_get
    <__main__.OverridingNoGet object at 0x665bcc>

    >>> obj.__dict__['over_no-get'] = 9
    >>> obj.over_no_get
    9

    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>)

    >>> obj.over_no_get
    9

    3. 没有__set__ 方法的描述符是非覆盖型描述符，如果设置了同名的实例属性。描述符会被遮盖，致使描述符无法处理
    那个实例的那个属性
    >>> obj = Managed()
    >>> obj.non_over
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>,<class Managed>)

    >>> obj.non_over = 7
    >>> obj.non_over
    7

    >>> Managed.non_over
    -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)

    >>> del obj.non_over
    >>> obj.non_over
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    """
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))