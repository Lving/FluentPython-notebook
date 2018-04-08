# -*- coding: utf-8 -*-
from urllib.request import urlopen
import warnings
import os
import json
import codecs

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'


def load():
    if not os.path.exists(JSON):
        msg = "download {} to {}".format(URL, JSON)
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

    with codecs.open(JSON, 'rb') as fp:  # 书里又来坑我了
        return json.load(fp)





