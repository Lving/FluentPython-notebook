# -*- coding: utf-8 -*-
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


if __name__ == '__main__':
    # 因为实现了__getitem__方法， 所以这个对象是可以迭代的
    s = Sentence('"The time has come, " the Walrus said,')
    for w in s:
        print(w)
    print(s)