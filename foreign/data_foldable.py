from functools import reduce


def foldr_array(f, b, arr):
    """foldr :: forall a b. (a -> b -> b) -> b -> f a -> b"""
    def flipped(x, y):
        return f(x)(y)
    return reduce(flipped, arr[::-1], b)


def foldl_array(f, b, arr):
    """foldl :: forall a b. (b -> a -> b) -> b -> f a -> b"""
    return reduce(lambda x, y: f(x)(y), arr, b)
