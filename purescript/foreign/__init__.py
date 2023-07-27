from purescript.corefn.abs import NativeX
from purescript.corefn.value import unit
from purescript.foreign import effect_aff, data_function_uncurried, data_string_common, data_string_regex, \
    partial_unsafe, data_lazy, unsafe_coerce, data_ring, data_enum, data_bounded, control_bind, data_functor, \
    data_heyting_algebra, data_show, data_ord, effect, control_extend, control_apply
from purescript.foreign.data_array import range_impl
from purescript.foreign.data_eq import eq_int_impl
from purescript.foreign.data_euclidean_ring import int_degree, int_div, int_mod
from purescript.foreign.data_foldable import foldr_array, foldl_array
from purescript.foreign.data_semigroup import concat_string
from purescript.foreign.data_semiring import int_add, int_mul
from purescript.foreign.effect_console import log

"""
Foreign functions can take any Box type as arguments.
Taking functions (Abs) as arguments complicates things since you cant call one without referencing a interpreter.
"""

foreign = {
    'Effect': effect.exports,
    'Effect.Aff': effect_aff.exports,
    'Effect.Console': {
        'log': log
    },
    'Data.Array': {
        'rangeImpl': NativeX(range_impl, 2, []),
    },
    'Data.Bounded': data_bounded.exports,
    'Data.Enum': data_enum.exports,
    'Data.Eq': data_eq.exports,
    'Data.EuclideanRing': data_euclidean_ring.exports,
    'Data.Foldable': {
        'foldrArray': foldr_array,
        'foldlArray': unit,
    },
    'Data.Functor': data_functor.exports,
    'Data.Function.Uncurried': data_function_uncurried.exports,
    'Data.HeytingAlgebra': data_heyting_algebra.exports,
    'Data.Lazy': data_lazy.exports,
    'Data.Ord': data_ord.exports,
    'Data.Ring': data_ring.exports,
    'Data.Semigroup': data_semigroup.exports,
    'Data.Semiring': data_semiring.exports,
    'Data.Show': data_show.exports,
    'Data.String.Common': data_string_common.exports,
    'Data.String.Regex': data_string_regex.exports,
    'Data.Unit': {'unit': unit},
    'Control.Apply': control_apply.exports,
    'Control.Bind': control_bind.exports,
    'Control.Extend': control_extend.exports,
    'Partial.Unsafe': partial_unsafe.exports,
    'Unsafe.Coerce': unsafe_coerce.exports,
}
