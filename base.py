#!/usr/bin/env python
# coding=utf-8
#    some helper functions
#    C19<caoyijun2050@gmail.com>

import time
import pdb
from collections import OrderedDict, Iterable
import xxhash as _xxhash

xxhash = lambda x: _xxhash.xxh64(ensure_utf8(x)).hexdigest()


class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


def none_on_error(func, *arg, **kwarg):
    try:
        return func(*arg, **kwarg)
    except Exception as e:
        print(e)
        return None


unzip = lambda x: zip(*x)


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for elem in flatten(x):
                yield elem
        else:
            yield x


def chain(*funcs):
    def wrap(*arg, **kwarg):
        result = funcs[0](*arg, **kwarg)
        for func in funcs[1:]:
            result = func(result)
        return result

    return wrap


def do(*arg):
    param, actions = arg[0], arg[1:]
    for action in actions:
        param = action(param)
    return param


def curry_filter(func):
    return lambda x: filter(func, x)


def curry_map(func):
    return lambda x: map(func, x)


def breakpoint(arg):
    pdb.set_trace()
    return arg


def lazydo(*arg):
    def func():
        param, actions = arg[0], arg[1:]
        for action in actions:
            param = action(param)
        return param

    return func


def update(dict1, dict2):
    dict1.update(dict2)
    return dict1


# cache part
def clear_cache(func):
    if 'cached' in func.__dict__:
        del func.cached
        print("{0}'s cache cleared.".format(func.__name__))
    else:
        print("{0} has no cache.".format(func.__name__))


def clear_all_cache(funcs):
    map(clear_cache, funcs)


def cache(func):
    cache.cached_funcs.add(func)

    def wrap(*arg, **kwarg):
        if 'cached' in func.__dict__:
            return func.cached
        else:
            func.cached = func(*arg, **kwarg)
            return func.cached

    return wrap


cache.cached_funcs = set()
cache.clear_all = lambda: clear_all_cache(cache.cached_funcs)


# cache part end

def tick(arg):
    if tick.t1:
        t = time.time()
        print("{0} s".format(t - tick.t1))
    else:
        print("begin")
        tick.t1 = time.time()
    return arg


tick.t1 = None


def tack(arg):
    tick.t1 = time.time()
    print("begin")
    return arg


def iprint(*arg, **kwarg):
    def wrap(onearg):
        print(arg)
        return onearg

    return wrap


def ensure_unicode(string):
    return string.decode('utf-8') if isinstance(string, str) else string


def ensure_utf8(string):
    return string if isinstance(string, bytes) else string.encode('utf-8')


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj.__repr__()
