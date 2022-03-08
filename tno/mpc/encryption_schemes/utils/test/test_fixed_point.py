"""
This file contains tests that determine whether the code for fixed points works as expected.
"""

from typing import Any, Callable, List

import pytest

from tno.mpc.encryption_schemes.utils import FixedPoint
from tno.mpc.encryption_schemes.utils.fixed_point import FxpInputType
from tno.mpc.encryption_schemes.utils.test.fixed_point_test_parameters import (
    addition_list,
    cal_list,
    comp_list,
    comp_list_incorrect,
    division_list,
    float_params,
    fxp_params,
    int_params,
    multiplication_list,
    rand_list,
    repr_params,
    round_list,
    string_params,
    sub_add_mul_div_list_wrong_type,
    subtraction_list,
    to_bool_params,
    to_float_params,
    to_int_params,
    wrong_string_params,
    wrong_type_params,
)

fxp = FixedPoint.fxp


@pytest.mark.parametrize("value", wrong_type_params)
def test_initiation_from_wrong_type(value: Any) -> None:
    """
    Test whether the string initializer correctly identifies wrong input

    :param value: wrongly formatted string
    """
    with pytest.raises(TypeError):
        _ = fxp(value)


@pytest.mark.parametrize("value, precision, true_fxp", int_params)
def test_initiation_from_int(value: int, precision: int, true_fxp: FixedPoint) -> None:
    """
    Test whether FixedPoint.fxp works properly for integer types

    :param value: integer value of type mpz
    :param precision: desired precision
    :param true_fxp: correct result
    """
    value_fxp = fxp(value, target_precision=precision)
    assert value_fxp == true_fxp


@pytest.mark.parametrize("value, precision, true_fxp", float_params)
def test_initiation_from_float(
    value: float, precision: int, true_fxp: FixedPoint
) -> None:
    """
    Test whether FixedPoint.fxp works properly for float input

    :param value: float value
    :param precision: desired precision
    :param true_fxp: correct result
    """
    value_fxp = fxp(value, target_precision=precision)
    assert value_fxp == true_fxp


@pytest.mark.parametrize("value, precision, true_fxp", fxp_params)
def test_initiation_from_fxp(
    value: FixedPoint, precision: int, true_fxp: FixedPoint
) -> None:
    """
    Test whether FixedPoint.fxp works properly for float input

    :param value: float value
    :param precision: desired precision
    :param true_fxp: correct result
    """
    value_fxp = fxp(value, target_precision=precision)
    assert value_fxp == true_fxp


@pytest.mark.parametrize("value, precision, true_fxp", string_params)
def test_initiation_from_string(
    value: str, precision: int, true_fxp: FixedPoint
) -> None:
    """
    Test whether FixedPoint.fxp works properly for string input

    :param value: string
    :param precision: desired precision
    :param true_fxp: correct result
    """
    value_fxp = fxp(value, target_precision=precision)
    assert value_fxp == true_fxp


@pytest.mark.parametrize("value", wrong_string_params)
def test_initiation_from_wrong_string(value: str) -> None:
    """
    Test whether FixedPoint.fxp correctly throws an exception for wrong input formats

    :param value: string with incorrect format
    """
    with pytest.raises(ValueError):
        _ = fxp(value)


@pytest.mark.parametrize("value_list, correct_values", cal_list)
def test_calibration(
    value_list: List[FixedPoint], correct_values: List[FixedPoint]
) -> None:
    """
    Test to determine whether the FixedPoint.calibrate method works properly

    :param value_list: input list of fixed point numbers
    :param correct_values: list of fixed point numbers that holds the correct result
    """
    cal_values = list(FixedPoint.calibrate(*value_list)[1])
    for cal_value, correct_value in zip(cal_values, correct_values):
        assert FixedPoint.strong_eq(cal_value, correct_value)


@pytest.mark.parametrize("value_1, value_2, correct", addition_list)
def test_addition(
    value_1: FxpInputType,
    value_2: FxpInputType,
    correct: FixedPoint,
) -> None:
    """
    Test to determine whether addition works properly between two fixed points and fixed points and
    other compatible data types (integer, string, float).

    :param value_1: input for the FixedPoint.fxp function
    :param value_2: input for the FixedPoint.fxp function
    :param correct: Correct output of fxp(value_1) + fxp(value_2)
    """
    correct_fxp = fxp(correct)
    sum_ = fxp(value_1) + fxp(value_2)
    sum_l = fxp(value_1) + value_2
    sum_r = value_1 + fxp(value_2)
    assert FixedPoint.strong_eq(sum_, correct_fxp)
    assert FixedPoint.strong_eq(sum_l, correct_fxp)
    assert FixedPoint.strong_eq(sum_r, correct_fxp)


