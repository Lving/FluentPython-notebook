# -*- coding: utf-8 -*-
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        """
        我也可以把next的方法写到这个类里面, 但是书上说这是常见的反模式。
        迭代器模型：为了遍历不同的聚合结构提供一个统一的接口，为了支持这种遍历
        必须能从同一个可迭代的实例内部获取多个独立的迭代器，这就是实现SentenceIterator的原因
        """
        return SentenceIterator(self.words)


class SentenceIterator:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self


