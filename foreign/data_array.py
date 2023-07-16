from corefn.literals import Array, Int


def range_impl(i, start, end):
    """
    :type start: Int
    :type end: Int
    """
    return Array([Int(x) for x in range(start.value, end.value + 1)])