@pytest.mark.parametrize(
    "value_correct_type, value_wrong_type", sub_add_mul_div_list_wrong_type
)
def test_addition_wrong_type(
    value_correct_type: FxpInputType,
    value_wrong_type: FxpInputType,
) -> None:
    """
    Test to determine whether addition correctly identifies incompatible types.

    :param value_correct_type: input for the FixedPoint.fxp function
    :param value_wrong_type: input for the FixedPoint.fxp function of the wrong type
    """
    with pytest.raises(NotImplementedError):
        _ = fxp(value_correct_type) + value_wrong_type

    with pytest.raises(NotImplementedError):
        _ = value_wrong_type + fxp(value_correct_type)


@pytest.mark.parametrize("value_1, value_2, correct", subtraction_list)
def test_subtraction(
    value_1: FxpInputType, value_2: FxpInputType, correct: FixedPoint
) -> None:
    """
    Test to determine whether subtraction works properly between two fixed points and fixed points
    and other compatible data types (integer, string, float).

    :param value_1: input for the FixedPoint.fxp function
    :param value_2: input for the FixedPoint.fxp function
    :param correct: Correct output fxp(value_1) - fxp(value_2)
    """
    correct_fxp = fxp(correct)
    sub_ = fxp(value_1) - fxp(value_2)
    sub_l = fxp(value_1) - value_2
    sub_r = value_1 - fxp(value_2)
    assert FixedPoint.strong_eq(sub_, correct_fxp)
    assert FixedPoint.strong_eq(sub_l, correct_fxp)
    assert FixedPoint.strong_eq(sub_r, correct_fxp)


@pytest.mark.parametrize(
    "value_correct_type, value_wrong_type", sub_add_mul_div_list_wrong_type
)
def test_subtraction_wrong_type(
    value_correct_type: FxpInputType,
    value_wrong_type: FxpInputType,
) -> None:
    """
    Test to determine whether subtraction correctly identifies incompatible types

    :param value_correct_type: input for the FixedPoint.fxp function
    :param value_wrong_type: input for the FixedPoint.fxp function of the wrong type
    """
    with pytest.raises(NotImplementedError):
        _ = fxp(value_correct_type) - value_wrong_type

    with pytest.raises(NotImplementedError):
        _ = value_wrong_type - fxp(value_correct_type)


@pytest.mark.parametrize("value_1, value_2, correct", multiplication_list)
def test_multiplication(
    value_1: FxpInputType, value_2: FxpInputType, correct: FixedPoint
) -> None:
    """
    Test to determine whether multiplication works properly between two fixed points and fixed
    points and other compatible data types (integer, string, float).

    :param value_1: input for the FixedPoint.fxp function
    :param value_2: input for the FixedPoint.fxp function
    :param correct: Correct output of fxp(value_1) * fxp(value_2)
    """
    pos_1 = fxp(value_1)
    neg_1 = -fxp(value_1)
    pos_2 = fxp(value_2)
    neg_2 = -fxp(value_2)
    product_pos_pos = pos_1 * pos_2
    product_pos_neg = pos_1 * neg_2
    product_neg_pos = neg_1 * pos_2
    product_neg_neg = neg_1 * neg_2
    assert FixedPoint.strong_eq(product_pos_pos, fxp(correct))
    assert FixedPoint.strong_eq(product_pos_pos, product_neg_neg)
    assert FixedPoint.strong_eq(product_pos_neg, product_neg_pos)
    assert FixedPoint.strong_eq(product_pos_neg, -fxp(correct))
    mul_l = pos_1 * value_2
    mul_r = value_1 * pos_2
    assert FixedPoint.strong_eq(mul_l, fxp(correct))
    assert FixedPoint.strong_eq(mul_r, fxp(correct))


