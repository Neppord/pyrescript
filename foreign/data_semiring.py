from corefn.literals import Int


def int_add(i, a, b):
    """

    :type a: Int
    :type b: Int
    """
    return Int(a.value + b.value)


def int_mul(i, a, b):
    return Int(a.value * b.value)
