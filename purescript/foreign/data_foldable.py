from purescript.corefn.value import Array, NativeX


def foldr_array_(f, b, arr):
    """foldr :: forall a b. (a -> b -> b) -> b -> f a -> b"""
    if isinstance(arr, Array):
        acc = b
        array = arr.array
        length = len(array)
        for i in range(length - 1, -1, -1):
            acc = f(array[i], acc)
        return acc
    else:
        raise ValueError("arr was not an array")


foldr_array = NativeX(foldr_array_, 3, [])


def foldl_array(f):
    raise NotImplementedError()
