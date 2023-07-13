from functools import reduce


def foldr_array(f, b, arr):
    """foldr :: forall a b. (a -> b -> b) -> b -> f a -> b"""
    acc = b
    for a in arr:
        acc = f(a)(acc)
    return acc


def foldl_array(f, b, arr):
    """foldl :: forall a b. (b -> a -> b) -> b -> f a -> b"""
    return reduce(lambda x, y: f(x)(y), arr, b)
