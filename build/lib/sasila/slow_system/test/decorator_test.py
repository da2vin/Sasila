#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps
from sasila.slow_system.utils.decorator import timeit

'''示例7: 在示例4的基础上，让装饰器带参数，
和上一示例相比在外层多了一层包装。
装饰函数名实际上应更有意义些'''


def deco(arg):
    def _deco(func):
        @wraps(func)
        def __deco(*args, **kwargs):
            ret = func(*args, **kwargs)
            return ret + arg

        return __deco

    return _deco


@timeit
@deco(3)
def myfunc(a, b):
    return a + b


print myfunc.__name__
print myfunc(2, 3)
