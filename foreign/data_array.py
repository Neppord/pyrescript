from corefn.literals import ArrayLiteral, IntLiteral


def range_impl(start, end):
    """
    :type start: IntLiteral
    :type end: IntLiteral
    """
    return ArrayLiteral([IntLiteral(x) for x in range(start.value, end.value + 1)])
