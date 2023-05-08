"""
This file contains tests that determine whether the code for utility functions works as expected.
"""

from functools import reduce
from math import gcd
from random import randint
from typing import Any, List

import pytest
from sympy import isprime

from tno.mpc.encryption_schemes.utils._check_gmpy2 import USE_GMPY2
from tno.mpc.encryption_schemes.utils.utils import (
    extended_euclidean,
    is_prime,
    lcm,
    mod_inv,
    next_prime,
    pow_mod,
    randprime,
)

if USE_GMPY2:
    from gmpy2 import mpz

small_primes = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
]


def prod(list_: List[Any]) -> Any:
    """
    Multiply all elements in a list

    :param list_: list of elements to be multiplied
    :return: the product of the elements in the input list
    """
    return reduce((lambda x, y: x * y), list_)


@pytest.mark.parametrize(
    "low, high",
    # random intervals
    [
        (rand_low, rand_low + randint(0, 2**100))
        for rand_low in [randint(0, 2**100) for _ in range(100)]
    ],
)
def test_randprime_regular_behaviour(low: int, high: int) -> None:
    """
    Test to check whether the randprime function from the utils module returns primes in the right
    interval and whether the result is of the correct type. The correct type depends on whether
    GMPY2 is installed.

    :param low: lower bound for the interval
    :param high: upper bound for the interval
    """
    prime = randprime(low, high)
    assert isprime(prime)
    assert low <= prime < high
    if USE_GMPY2:
        assert isinstance(prime, type(mpz(0)))
    else:
        assert isinstance(prime, int)


@pytest.mark.parametrize(
    "low, high",
    # random intervals
    [
        (rand_low, rand_low - randint(0, 2**100))
        for rand_low in [randint(0, 2**100) for _ in range(100)]
    ],
)
def test_randprime_wrong_input(low: int, high: int) -> None:
    """
    Test to check whether the randprime function from the utils module returns primes in the right
    interval and whether the result is of the correct type. The correct type depends on whether
    GMPY2 is installed.

    :param low: lower bound for the interval
    :param high: upper bound for the interval
    """
    with pytest.raises(ValueError):
        _ = randprime(low, high)


@pytest.mark.parametrize("low", list(range(0, 100)))
def test_next_prime(low: int) -> None:
    """
    Test to check whether the next_prime function indeed generates the next prime number. Also verifies if the mpz type
    is used when available.

    :param low: lower bound for the prime number
    """
    prime = next_prime(low)

    # check type correctness
    if USE_GMPY2:
        assert isinstance(prime, type(mpz(0)))
    else:
        assert isinstance(prime, int)

    # verify generated prime is indeed prime
    assert prime in small_primes
    # verify that this was indeed the first prime greater than the given lower bound
    prime_index = small_primes.index(prime)
    if prime_index == 0:
        assert low < prime
    else:
        assert small_primes[prime_index - 1] <= low < prime


@pytest.mark.parametrize(
    "nr_of_primes",
    # 100 testentries, where the nr_of_primes is random between 3 and 100 and the respective powers
    # are random between 1 and 100
    list(range(3, 30)),
)
def test_lcm(nr_of_primes: int) -> None:
    """
    Test to determine whether the lcm function works properly. Artificial values are created through
    random prime numbers and random powers, such that we know the correct lcm by construction.
    This value is then checked against the result from the lcm function of the utils module.

    :param nr_of_primes: The number of primes to be generated
    """
    primes = []
    for i in range(nr_of_primes):
        new_prime = randprime(1, 2**100)
        while new_prime in primes:
            new_prime = randprime(1, 2**100)
        primes.append(new_prime)

    powers_1 = [randint(0, 100) for _ in range(nr_of_primes)]
    powers_2 = [randint(0, 100) for _ in range(nr_of_primes)]
    lcm_powers = [max(powers_1[i], powers_2[i]) for i in range(nr_of_primes)]
    value_1 = prod([primes[i] ** powers_1[i] for i in range(nr_of_primes)])
    value_2 = prod([primes[i] ** powers_2[i] for i in range(nr_of_primes)])
    correct_lcm = prod([primes[i] ** lcm_powers[i] for i in range(nr_of_primes)])
    if USE_GMPY2:
        utils_lcm_value = lcm(mpz(value_1), mpz(value_2))
    else:
        utils_lcm_value = lcm(value_1, value_2)
    assert correct_lcm == utils_lcm_value


@pytest.mark.parametrize(
    "value, inverse",
    [(randint(2, 2**1024), randint(2, 2**1024)) for _ in range(100)],
)
def test_mod_inv_invertible(value: int, inverse: int) -> None:
    """
    Test to check whether the mod_inv function works properly. Artificial pairs of value, inverse
    are created and the respective modulus is extracted from this input.

    :param value: value for which the inverse needs to be found
    :param inverse: correct inverse
    """
    # extract modulus such that inverse is the modulus inverse of value
    # modulus = value * inverse - 1 ->
    # value * inverse = modulus + 1 ->
    # value * inverse = 1 mod modulus
    modulus = value * inverse - 1
    utils_inverse = mod_inv(value, modulus)
    assert utils_inverse == inverse


