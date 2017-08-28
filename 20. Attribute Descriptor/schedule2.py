# -*- coding: utf-8 -*-
"""
本章目前所举的实例是为了展示如何使用基本的工具，如：
__getattr__ 方法， hasattr 函数， getattr 函数， @property 装饰器
和__dict__属性，来实现动态属性
"""
import warnings
import inspect  #1

import osconfeed

DB_NAME = 'data/schedule2_db' # 2
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):  # 3
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


class MissingDatabaseError(RuntimeError):
    """"""


class DbRecord(Record): # 2
    __db = None  # 3  # 存储一个打开的shelve.Sheld 数据库引用

    @staticmethod # 4
    def set_db(db):
        DbRecord.__db = db # 5

    @staticmethod # 6
    def get_db():
        return DbRecord.__db

    @classmethod # 7
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]  # 8
        except TypeError:
            if db is None:  # 9
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
        else:  # 10
            raise

    def __repr__(self):
        if hasattr(self, 'serial'):  # 11
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  # 12


class Event(DbRecord):
    """
    >> DbRecord.set_db(db)
    >> event = DbRecord.fetch('event.33950')
    >> event
    <Event 'There *Will* Be Bugs'>
    >> event.venue
    <DbRecord serial='venue.1449'>
    >> event.venue.name
    'Portland 251'

    """
    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speakers_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch  # 防止event实例中，有fetch字段， 这样的话，self.fetch调用的就不是DbRecord的方法了
            self._speaker_objs = [
                fetch('speakers.{}'.format(key)) for key in spkr_serials
            ]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


def load_db(db):
    raw_data = osconfeed.load()
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1] # 1
        cls_name = record_type.capitalize() # 2 首字母大写，获取可能的类名
        cls = globals().get(cls_name, DbRecord) # 3 从全局作用域中获取那个名称对应的对象，默认使用DbRecord
        if inspect.isclass(cls) and issubclass(cls, DbRecord): # 4 获取的对象是类 且是DbRecord的子类
            factory = cls # 5  把对象复制给factory变量。因此，factory的值可能是DbRecord的任何一个子类，具体取决域record_type
        else:
            factory = DbRecord  # 6
        for record in rec_list: # 7
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  # 8