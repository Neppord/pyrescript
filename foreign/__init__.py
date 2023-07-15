from foreign.data_array import range_impl
from foreign.data_eq import eq_int_impl
from foreign.data_euclidean_ring import int_degree, int_div, int_mod
from foreign.data_foldable import foldr_array, foldl_array
from foreign.data_semigroup import concat_string
from foreign.data_semiring import int_add, int_mul
from foreign.effect_console import log
from functools import wraps


def pure(x):
    return x


def apply(f):
    def apply2(a):
        return f(a)

    return apply2


def run_fn_2(fn):
    return curry(fn, 2)


def curry(fn, n):
    if n == 1:
        return fn
    elif n == 2:
        return wraps(fn)(lambda x: wraps(fn)(lambda y: fn(x, y)))
    elif n == 3:
        return wraps(fn)(lambda x: wraps(fn)(lambda y: wraps(fn)(lambda z: fn(x, y, z))))
    else:
        raise NotImplementedError


def bindE(a, atob):
    return atob(a)


foreign = {
    'Effect': {
        'pureE': pure,
        'bindE': curry(bindE, 2)
    },
    'Effect.Console': {
        'log': log
    },
    'Data.Array': {
        'rangeImpl': range_impl,
    },
    'Data.Eq': {
        'eqIntImpl': curry(eq_int_impl, 2),
    },
    'Data.EuclideanRing': {
        'intDegree': int_degree,
        'intDiv': curry(int_div, 2),
        'intMod': curry(int_mod, 2),
    },
    'Data.Foldable': {
        'foldrArray': curry(foldr_array, 3),
        'foldlArray': curry(foldl_array, 3),
    },
    'Data.Function.Uncurried': {
        'runFn2': run_fn_2,
    },
    'Data.Semigroup': {
        'concatString': curry(concat_string, 2)
    },
    'Data.Semiring': {
        'intAdd': curry(int_add, 2),
        'intMul': curry(int_mul, 2),
    },
    'Data.Show': {
        'showIntImpl': str
    },
    'Data.Unit': {
        'unit': "unit"
    },
}