@pytest.mark.parametrize(
    "value_correct_type, value_wrong_type", sub_add_mul_div_list_wrong_type
)
def test_multiplication_wrong_type(
    value_correct_type: FxpInputType,
    value_wrong_type: FxpInputType,
) -> None:
    """
    Test to determine whether multiplication correctly identifies incompatible types

    :param value_correct_type: input for the FixedPoint.fxp function
    :param value_wrong_type: input for the FixedPoint.fxp function of the wrong type
    """
    with pytest.raises(NotImplementedError):
        _ = fxp(value_correct_type) * value_wrong_type

    with pytest.raises(NotImplementedError):
        _ = value_wrong_type * fxp(value_correct_type)


@pytest.mark.parametrize("value_1, value_2, correct", division_list)
def test_division(
    value_1: FxpInputType, value_2: FxpInputType, correct: FixedPoint
) -> None:
    """
    Test to determine whether division works properly between two fixed points and fixed
    points and other compatible data types (integer, string, float).

    :param value_1: input for the FixedPoint.fxp function
    :param value_2: input for the FixedPoint.fxp function
    :param correct: Correct output of fxp(value_1) / fxp(value_2)
    """
    pos_1 = fxp(value_1)
    neg_1 = -fxp(value_1)
    pos_2 = fxp(value_2)
    neg_2 = -fxp(value_2)
    quotient_pos_pos = pos_1 / pos_2
    quotient_pos_neg = pos_1 / neg_2
    quotient_neg_pos = neg_1 / pos_2
    quotient_neg_neg = neg_1 / neg_2
    assert FixedPoint.strong_eq(quotient_pos_pos, fxp(correct))
    assert FixedPoint.strong_eq(quotient_pos_pos, quotient_neg_neg)
    assert FixedPoint.strong_eq(quotient_pos_neg, quotient_neg_pos)
    assert FixedPoint.strong_eq(quotient_pos_neg, -fxp(correct))
    div_l = pos_1 / value_2
    div_r = value_1 / pos_2
    assert FixedPoint.strong_eq(div_l, fxp(correct))
    assert FixedPoint.strong_eq(div_r, fxp(correct))


@pytest.mark.parametrize(
    "value_correct_type, value_wrong_type", sub_add_mul_div_list_wrong_type
)
def test_division_wrong_type(
    value_correct_type: FxpInputType,
    value_wrong_type: FxpInputType,
) -> None:
    """
    Test to determine whether division correctly identifies incompatible types

    :param value_correct_type: input for the FixedPoint.fxp function
    :param value_wrong_type: input for the FixedPoint.fxp function of the wrong type
    """
    with pytest.raises(NotImplementedError):
        _ = fxp(value_correct_type) / value_wrong_type

    with pytest.raises(NotImplementedError):
        _ = value_wrong_type / fxp(value_correct_type)


@pytest.mark.parametrize("operator, value_1, value_2, correct", comp_list)
def test_comparison_correct_type(
    operator: Callable[[FxpInputType, FxpInputType], bool],
    value_1: FxpInputType,
    value_2: FxpInputType,
    correct: bool,
) -> None:
    """
    Test to determine whether all boolean operators work properly between two fixed points and
    fixed points and compatible types (integer, string, float).

    :param operator: function that takes two compatible fxp input values and returns a boolean
    :param value_1: input for the FixedPoint.fxp function
    :param value_2: input for the FixedPoint.fxp function
    :param correct: the correct answer of applying operator to fxp(value_1) and fxp(value_2)
    """
    assert operator(fxp(value_1), fxp(value_2)) == correct
    assert operator(fxp(value_1), value_2) == correct
    assert operator(value_1, fxp(value_2)) == correct


@pytest.mark.parametrize(
    "operator, value_correct_type, value_wrong_type", comp_list_incorrect
)
def test_comparison_incorrect_type(
    operator: Callable[[FxpInputType, FxpInputType], bool],
    value_correct_type: FxpInputType,
    value_wrong_type: FxpInputType,
) -> None:
    """
    Test to determine whether all boolean operators properly identify incompatible types.

    :param operator: function that takes two compatible fxp input values and returns a boolean
    :param value_correct_type: input for the FixedPoint.fxp function
    :param value_wrong_type: input for the FixedPoint.fxp function of the wrong type
    """

    with pytest.raises(NotImplementedError):
        _ = operator(fxp(value_correct_type), value_wrong_type)

    with pytest.raises(NotImplementedError):
        _ = operator(value_wrong_type, fxp(value_correct_type))


