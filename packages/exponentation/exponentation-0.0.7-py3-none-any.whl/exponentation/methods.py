from decimal import Decimal


def power_with_naive(base, exponent):
    base = Decimal(base)
    if exponent >= 0:
        result = Decimal(1)
        for _ in range(exponent):
            result *= base
    else:
        result = Decimal(1)
        for _ in range(-exponent):
            result /= base
    return result


def tree(base, exponent):
    base = Decimal(base)
    if not isinstance(exponent, int):
        raise TypeError("Exponent must be an integer")
    if exponent == 0:
        return Decimal(1)
    if exponent < 0:
        base = Decimal(1) / base
        exponent = -exponent
    if exponent % 2 == 0:
        half_power = tree(base, exponent // 2)
        return half_power * half_power
    else:
        half_power = tree(base, (exponent - 1) // 2)
        return half_power * half_power * base


def accum(base, exponent):
    base = Decimal(base)
    result = Decimal(1)
    if exponent < 0:
        base = Decimal(1) / base
        exponent = -exponent
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base = base * base if exponent > 1 else base
        exponent //= 2

    return result


def right_left(base, exponent):
    base = Decimal(base)
    result = Decimal(1)
    while exponent != 0:
        if exponent % 2 == 1:
            result *= base
        exponent >>= 1
        base *= base
    return result


def stairs(base, exponent):
    base = Decimal(base)
    result = Decimal(1)
    x1 = Decimal(1)
    x2 = base
    bin_k = list(map(int, bin(exponent)[2:]))
    for i in range(len(bin_k)):
        if bin_k[i] == 0:
            x2 = x1 * x2
            x1 = x1 * x1
        else:
            x1 = x1 * x2
            x2 = x2 * x2
    return x1


def factorize(n):
    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            n //= i
            factors.append(i)
        i += 1
    if n >= 0:
        factors.append(n)
    return factors


def power_fact(base, exponent):
    base = Decimal(base)
    result = Decimal(1)
    lists = factorize(exponent)
    for el in lists:
        result *= base ** el
    return result


def binary(val, p):
    val = Decimal(val)
    result = Decimal(1)
    bin_k = list(map(int, bin(p)[2:]))
    for bit in bin_k:
        result *= result
        if bit == 1:
            result *= val
    return result
