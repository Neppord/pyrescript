def int_mod(a, b):
    abs_b = abs(b)
    return ((a % abs_b) + abs_b) % abs_b


def int_degree(x): return min(abs(x), 2147483647)


def int_div(a, b): return a // b
