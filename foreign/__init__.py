from corefn.abs import Foreign, Dynamic
from corefn.expression import App
from corefn.literals import String, Effect, unit
from foreign.data_array import range_impl
from foreign.data_eq import eq_int_impl
from foreign.data_euclidean_ring import int_degree, int_div, int_mod
from foreign.data_foldable import foldr_array, foldl_array
from foreign.data_semigroup import concat_string
from foreign.data_semiring import int_add, int_mul
from foreign.effect import bindE, pureE
from foreign.effect_console import log
from foreign.util import to_foreign

"""
Foreign functions can take any Box type as arguments.
Taking functions (Abs) as arguments complicates things since you cant call one without referencing a interpreter.
"""

foreign = {
    'Effect': {
        'pureE': pureE,
        'bindE': bindE
    },
    'Effect.Console': {
        'log': log
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
        'foldrArray': foldr_array,
        'foldlArray': unit,
    },
    'Data.Function.Uncurried': {
        'runFn2': to_foreign(lambda i, a: a),
    },
    'Data.Semigroup': {
        'concatString': to_foreign(concat_string),
    },
    'Data.Semiring': {
        'intAdd': to_foreign(int_add),
        'intMul': to_foreign(int_mul),
    },
    'Data.Show': {
        'showIntImpl': to_foreign(lambda i, e: String(str(e.value)))
    },
    'Data.Unit': {
        'unit': unit
    },
}
