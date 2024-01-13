# %%
from functools import update_wrapper


# %%
def decorator(d):
    "Make function d a decorator. d wraps a function f"
    def _d(f):
        return update_wrapper(d(f), f)
    update_wrapper(_d, d)
    return _d

# %%
@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such that
    f(x, y, z) = f(x, f(y, z)), etc. Also, allow f(x) = x."""
    def n_ary_f(x, *args):
        return (f(x, n_ary_f(*args)) if args else x)
    return n_ary_f


# %%
@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then, when called again with some args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # Some types of args cannot be dict keys.
            return f(args)
    return _f


# %%
@decorator
def countcalls(f):
    """Decorator that counts the number of calls to itself and stores them in
    callscount[f]."""
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

callcounts = {}


# %%
@countcalls
def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


# %%
@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = f"{f.__name__}({', '.join(map(repr, args))})"
        print(f'{trace.level * indent}--> {signature}')
        trace.level += 1
        try:
            result = f(*args)
            print(f'{indent * (trace.level - 1)}<-- {signature} === {result}')
        finally:
            # This is needed in case the function exits unexpectedly and the 
            # indentation is not decreased.
            trace.level -= 1
        return result
    trace.level = 0
    return _f

# %%
@trace
def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)

fib(5)
# %%
