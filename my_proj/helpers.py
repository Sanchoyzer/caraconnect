def is_float_equal(a: float, b: float, delta: float = 10**-3) -> bool:
    return abs(a - b) < delta
