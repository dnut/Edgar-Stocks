import inspect
from functools import partial

def curry(f):
    if len(inspect.getfullargspec(f).args) < 2:
        return f
    return lambda x: curry(partial(f, x))