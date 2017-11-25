#!/usr/bin/env python
# coding=utf-8
#    Anormaly Detection Configure
#    C19<caoyijun2050@gmail.com>

import json
import os
import redis
from base import do

__all__ = ['Config', 'set_config']

Config = None


def set_config(conf):
    global Config
    Config = do(__file__,
                os.path.dirname,
                lambda path: os.path.join(path, conf),
                open,
                json.load,
                )
    return Config
