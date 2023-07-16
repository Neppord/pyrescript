from types import FunctionType, BuiltinFunctionType

from corefn.abs import Foreign, ForeignUsingInterpreter
from corefn.literals import String
from foreign.data_array import range_impl
from foreign.data_eq import eq_int_impl
from foreign.data_euclidean_ring import int_degree, int_div, int_mod
from foreign.data_foldable import foldr_array, foldl_array
from foreign.data_semigroup import concat_string
from foreign.data_semiring import int_add, int_mul
from foreign.effect_console import log

from rpython.rlib.objectmodel import not_rpython


def pure(x):
    return x


def apply(f):
    def apply2(a):
        return f(a)
    return apply2


def run_fn_2(fn):
    """noop all functions are curried by default"""
    return fn


def bindE(interpreter, a):
    return Foreign("bindE", lambda atob: atob.call_abs(interpreter, a))

@not_rpython
def to_foreign(value):
    t = type(value)
    if t == str:
        return String(value)
    elif t in [FunctionType, BuiltinFunctionType]:
        arguments = value.func_code.co_argcount
        if arguments == 1:
            return Foreign(
                value.func_code.co_name,
                lambda x: value(x)
            )
        elif arguments == 2:
            return Foreign(
                value.func_code.co_name,
                lambda x: Foreign(
                    "%s (%s)" % (value.func_code.co_name, x.__repr__()),
                    lambda y: value(x, y)
              )
            )
        elif arguments == 3:
            return Foreign(
                value.func_code.co_name,
                lambda x: Foreign(
                    "%s (%s)" % (value.func_code.co_name, x.__repr__()),
                    lambda y: Foreign(
                    "%s (%s) (%s)" % (value.func_code.co_name, x.__repr__(), y.__repr__()),
                        lambda z: value(x, y, z)
                    )
                )
            )
        else:
            NotImplementedError("dont support %s number of arguments" % arguments)
    else:
        NotImplementedError("cant translate %r of type %r" % (value, t))

def with_interpreter(f):
    return ForeignUsingInterpreter(f)

foreign = {
    'Effect': {
        'pureE': to_foreign(pure),
        'bindE': to_foreign(bindE)
    },
    'Effect.Console': {
        'log': to_foreign(log)
    },
    'Data.Array': {
        'rangeImpl': to_foreign(range_impl),
    },
    'Data.Eq': {
        'eqIntImpl': to_foreign(eq_int_impl),
    },
    'Data.EuclideanRing': {
        'intDegree': to_foreign(int_degree),
        'intDiv': to_foreign(int_div),
        'intMod': to_foreign(int_mod),
    },
    'Data.Foldable': {
        'foldrArray': with_interpreter(foldr_array),
        'foldlArray': with_interpreter(foldl_array),
    },
    'Data.Function.Uncurried': {
        'runFn2': to_foreign(run_fn_2),
    },
    'Data.Semigroup': {
        'concatString': to_foreign(concat_string),
    },
    'Data.Semiring': {
        'intAdd': to_foreign(int_add),
        'intMul': to_foreign(int_mul),
    },
    'Data.Show': {
        'showIntImpl': to_foreign(lambda e: String(str(e.value)))
    },
    'Data.Unit': {
        'unit': to_foreign("unit")
    },
}
