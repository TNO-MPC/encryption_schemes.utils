"""
This is module implementing fixed point numbers for python. For a motivation, description and some
examples, we refer to the docstring of the FixedPoint class.
"""

from __future__ import annotations

import numbers
from secrets import randbelow
from typing import Optional, Tuple, Union

# Add numpy support, if available.
try:
    import numpy as np

    SUPPORT_NUMPY = True
except ImportError:
    SUPPORT_NUMPY = False

FxpInputType = Union["FixedPoint", numbers.Integral, str, float]


class FixedPoint:
    r"""
    Outline:

    1. Motivation
    2. Description
    3. Examples

    1. Motivation

    Encryption schemes generally work with (scaled) fixed-point numbers (or integers), while such
    numbers are represented by floating points in python. This causes a discrepancy between the
    number that is encrypted and the respective decryption. This results in difficulties, e.g., when
    you want a random additive plaintext mask. This module addresses that discrepancy and provides
    arbitrary-precision fixed-point numbers including simple arithmetic such as addition,
    subtraction, multiplication and comparison operators.

    2. Description

    A fixed-point number is defined by 2 integers:

    - value: an arbitrary-precision integer
    - precision: an integer indicating the position of the radix which separates the integer part
      from the fractional part (counting from the right)

    Fixed-point numbers can be instantiated from strings, integers, floats and other fixed-points.
    using the class method FixedPoint.fxp.

    3. Examples:

    - fxp("10.001234")    -> value = 10001234   precision = 6     (this represents 10.001234)
    - fxp("1234e-2")      -> value = 1234       precision = 2     (this represents 12.34)
    - fxp(42)             -> value = 42         precision = 0     (this represents 42)
    - fxp(-123, 2)        -> value = -12300     precision = 2     (this represents -123.00)
    - fxp(123.)           -> value = 123        precision = 0     (This represents 123)
    - fxp(-1.23)          -> value = -123       precision = 2     (this represents -1.23)
    - fxp(-0.123, 5)      -> value = -12300     precision = 5     (this represents -0.12300)
    - fxp(1234e-2)        -> value = 1234       precision = 2     (this represents 12.34)
    """

    __slots__ = (
        "value",
        "precision",
    )

    value: int
    precision: int

    DEFAULT_FLOAT_PRECISION = 16

    @classmethod
    def fxp(
        cls,
        input_value: FxpInputType,
        target_precision: Optional[int] = None,
    ) -> FixedPoint:
        """
        Create a fixed-point number from a string, int, float or fixed-point number with a specified
        precision. If no precision is provided, it is deduced from the input_value. If precision is
        provided but it contradicts the precision of the input_value value (too large or too small), the
        input_value value is either truncated or trailing zeroes are added.

        Legitimate input values:

        - str: a string containing numbers in the range [0-9].
            This can be point-separated to represent an integer part (before the full stop)
            and a fractional part (after the full stop).
        - int: an arbitrarily large integer.
            By default,it will be converted to a fixed-point with a precision of 0, but if a precision
            is provided, then the fixed point represents the input_value value times 10**-precision.
        - float: a floating-point number.
            The default precision is 16 bits.
            The floating point is scaled and the value is extracted according to the
            floating point number and the precision.
        - FixedPoint: another fixed-point number.
            If no precision is provided, all values are copied.
            If a precision is provided, the fixed-point number is either truncated or
            trailing zeroes are added to attain the new precision.

        :param input_value: the number to be converted to a fixed-point.
        :param target_precision: The desired precision of the resulting fixed-point number.
        :return: A fixed point version of the provided input
        :raises TypeError: Raised if the input value is not an integer, float, fixed point or string
        """
        # minimal precision is 0
        if target_precision is not None:
            assert target_precision >= 0

        if isinstance(input_value, str):
            return FixedPoint.initiate_from_string(input_value, target_precision)
        if isinstance(input_value, numbers.Integral):
            return FixedPoint.initiate_from_int(input_value, target_precision)
        if isinstance(input_value, float):
            return FixedPoint.initiate_from_float(input_value, target_precision)
        if SUPPORT_NUMPY and isinstance(input_value, np.floating):
            return FixedPoint.initiate_from_float(input_value, target_precision)
        if isinstance(input_value, FixedPoint):
            return FixedPoint.initiate_from_fxp(input_value, target_precision)
        raise TypeError("the input_value is not of type int, float, fixed-point or str")

    def __init__(self, value: int, precision: int) -> None:
        """
        Initialise the fixed point number.

        :param value: The arbitrary-precision integer value representing the fixed point number
        :param precision: The location of the radix, counting from the right
        """
        self.value = value
        assert precision >= 0
        self.precision = precision

    @staticmethod
    def initiate_from_string(
        input_value: str, precision: Optional[int] = None
    ) -> FixedPoint:
        """
        This is the most reliable way to instantiate a fixed point, as the string accurately
        represents how the fixed point will be represented.
        The input is parsed as <integer>.<fractional> or <integer> or <integer>e<integer>.
        the precision is extracted automatically. If a target precision is
        provided then zeroes are added if the target precision is higher and the number is
        rounded towards the right precision if the target precision is lower.

        :param input_value: string of decimals, possibly separated by a full stop
        :param precision: desired precision. This has precedence over the implicit string precision.
        :return: the resulting fixed-point number
        :raises ValueError: Raised if the provided string does not fit the parsing format.
        """
        if " " in input_value:
            raise ValueError("It is not allowed to have spaces in the input")
        if "e" in input_value:
            e_split = input_value.split("e")
            left_side = FixedPoint.initiate_from_string(e_split[0])
            power = int(e_split[1])
            if power < 0:
                result = FixedPoint(left_side.value, left_side.precision - power)
            else:
                result = FixedPoint(left_side.value * 10**power, left_side.precision)
            return FixedPoint.fxp(result, precision)

        split = input_value.split(".")
        left = split[0]
        nr_entries = len(split)

        # If the format is <integer>, parse the input as an int and call the initiation function
        # for integers.
        if nr_entries == 1:
            try:
                value = int(left)
            except ValueError as format_error:
                raise ValueError(
                    'The input value does not conform to the expect format "x.y" or "x" for '
                    "integers x and y"
                ) from format_error
            if precision is None:
                return FixedPoint(value, 0)
            return FixedPoint(value * 10**precision, precision)

        # If the format is <integer>.<fractional>, determine whether the fractional part gives the
        # right precision. Correct the value if the precisions do not match.
        if nr_entries == 2:
            right = split[1]
            # combine the integer and fractional part into 1 big integer
            value_str = left + right
            # determine the precision of the fractional part
            input_precision = len(right)
            if precision is not None:
                radix_from_right = precision
                assert precision >= 0
                difference = precision - input_precision
                if difference >= 0:
                    # add (precision - input_precision) trailing zeroes
                    value_str += "0" * difference
                    value = int(value_str)
                else:
                    # truncate the last (input_precision - precision) digits and round if necessary
                    value_int = int(value_str)
                    value = FixedPoint.round_to_precision(
                        value_int, input_precision, precision
                    )
            else:
                radix_from_right = input_precision
                value = int(value_str)
            return FixedPoint(value, radix_from_right)

        # Raise an error if the input_value does not have the right format
        raise ValueError(
            'The input value does not conform to the expect format "x.y" or "x" '
            "for integers x and y"
        )

    @staticmethod
    def initiate_from_int(
        input_value: numbers.Integral, precision: Optional[int] = None
    ) -> FixedPoint:
        """
        If the input_value is an integer, we set the integer value to the input_value and decimal to zero.

        :param input_value: the input_value integer
        :param precision: position of the radix, counting from the right
        :return: the resulting fixed-point number
        """
        if precision is None:
            return FixedPoint(int(input_value), 0)
        return FixedPoint(int(input_value * 10**precision), precision)

    @staticmethod
    def initiate_from_float(
        input_value: float, target_precision: Optional[int] = None
    ) -> FixedPoint:
        """
        if the input value is a float, we multiply it by a power of 10 to create a scaled floating
        point  number and then extract an integer to represent the fixed point number. If no
        precision is provided, the precision is extracted from the string representation.

        :param input_value: the input_value integer
        :param target_precision: desired precision
        :return: the resulting fixed-point number
        """

        return FixedPoint.initiate_from_string(str(input_value), target_precision)

    @staticmethod
    def initiate_from_fxp(
        input_value: FixedPoint, target_precision: Optional[int] = None
    ) -> FixedPoint:
        """
        If the input value is another fixed point, correct the value with respect to the target
        precision.

        :param input_value: the input_value fixed-point number
        :param target_precision: desired precision
        :return: the resulting fixed-point number
        """
        if target_precision is None:
            return FixedPoint(input_value.value, input_value.precision)

        assert target_precision >= 0
        if target_precision >= input_value.precision:
            value = input_value.value * 10 ** (target_precision - input_value.precision)
        else:
            value = FixedPoint.round_to_precision(
                input_value.value, input_value.precision, target_precision
            )
        return FixedPoint(value, target_precision)

    # endregion

    @staticmethod
    def calibrate(*fixed_points: FixedPoint) -> Tuple[int, Tuple[FixedPoint, ...]]:
        r"""
        Function that determines that maximum precision among all the fixed points and scales
        the fixed points according to the maximum precision.

        :param \*fixed_points: fixed point numbers
        :return: A tuple where the first entry is the maximum precision and the subsequent entries
            are the given fixed points scaled to this maximum precision.
        """
        max_precision: int = max(fixed_point.precision for fixed_point in fixed_points)
        calibrated_fxps = tuple(
            FixedPoint.fxp(fixed_point, max_precision) for fixed_point in fixed_points
        )
        return max_precision, calibrated_fxps

    def __repr__(self) -> str:
        """
        Function that determines the representation of a fixed point object

        :return: string containing a representation of the fixed point object
        """
        return str(self)

    def __str__(self) -> str:
        """
        Function that casts a fixed point object to a string. First a representation without a radix
        is found and then the radix is inserted in the right place if the fixed point is not integer.

        :return: A string representing the fixed point object
        """
        is_neg = self.value < 0
        sign = "-" if is_neg else ""
        pos_string = str(abs(self.value))
        string_len = len(pos_string)
        if self.precision == 0:
            return sign + pos_string
        if string_len <= self.precision:
            diff = self.precision - string_len
            pos_string = "0" * (diff + 1) + pos_string
        return (
            sign + pos_string[: -self.precision] + "." + pos_string[-self.precision :]
        )

    def __bool__(self) -> bool:
        """
        Function that casts a fixed point object to a boolean.

        :return: A bool representing whether the fixed point object is unequal to zero.
        """
        return bool(self.value)

    def __int__(self) -> int:
        """
        Function that casts a fixed point object to an integer.
        The function uses rounding instead of downward truncation.

        :return: An integer representing the rounded fixed point object
        """
        return int(FixedPoint.round_to_precision(self.value, self.precision, 0))

    def __float__(self) -> float:
        """
        Function that cases a fixed point object to a float. If the fixed point number is too large,
        the float might return an error.

        :return: A floating point number representing the fixed point object
        """
        return float(self.value) / float(10**self.precision)

    def __eq__(self, other: object) -> bool:
        """
        Function that determines whether the fixed point object is equal to another object. The
        other object does not have to be a fixed point object. Additionally, this is a 'weak'
        equality in the sense that we first cast the other object to a fixed point number if it is
        not already and then check for equality. The precision value does not need to be equal, as
        long as the calibrated fixed point objects are equal. For strong equality, use strong_eq.

        For example:

        - fxp("100.0") == fxp("100.0000") -> True
        - fxp("12.34") == 12.34 -> True
        - fxp("0.012") == fxp("0.01") -> False

        :param other: Fixed point object, integer, string or float
        :return: whether self and the other object are (weakly) equal
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        if isinstance(other, FixedPoint):
            if self.precision != other.precision:
                _, (cal_self, cal_other) = FixedPoint.calibrate(self, other)
                return cal_self.value == cal_other.value
            return self.value == other.value
        return self == FixedPoint.fxp(other, self.precision)

    @staticmethod
    def strong_eq(fxp_1: FixedPoint, fxp_2: FixedPoint) -> bool:
        """
        Function that determines whether two fixed points are exactly equal

        :param fxp_1: Fixed point number
        :param fxp_2: Fixed point number
        :return: Whether the values and precision of the fixed point objects are equal
        """
        return fxp_1.value == fxp_2.value and fxp_1.precision == fxp_2.precision

    def __neg__(self) -> FixedPoint:
        """
        Function that returns a fixed point number that represents the negation of the fixed point
        number.

        :return: negation of the fixed point number
        """
        return FixedPoint(-self.value, self.precision)

    def __gt__(self, other: object) -> bool:
        """
        Function that returns whether this fixed pont number is greater than another compatible
        data type instance.

        :param other: fixed point number, integer, string or float
        :return: whether self is greater than the fixed point version of other
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)
        _, (cal_self, cal_other) = FixedPoint.calibrate(self, other_)
        return cal_self.value > cal_other.value

    def __ge__(self, other: object) -> bool:
        """
        Function that returns whether this fixed pont number is greater than or equal to another
        compatible data type instance.

        :param other: fixed point number, integer, string or float
        :return: whether self is greater than or equal to the fixed point version of other
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)
        _, (cal_self, cal_other) = FixedPoint.calibrate(self, other_)
        return cal_self.value >= cal_other.value

    def __lt__(self, other: object) -> bool:
        """
        Function that returns whether this fixed pont number is less than another
        compatible data type instance.

        :param other: fixed point number, integer, string or float
        :return: whether self is less than the fixed point version of other
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)
        _, (cal_self, cal_other) = FixedPoint.calibrate(self, other_)
        return cal_self.value < cal_other.value

    def __le__(self, other: object) -> bool:
        """
        Function that returns whether this fixed pont number is less than or equal to another
        compatible data type instance.

        :param other: fixed point number, integer, string or float
        :return: whether self is less than or equal to the fixed point version of other
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)
        _, (cal_self, cal_other) = FixedPoint.calibrate(self, other_)
        return cal_self.value <= cal_other.value

    def __abs__(self) -> FixedPoint:
        """
        Function that returns a fixed point number that represents the absolute value of the fixed
        point number.

        :return: absolute value of the fixed point number
        """
        return FixedPoint(abs(self.value), self.precision)

    def __sub__(self, other: object) -> FixedPoint:
        """
        Subtract another fixed point number (or type convertible to a fixed point number) from self.

        :param other: a fixed point number, integer, string or float
        :return: the result of subtracting the other value from self
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)
        max_precision, (cal_self, cal_other) = FixedPoint.calibrate(self, other_)
        return FixedPoint(cal_self.value - cal_other.value, max_precision)

    def __rsub__(self, other: object) -> FixedPoint:
        """
        Subtract self from an object of a type convertible to a fixed point number

        :param other: a fixed point number, integer, string or float
        :return: the result of subtracting self from the other value
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other, self.precision)
        return other_ - self

    def __add__(self, other: object) -> FixedPoint:
        """
        Add another fixed point number (or type convertible to a fixed point number) to self.

        :param other: a fixed pont number, integer, string or float
        :return: The addition of self to other
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)
        max_precision, (cal_self, cal_other) = FixedPoint.calibrate(self, other_)
        return FixedPoint(cal_self.value + cal_other.value, max_precision)

    __radd__ = __add__

    @staticmethod
    def round_to_precision(
        value: int, current_precision: int, target_precision: int
    ) -> int:
        """
        Function that takes a fixed point representation (value, precision) and changes the value
        to obtain the right precision for the fixed point representation. It uses rounding when the
        target precision is lower than the current precision.

        :param value: An integer representing the value
        :param current_precision: An integer representing the precision of the given value
        :param target_precision: The desired precision
        :return: A new value that represents a (rounded) fixed point number with the target
                 precision
        :raise TypeError: If value, current_precision or target_precision is not an int
        """

        if current_precision <= target_precision:
            return_value: int = value * 10 ** int(target_precision - current_precision)
            return return_value

        sign = int(value >= 0) * 2 - 1
        abs_value: int = abs(value)
        to_reduce_by: int = current_precision - target_precision
        # to_reduce_by > 0, because current_precision > target_precision
        pre_scaled_value: int = abs_value // 10 ** (to_reduce_by - 1)
        last_digit: int = pre_scaled_value % 10
        round_away_from_zero: bool = last_digit >= 5
        scaled_value: int = pre_scaled_value // 10
        # if we only truncate zeroes, we do not need any corrections
        correction: int = int(round_away_from_zero)
        if scaled_value * 10**to_reduce_by == abs_value:
            correction = 0

        rounded_scaled_value = sign * (scaled_value + correction)
        return rounded_scaled_value

    def __mul__(self, other: object) -> FixedPoint:
        """
        Multiply another fixed point number (or type convertible to a fixed point number) with self.
        Note that the result is calculated first with arbitrary precision and then rounded to obtain
        the maximum precision of the two inputs.

        For example:

        - fxp("0.1") * fxp("0.5") = fxp("0.1")
        - fxp("0.1") * fxp("0.4") = fxp("0.0")

        :param other: a fixed point number or other type convertible to a fixed point number.
        :return: a * b
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)

        max_precision = max(self.precision, other_.precision)

        # The multiplication value is simply the multiplied values
        mult = self.value * other_.value
        # This has precision self.precision + other_.precision
        new_precision = self.precision + other_.precision

        # scale down, such that is has a precision of max_precision
        scaled_mult = FixedPoint.round_to_precision(
            value=mult, current_precision=new_precision, target_precision=max_precision
        )
        return FixedPoint(scaled_mult, max_precision)

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> FixedPoint:
        """
        Divide self with another fixed point number (or type convertible to a fixed point number).
        Note that the result is calculated first with arbitrary precision and then rounded to obtain
        the maximum precision of the two inputs.

        For example:

        - fxp("0.2") / fxp("3.0") = fxp("0.7")
        - fxp("0.1") / fxp("2.1") = fxp("0.0")

        :param other: a fixed point number or other type convertible to a fixed point number.
        :return: a / b
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        other_ = FixedPoint.fxp(other)

        max_precision = max(self.precision, other_.precision)

        # To divide we first determine a scaling factor (for higher precision)
        scale_factor = 10 ** (self.precision + 2 * other_.precision + 1)
        # use proper rounding
        div = (scale_factor * self.value + other_.value // 2) // other_.value
        # This has precision self.precision + other.precision
        new_precision = 2 * self.precision + other_.precision + 1

        # scale down, such that is has a precision of max_precision
        scaled_div = FixedPoint.round_to_precision(
            value=div, current_precision=new_precision, target_precision=max_precision
        )

        return FixedPoint(scaled_div, max_precision)

    def __rtruediv__(self, other: object) -> FixedPoint:
        """
        Divide self with another fixed point number (or type convertible to a fixed point number).
        Note that the result is calculated first with arbitrary precision and then rounded to obtain
        the maximum precision of the two inputs.

        For example:

        - fxp("0.2") / fxp("3.0") = fxp("0.7")
        - fxp("0.1") / fxp("2.1") = fxp("0.0")

        :param other: a fixed point number or other type convertible to a fixed point number.
        :return: a / b
        :raise NotImplementedError: If the other object does not have a compatible type.
        """
        if not isinstance(other, (str, numbers.Integral, float, FixedPoint)):
            raise NotImplementedError(
                "The compatible object types are string, integer, float and FixedPoint."
            )
        return FixedPoint.fxp(other).__truediv__(self)

    def __rshift__(self, other: int) -> FixedPoint:
        """
        Right bit shift operation without moving the radix.
        Shifts the underlying integer value, but does not modify the radix position.

        :param other: number of bits to shift
        :return: shifted fixed point
        """
        return FixedPoint(self.value >> other, self.precision)

    def __lshift__(self, other: int) -> FixedPoint:
        """
        Left bit shift operation without moving the radix.
        Shifts the underlying integer value, but does not modify the radix position

        :param other: number of bits to shift
        :return: shifted fixed point
        """
        return FixedPoint(self.value << other, self.precision)

    @staticmethod
    def random_range(
        lower_bound: FixedPoint,
        upper_bound: FixedPoint,
        signed: bool = False,
    ) -> FixedPoint:
        r"""
        Return a uniformly random fixed-point in the interval [lower_bound, upper_bound).
        If signed is True, the interval becomes
        [lower_bound, upper_bound) $\cup$ (-upper_bound, lower_bound].

        :param lower_bound: integer lower bound (inclusive)
        :param upper_bound: integer upper bound (exclusive)
        :param signed: whether the random fixed-point number should have a random sign or just be
                       positive
        :return: a uniformly random fixed-point in the specified interval
        """
        assert (
            lower_bound < upper_bound
        ), "the upper bound needs to be larger than the lower bound"
        max_precision, (cal_lower_bound, cal_upper_bound) = FixedPoint.calibrate(
            lower_bound, upper_bound
        )
        value = (
            randbelow(cal_upper_bound.value - cal_lower_bound.value)
            + cal_lower_bound.value
        )
        if signed:
            sign = randbelow(2) * 2 - 1
            value *= sign
        return FixedPoint(value, max_precision)