@pytest.mark.parametrize("low, high, signed", rand_list)
def test_random_range(low: FixedPoint, high: FixedPoint, signed: bool) -> None:
    """
    Test to determine whether the FixedPoint.random_range produces values in the correct range.

    :param low: lower bound for the random range
    :param high: upper bound for the random range
    :param signed: whether the range [low, high) should be extended to
    [low, high) \\cup (-high, low].
    """
    for _ in range(100):
        random_value = FixedPoint.random_range(low, high, signed)
        abs_random_value = abs(random_value)
        assert abs_random_value >= low
        assert abs_random_value < high
        assert random_value.precision == max(low.precision, high.precision)
        if not signed:
            assert random_value >= 0


@pytest.mark.parametrize(
    "integer_representation, current_precision, target_precision, correct_answer",
    round_list,
)
def test_round_to_precision(
    integer_representation: int,
    current_precision: int,
    target_precision: int,
    correct_answer: int,
) -> None:
    """
    Test whether the round_to_precision function works properly

    :param integer_representation: value-part of the fixed-point representation
    :param current_precision: precision-part of the fixed-point representation
    :param target_precision: target precision
    :param correct_answer: the correct new value-part
    """
    result = FixedPoint.round_to_precision(
        integer_representation, current_precision, target_precision
    )
    assert result == correct_answer


@pytest.mark.parametrize("input_value, correct_output", repr_params)
def test_representation(input_value: FixedPoint, correct_output: str) -> None:
    """
    Test whether the __repr__ function works correctly

    :param input_value: fixed-point number
    :param correct_output: correct representation of the fixed-point number
    """
    output = repr(input_value)
    assert output == correct_output


@pytest.mark.parametrize("input_value, correct_output", repr_params)
def test_to_string(input_value: FixedPoint, correct_output: str) -> None:
    """
    Test whether the __str__ function works correctly

    :param input_value: fixed-point number
    :param correct_output: correct representation of the fixed-point number
    """
    output = str(input_value)
    assert output == correct_output


@pytest.mark.parametrize("input_value, correct_output", to_bool_params)
def test_to_bool(input_value: FixedPoint, correct_output: bool) -> None:
    """
    Test whether the __bool__ function works correctly

    :param input_value: fixed-point number
    :param correct_output: correct bool cast of the fixed-point number
    """
    output = bool(input_value)
    assert output == correct_output


@pytest.mark.parametrize("input_value, correct_output", to_int_params)
def test_to_int(input_value: FixedPoint, correct_output: int) -> None:
    """
    Test whether the __int__ function works correctly

    :param input_value: fixed-point number
    :param correct_output: correct integer cast of the fixed-point number
    """
    output = int(input_value)
    assert output == correct_output


@pytest.mark.parametrize("input_value, correct_output", to_float_params)
def test_to_float(input_value: FixedPoint, correct_output: float) -> None:
    """
    Test whether the __float__ function works correctly

    :param input_value: fixed-point number
    :param correct_output: correct float cast of the fixed-point number
    """
    output = float(input_value)
    assert output == correct_output


@pytest.mark.parametrize("input_value", list(range(-10, 10)))
@pytest.mark.parametrize("precision", list(range(8)))
@pytest.mark.parametrize("bits", list(range(8)))
def test_right_bitshift(input_value: int, precision: int, bits: int) -> None:
    """
    Test the right bit shift operator

    :param input_value: input to shift
    :param precision: location of the radix, number of decimals
    :param bits: number of bits to shift
    """
    value = fxp(input_value, precision)
    assert abs((value >> bits) - (value / 2**bits)) <= 10**-precision


@pytest.mark.parametrize("input_value", list(range(-10, 10)))
@pytest.mark.parametrize("precision", list(range(8)))
@pytest.mark.parametrize("bits", list(range(8)))
def test_left_bitshift(input_value: int, precision: int, bits: int) -> None:
    """
    Test the left bit shift operator

    :param input_value: input to shift
    :param precision: location of the radix, number of decimals
    :param bits: number of bits to shift
    """
    value = fxp(input_value, precision)
    assert value << bits == value * 2**bits
