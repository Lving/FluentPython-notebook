# -*- coding: utf-8 -*-
import abc


class Tombola(abc.ABC):
    """
    1. 抽象方法使用@abstractclassmethod装饰，只有字符串文档
    2. 抽象基类可以包含具体方法，具体方法只能依赖抽象基类中的其他具体方法
    抽象方法或特性
    """

    @abc.abstractclassmethod
    def load(self, iterable):
        """从可第迭代对象中添加元素"""

    @abc.abstractclassmethod
    def pick(self):
        """随机删除元素"""

    def loaded(self):
        """ss"""
        return bool(self.inspect())

    def inspect(self):
        """返回有序元素"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break

        self.load(items)
        return tuple(sorted(items))


class Fake(Tombola):
    """
    1. 这是一个优缺点的子类， 因为他没有实现load方法
    2. 抽象基类的子类，一定要重写其的抽象方法, 抽象基类的具体方法可以重写，也可以不重写
    3. 抽象基类的作用可以看作是有固定接口的基类， 你在继承这个类的时候，一定要实现这些抽象方法"""
    def pick(self):
        return 13


if __name__ == '__main__':
    print(Fake)
    f = Fake()