@pytest.mark.parametrize(
    "value, modulus",
    [
        (prime, prime ** randint(3, 10))
        for prime in [randprime(3, 2**100) for _ in range(100)]
    ]
    + [(0, prime) for prime in [randprime(3, 2**100) for _ in range(100)]],
)
def test_mod_inv_not_invertible(value: int, modulus: int) -> None:
    """
    Test to check whether the mod_inv function correctly identifies when a value is not invertible
    in Z_modulus.

    :param value: value for which the inverse needs to be found
    :param modulus: modulus such that value is not invertible in Z_modulus
    """
    with pytest.raises(ZeroDivisionError):
        _ = mod_inv(value, modulus)


@pytest.mark.parametrize(
    "value, power, modulus",
    [
        (randint(1, mod - 1) * (randint(0, 1) * 2 - 1), randint(-mod, mod), mod)
        for mod in [randprime(3, 2**20) for _ in range(100)]
    ],
)
def test_pow_mod_prime(value: int, power: int, modulus: int) -> None:
    """
    Test to check whether the pow_mod returns correct results for positive and negative values and
    powers if the modulus is prime (and thus each element is invertible).

    :param value: the base
    :param power: the exponent
    :param modulus: the modulus
    """
    utils_value = pow_mod(value, power, modulus)
    correct_value = 1
    if power < 0:
        value = mod_inv(value, modulus)
        power = -power
    for _ in range(power):
        correct_value = (correct_value * value) % modulus
    assert utils_value == correct_value


@pytest.mark.parametrize(
    "value, power, modulus",
    [
        (prime, randint(-prime + 1, -1), prime ** randint(2, 10))
        for prime in [randprime(3, 2**20) for _ in range(100)]
    ],
)
def test_pow_mod_prime_power(value: int, power: int, modulus: int) -> None:
    """
    Test to check whether the pow_mod returns correctly identifies that negative powers are
    impossible to calculate when the base value is not invertible in Z_modulus

    :param value: the base
    :param power: the exponent
    :param modulus: the modulus
    """
    with pytest.raises((ValueError, ZeroDivisionError)) as error:
        _ = pow_mod(value, power, modulus)
    assert "invertible" in str(error.value) or "Inverse" in str(error.value)


@pytest.mark.parametrize(
    "value_1, value_2",
    [(randint(3, 2**100), randint(3, 2**100)) for _ in range(100)],
)
def test_extended_euclidean(value_1: int, value_2: int) -> None:
    """
    Test to determine whether the extended euclidean function works properly. The return value of
    the gcd is checked against the gcd result from the math library and the relation between the
    outputs and the inputs is verified.

    :param value_1: integer value
    :param value_2: integer value
    """
    gcd_inputs, value_1_mult, value_2_mult = extended_euclidean(value_1, value_2)
    assert gcd_inputs == gcd(value_1, value_2)
    assert value_1_mult * value_1 + value_2_mult * value_2 == gcd_inputs


@pytest.mark.parametrize(
    "low, high",
    # random intervals
    [
        (rand_low, rand_low + randint(0, 2**100))
        for rand_low in [randint(0, 2**100) for _ in range(100)]
    ],
)
def test_primality_check_primes(low: int, high: int) -> None:
    """
    Test to determine that generated primes are actually prime.

    :param low: Lower bound (inclusive) of range in which to generate a prime.
    :param high: Higher bound (exclusive) of range in which to generate a prime.
    """
    prime = randprime(low, high)
    assert is_prime(prime)


@pytest.mark.parametrize(
    "low, high",
    # random intervals
    [
        (rand_low, rand_low + randint(0, 2**100))
        for rand_low in [randint(0, 2**100) for _ in range(100)]
    ],
)
def test_no_negative_primes(low: int, high: int) -> None:
    """
    Test to determine that negative primes are not seen as primes. In this case negative primes are negations of real
    primes.

    :param low: Lower bound (inclusive) of range in which to generate a real prime.
    :param high: Higher bound (exclusive) of range in which to generate a real prime.
    """
    prime = randprime(low, high)
    assert not is_prime(-prime)


@pytest.mark.parametrize(
    "number",
    # random number
    list(randint(-(2**100), 2**100) for _ in range(100)),
)
def test_primality_check_random_number(number: int) -> None:
    """
    Test to check if the custom is_prime method gives the same results as they sympy.isprime method.

    :param number: Number to check for primality.
    """
    assert isprime(number) == is_prime(number)
