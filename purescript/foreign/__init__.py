from purescript.corefn.literals import unit
from purescript.foreign import effect_aff, data_function_uncurried, data_string_common, data_string_regex, \
    partial_unsafe, data_lazy, unsafe_coerce, data_ring, data_enum, data_bounded
from purescript.foreign.data_array import range_impl
from purescript.foreign.data_eq import eq_int_impl
from purescript.foreign.data_euclidean_ring import int_degree, int_div, int_mod
from purescript.foreign.data_foldable import foldr_array, foldl_array
from purescript.foreign.data_semigroup import concat_string
from purescript.foreign.data_semiring import int_add, int_mul
from purescript.foreign.data_show import show_int_impl
from purescript.foreign.effect import bindE, pureE
from purescript.foreign.effect_console import log
from purescript.foreign.util import to_foreign

"""
Foreign functions can take any Box type as arguments.
Taking functions (Abs) as arguments complicates things since you cant call one without referencing a interpreter.
"""

foreign = {
    'Effect': {
        'pureE': pureE,
        'bindE': bindE
    },
    'Effect.Aff': effect_aff.exports,
    'Effect.Console': {
        'log': log
    },
    'Data.Array': {
        'rangeImpl': to_foreign(range_impl),
    },
    'Data.Bounded': data_bounded.exports,
    'Data.Enum': data_enum.exports,
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
    'Data.Function.Uncurried': data_function_uncurried.exports,
    'Data.Lazy': data_lazy.exports,
    'Data.Ring': data_ring.exports,
    'Data.Semigroup': {
        'concatString': to_foreign(concat_string),
    },
    'Data.Semiring': {
        'intAdd': to_foreign(int_add),
        'intMul': to_foreign(int_mul),
    },
    'Data.Show': {'showIntImpl': show_int_impl},
    'Data.String.Common': data_string_common.exports,
    'Data.String.Regex': data_string_regex.exports,
    'Data.Unit': {'unit': unit},
    'Partial.Unsafe': partial_unsafe.exports,
    'Unsafe.Coerce': unsafe_coerce.exports,
}
