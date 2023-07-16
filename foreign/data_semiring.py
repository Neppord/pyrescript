from corefn.literals import Int


def int_add(a, b):
    """

    :type a: Int
    :type b: Int
    """
    return Int(a.value + b.value)


def int_mul(a, b):
    return Int(a.value * b.value)
