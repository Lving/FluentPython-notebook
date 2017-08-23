# -*- coding: utf-8 -*-
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# 子生成器
def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # 书中的代码这里有错误


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from average() # yield from 会等待average给自己返回值？？


# 调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            # grouper 发送的每个值都会经由yield from 处理，通过管道传给average实例
            # grouper会在yield from表达式处暂停，等待average实例处理客户端发来的值，
            # average实例运行完毕后，返回的值绑定到results[key]上。
            # while循环会不断创建average实例，处理更多的值
            group.send(value)
        group.send(None)  # 这一行很重要
        # 假如去掉的话：内层循环结束的时候，group实例依旧在yield from 表达式处暂停，
        # 所以委派生成器中的results[key] 复制语句就无法执行

    print(results)
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))


data = {'girls;kg': [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
        'girls;m': [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
        'boys;kg': [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
        'boys;m': [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
        }


if __name__ == '__main__':
    main(data)