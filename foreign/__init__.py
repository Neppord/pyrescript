from corefn.abs import Foreign
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
from foreign.util import to_foreign, with_interpreter

"""
Foreign functions can take any Box type as arguments.
Taking functions (Abs) as arguments complicates things since you cant call one without referencing a interpreter.
"""

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
