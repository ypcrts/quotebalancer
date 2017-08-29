#!/usr/bin/env python3
from __future__ import print_function

try:
    import vim
    import threading
except ImportError as e:
    print("ImportError {}".format(e.message))
    exit(1)


class cached_property_threadsafe(object):
    """
    A cached_property version for use in environments where multiple threads
    might concurrently try to access the property.
    https://raw.githubusercontent.com/pydanny/cached-property/master/cached_property.py
    """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func
        self.lock = threading.RLock()

    def __get__(self, obj, cls):
        if obj is None:
            return self

        obj_dict = obj.__dict__
        name = self.func.__name__
        with self.lock:
            try:
                # check if the value was computed before the lock was acquired
                return obj_dict[name]
            except KeyError:
                # if not, do the calculation and release the lock
                return obj_dict.setdefault(name, self.func(obj))


class Pair(tuple):
    def __new__(self, begin, stop=None):
        assert begin
        if not stop:
            begin = stop
        tuple.__init__(self, begin, stop)


class Parser:
    def __init__(self):
        self.pairs = set()
        self.pairs.update(self.common)

        if self.filetype == 'sh':
            self.pairs.add(Pair('$(', ')'))

    def __call__(self, buf=None):
        if not buf:
            buf = vim.current.buffer
        # todo: parse

    @classmethod
    def common(self):
        common_ = """`"'"""
        return list(Pair(q) for q in common_)

    @cached_property_threadsafe
    def filetype(self):
        return vim.eval("&ft")
