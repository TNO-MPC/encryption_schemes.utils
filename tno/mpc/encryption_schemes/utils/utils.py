"""
Useful functions for creating encryption schemes.
"""

from math import gcd
from typing import Tuple

import sympy

# Import gmpy2 to improve efficiency (for larger integers), if available.
try:
    import gmpy2

    USE_GMPY2 = True
except ImportError:
    USE_GMPY2 = False


def randprime(low: int, high: int) -> int:
    """
    Generate a random prime number in the range [low, high). Returns GMPY2 MPZ integer if available.

    :param low: Lower bound (inclusive) of the range.
    :param high: Upper bound (exclusive) of the range.
    :return: Random prime number.
    :raise ValueError: the lower bound should be strictly lower than the upper bound
    """
    if low >= high:
        raise ValueError(
            "the lower bound should be smaller or equal to the upper bound"
        )
    if USE_GMPY2:
        return gmpy2.mpz(sympy.ntheory.generate.randprime(low, high))
    # else
    return sympy.ntheory.generate.randprime(low, high)


def pow_mod(base: int, exponent: int, modulus: int) -> int:
    """
    Compute base**exponent % modulus. Uses GMPY2 if available.

    :param base: base
    :param exponent: exponent
    :param modulus: modulus
    :return: base**exponent % modulus
    """
    if USE_GMPY2:
        return gmpy2.powmod(base, exponent, modulus)
    # else
    return pow(base, exponent, modulus)


def mod_inv(value: int, modulus: int) -> int:
    """
    Compute the inverse of a number, given the modulus of the group.
    Note that the inverse might not exist. Uses GMPY2 if available.

    :param value: The number to be inverted.
    :param modulus: The group modulus.
    :raise ZeroDivisionError: Raised when the inverse of the value does not exist.
    :return: The inverse of a under the modulus.
    """
    value %= modulus
    if USE_GMPY2:
        return gmpy2.invert(value, modulus)
    # else
    gcd_, inverse, _ = extended_euclidean(value, modulus)
    if gcd_ != 1:
        raise ZeroDivisionError(f"Inverse of {value} mod {modulus} does not exist.")
    return inverse


def extended_euclidean(num_a: int, num_b: int) -> Tuple[int, int, int]:
    """
    Perform the extended euclidean algorithm on the input numbers.
    The method returns gcd, x, y, such that a*x + b*y = gcd.

    :param num_a: First number a.
    :param num_b: Second number b.
    :return: Tuple containing gcd, x, and y, such that  a*x + b*y = gcd.
    """
    # a*x + b*y = gcd
    x_old, x_cur, y_old, y_cur = 0, 1, 1, 0
    while num_a != 0:
        quotient, num_b, num_a = num_b // num_a, num_a, num_b % num_a
        y_old, y_cur = y_cur, y_old - quotient * y_cur
        x_old, x_cur = x_cur, x_old - quotient * x_cur
    return num_b, x_old, y_old


def lcm(num_a: int, num_b: int) -> int:
    """
    Compute the least common multiple of two input numbers. Uses GMPY2 if available.

    :param num_a: First number a.
    :param num_b: Second number b.
    :return: Least common multiple of a and b.
    """
    if USE_GMPY2:
        return gmpy2.lcm(num_a, num_b)
    # else
    return num_a * num_b // gcd(num_a, num_b)
