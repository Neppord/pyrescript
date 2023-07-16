from types import FunctionType, BuiltinFunctionType

from corefn.abs import Foreign, ForeignUsingInterpreter
from corefn.expression import App
from corefn.literals import String, Effect
from foreign.data_array import range_impl
from foreign.data_eq import eq_int_impl
from foreign.data_euclidean_ring import int_degree, int_div, int_mod
from foreign.data_foldable import foldr_array, foldl_array
from foreign.data_semigroup import concat_string
from foreign.data_semiring import int_add, int_mul
from foreign.effect import bindE
from foreign.effect_console import log

from rpython.rlib.objectmodel import not_rpython

"""
Foreign functions can take any Box type as arguments.
Taking functions (Abs) as arguments complicates things since you cant call one without referencing a interpreter.
"""

@not_rpython
def to_foreign(value):
    t = type(value)
    if t == str:
        return String(value)
    elif t in [FunctionType, BuiltinFunctionType]:
        arguments = value.func_code.co_argcount
        if arguments == 1:
            return Foreign(value.func_code.co_name, lambda x: value(x))
        elif arguments == 2:
            return Foreign(value.func_code.co_name,
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
        'pureE': to_foreign(lambda x: Effect(x)),
        'bindE': with_interpreter(bindE)
    },
    'Effect.Console': {
        'log': Foreign("log", lambda x: Effect(App(Foreign("log", log), x)))
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
        'runFn2': to_foreign(lambda a: a),
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
