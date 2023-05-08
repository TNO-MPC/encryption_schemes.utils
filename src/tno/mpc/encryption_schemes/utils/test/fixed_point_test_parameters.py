"""
File containing test input for test_fixed_point.py
"""
import numpy as np

from tno.mpc.encryption_schemes.utils.fixed_point import FixedPoint

try:
    import gmpy2

    USE_GMPY2 = True
except ImportError:
    USE_GMPY2 = False

fxp = FixedPoint.fxp

wrong_type_params = [[1], (2,), fxp]

wrong_string_params = ["1.1.1", " 1.1", "1.1 ", "1,2"]

string_params = [
    ("0", 0, FixedPoint(0, 0)),
    ("1", 0, FixedPoint(1, 0)),
    ("-2", 0, FixedPoint(-2, 0)),
    ("0.00123", None, FixedPoint(123, 5)),
    (".0012", 4, FixedPoint(12, 4)),
    ("0.00123", 5, FixedPoint(123, 5)),
    ("1.00000000000011111111", None, FixedPoint(100000000000011111111, 20)),
    ("-123456.78901234556", None, FixedPoint(-12345678901234556, 11)),
    ("0.0001", None, FixedPoint(1, 4)),
    ("12300.0045", None, FixedPoint(123000045, 4)),
    ("12300.0045", 3, FixedPoint(12300005, 3)),
    ("12300.0045", 2, FixedPoint(1230000, 2)),
    ("-12300.0045", None, FixedPoint(-123000045, 4)),
    ("-12300.0045", 3, FixedPoint(-12300005, 3)),
    ("-12300.0045", 2, FixedPoint(-1230000, 2)),
    ("1234e-2", None, FixedPoint(1234, 2)),
    ("1234e-2", 4, FixedPoint(123400, 4)),
    ("1234e-2", 1, FixedPoint(123, 1)),
    ("1234e2", None, FixedPoint(123400, 0)),
    ("1234e2", 4, FixedPoint(1234000000, 4)),
    ("-1234e-2", None, FixedPoint(-1234, 2)),
    ("-1234e-2", 4, FixedPoint(-123400, 4)),
    ("-1234e-2", 1, FixedPoint(-123, 1)),
    ("-1234e2", None, FixedPoint(-123400, 0)),
    ("-1234e2", 4, FixedPoint(-1234000000, 4)),
    ("1.234e-2", None, FixedPoint(1234, 5)),
    ("1.234e-2", 7, FixedPoint(123400, 7)),
    ("1.234e-2", 3, FixedPoint(12, 3)),
    ("-1.234e-2", None, FixedPoint(-1234, 5)),
    ("-1.234e-2", 7, FixedPoint(-123400, 7)),
    ("-1.234e-2", 3, FixedPoint(-12, 3)),
]

repr_params = [
    (FixedPoint(123, 5), "0.00123"),
    (FixedPoint(10**100, 0), str(10**100)),
    (FixedPoint(10**100, 5), str(10**95) + "." + 5 * "0"),
    (FixedPoint(10001, 4), "1.0001"),
]

int_params = [
    (1, None, FixedPoint(1, 0)),
    (1, 2, FixedPoint(100, 2)),
    (-12345, None, FixedPoint(-12345, 0)),
    (-12345, 3, FixedPoint(-12345000, 3)),
    (np.int16(1), None, FixedPoint(1, 0)),
    (np.int16(1), 2, FixedPoint(100, 2)),
    (np.int16(-12345), None, FixedPoint(-12345, 0)),
    (np.int16(-12345), 3, FixedPoint(-12345000, 3)),
    (np.int32(1), None, FixedPoint(1, 0)),
    (np.int32(1), 2, FixedPoint(100, 2)),
    (np.int32(-12345), None, FixedPoint(-12345, 0)),
    (np.int32(-12345), 3, FixedPoint(-12345000, 3)),
    (np.int64(1), None, FixedPoint(1, 0)),
    (np.int64(1), 2, FixedPoint(100, 2)),
    (np.int64(-12345), None, FixedPoint(-12345, 0)),
    (np.int64(-12345), 3, FixedPoint(-12345000, 3)),
]

if USE_GMPY2:
    int_params += [
        (gmpy2.mpz(1), None, FixedPoint(1, 0)),
        (gmpy2.mpz(1), 2, FixedPoint(100, 2)),
        (gmpy2.mpz(-12345), None, FixedPoint(-12345, 0)),
        (gmpy2.mpz(-12345), 3, FixedPoint(-12345000, 3)),
    ]

float_params = [
    (0.00123, None, FixedPoint(123, 5)),
    (0.0001, None, FixedPoint(1, 4)),
    (12300.0045, None, FixedPoint(123000045, 4)),
    (12300.0045, 3, FixedPoint(12300005, 3)),
    (-12300.0045, None, FixedPoint(-123000045, 4)),
    (-12300.0045, 3, FixedPoint(-12300005, 3)),
    (1234e-2, None, FixedPoint(1234, 2)),
    (1234e-2, 4, FixedPoint(123400, 4)),
    (1234e-2, 1, FixedPoint(123, 1)),
    (1234e2, None, FixedPoint(123400, 0)),
    (1234e2, 4, FixedPoint(1234000000, 4)),
    (-1234e-2, None, FixedPoint(-1234, 2)),
    (-1234e-2, 4, FixedPoint(-123400, 4)),
    (-1234e-2, 1, FixedPoint(-123, 1)),
    (-1234e2, None, FixedPoint(-123400, 0)),
    (-1234e2, 4, FixedPoint(-1234000000, 4)),
    (1.234e-2, None, FixedPoint(1234, 5)),
    (1.234e-2, 7, FixedPoint(123400, 7)),
    (1.234e-2, 3, FixedPoint(12, 3)),
    (-1.234e-2, None, FixedPoint(-1234, 5)),
    (-1.234e-2, 7, FixedPoint(-123400, 7)),
    (-1.234e-2, 3, FixedPoint(-12, 3)),
    (np.float16(0.00123), None, FixedPoint(123, 5)),
    (np.float16(0.0001), None, FixedPoint(1, 4)),
    (np.float16(1234e-2), None, FixedPoint(1234, 2)),
    (np.float16(1234e-2), 4, FixedPoint(123400, 4)),
    (np.float16(1234e-2), 1, FixedPoint(123, 1)),
    (np.float16(-1234e-2), None, FixedPoint(-1234, 2)),
    (np.float16(-1234e-2), 4, FixedPoint(-123400, 4)),
    (np.float16(-1234e-2), 1, FixedPoint(-123, 1)),
    (np.float16(1.234e-2), None, FixedPoint(1234, 5)),
    (np.float16(1.234e-2), 7, FixedPoint(123400, 7)),
    (np.float16(1.234e-2), 3, FixedPoint(12, 3)),
    (np.float16(-1.234e-2), None, FixedPoint(-1234, 5)),
    (np.float16(-1.234e-2), 7, FixedPoint(-123400, 7)),
    (np.float16(-1.234e-2), 3, FixedPoint(-12, 3)),
    (np.float32(0.00123), None, FixedPoint(123, 5)),
    (np.float32(0.0001), None, FixedPoint(1, 4)),
    (np.float32(12300.0045), 3, FixedPoint(12300005, 3)),
    (np.float32(-12300.0045), 3, FixedPoint(-12300005, 3)),
    (np.float32(1234e-2), None, FixedPoint(1234, 2)),
    (np.float32(1234e-2), 4, FixedPoint(123400, 4)),
    (np.float32(1234e-2), 1, FixedPoint(123, 1)),
    (np.float32(1234e2), None, FixedPoint(123400, 0)),
    (np.float32(1234e2), 4, FixedPoint(1234000000, 4)),
    (np.float32(-1234e-2), None, FixedPoint(-1234, 2)),
    (np.float32(-1234e-2), 4, FixedPoint(-123400, 4)),
    (np.float32(-1234e-2), 1, FixedPoint(-123, 1)),
    (np.float32(-1234e2), None, FixedPoint(-123400, 0)),
    (np.float32(-1234e2), 4, FixedPoint(-1234000000, 4)),
    (np.float32(1.234e-2), None, FixedPoint(1234, 5)),
    (np.float32(1.234e-2), 7, FixedPoint(123400, 7)),
    (np.float32(1.234e-2), 3, FixedPoint(12, 3)),
    (np.float32(-1.234e-2), None, FixedPoint(-1234, 5)),
    (np.float32(-1.234e-2), 7, FixedPoint(-123400, 7)),
    (np.float32(-1.234e-2), 3, FixedPoint(-12, 3)),
    (np.float64(0.00123), None, FixedPoint(123, 5)),
    (np.float64(0.0001), None, FixedPoint(1, 4)),
    (np.float64(12300.0045), None, FixedPoint(123000045, 4)),
    (np.float64(12300.0045), 3, FixedPoint(12300005, 3)),
    (np.float64(-12300.0045), None, FixedPoint(-123000045, 4)),
    (np.float64(-12300.0045), 3, FixedPoint(-12300005, 3)),
    (np.float64(1234e-2), None, FixedPoint(1234, 2)),
    (np.float64(1234e-2), 4, FixedPoint(123400, 4)),
    (np.float64(1234e-2), 1, FixedPoint(123, 1)),
    (np.float64(1234e2), None, FixedPoint(123400, 0)),
    (np.float64(1234e2), 4, FixedPoint(1234000000, 4)),
    (np.float64(-1234e-2), None, FixedPoint(-1234, 2)),
    (np.float64(-1234e-2), 4, FixedPoint(-123400, 4)),
    (np.float64(-1234e-2), 1, FixedPoint(-123, 1)),
    (np.float64(-1234e2), None, FixedPoint(-123400, 0)),
    (np.float64(-1234e2), 4, FixedPoint(-1234000000, 4)),
    (np.float64(1.234e-2), None, FixedPoint(1234, 5)),
    (np.float64(1.234e-2), 7, FixedPoint(123400, 7)),
    (np.float64(1.234e-2), 3, FixedPoint(12, 3)),
    (np.float64(-1.234e-2), None, FixedPoint(-1234, 5)),
    (np.float64(-1.234e-2), 7, FixedPoint(-123400, 7)),
    (np.float64(-1.234e-2), 3, FixedPoint(-12, 3)),
]

fxp_params = [
    (fxp(0.0001), None, FixedPoint(1, 4)),
    (fxp(0.0001), 5, FixedPoint(10, 5)),
    (fxp(0.0001), 3, FixedPoint(0, 3)),
    (fxp(0.0005), 3, FixedPoint(1, 3)),
]

subtraction_list = [
    ("1.001", "-2345.000000345", "2346.001000345"),
    (0.1, 0.3, "-0.2"),
    (42, 123456789, "-123456747"),
    (fxp(51, 3), fxp(300, 5), "-249.00000"),
    ("-5.001", "-5.001", "0.000"),
    ("-2222", "1111.111", "-3333.111"),
    ("-10.2", "-5.4", "-4.8"),
    ("987654321", "1.111", "987654319.889"),
]

sub_add_mul_div_list_wrong_type = [
    ("1.001", [-2345.000000345]),
    (0.1, (0.3,)),
    (42, [123456789]),
    (fxp(51, 3), [300, 5]),
    ("-5.001", (-5.001,)),
    ("-2222", [1111.111]),
    ("-10.2", (-5.4,)),
    ("987654321", [1.111]),
]

cal_list = [
    ([fxp("1.1"), fxp("2.2")], [fxp("1.1"), fxp("2.2")]),
    ([fxp("1.1"), fxp("2.22")], [fxp("1.10"), fxp("2.22")]),
    (
        [fxp("1.1"), fxp("2.22"), fxp("3.333")],
        [fxp("1.100"), fxp("2.220"), fxp("3.333")],
    ),
    (
        [fxp("-1.1"), fxp("2.22"), fxp("3.333")],
        [fxp("-1.100"), fxp("2.220"), fxp("3.333")],
    ),
    (
        [fxp("-1.1"), fxp("-2.22"), fxp("-3.333")],
        [fxp("-1.100"), fxp("-2.220"), fxp("-3.333")],
    ),
]

addition_list = [
    ("1.001", "2345.000000345", "2346.001000345"),
    (0.1, 0.3, "0.4"),
    (42, 123456789, "123456831"),
    (fxp(51, 3), fxp(300, 5), "351.00000"),
    ("-5.001", "5.001", "0.000"),
    ("-2222", "-1111.111", "-3333.111"),
    ("-10.2", "5.4", "-4.8"),
    ("987654321", "-1.111", "987654319.889"),
]

multiplication_list = [
    ("1.0101", "1.0010000", "1.0111101"),
    (0.1, 0.3, "0.0"),
    (42, 123456789, "5185185138"),
    (fxp(51, 3), fxp(300, 5), "15300.00000"),
    ("1.0101", "1.001", "1.0111"),
    (2 * 10**100, "0." + "0" * 97 + "200", "400." + "0" * 100),
    ("3", "4", "12"),
    (0.1999, 0.1, "0.0200"),
]

division_list = [
    ("1.0101", "1.0010000", "1.0090909"),
    (0.1, 0.3, "0.3"),
    (0.3, 0.1, "3.0"),
    (123456789, 42, "2939447"),
    (123456789, 42.0, "2939447.4"),
    ("123456789.00", 42.0, "2939447.36"),
    ("123456789.00", "42.000", "2939447.357"),
    (fxp(300, 5), fxp(51, 3), "5.88235"),
    ("1.0101", "1.001", "1.0091"),
    ("2", "3", "1"),
    ("2", "3.0", "0.7"),
    ("2.0", "3.0", "0.7"),
    ("2.0", "3", "0.7"),
]

rand_list = [
    (fxp(0, 200), fxp(2**200, 20), True),
    (fxp(5.0, 50), fxp(15.0, 50), False),
    (fxp(0.0, 20), fxp(1, 20), True),
    (fxp("1.00002"), fxp("5000.12"), False),
]


greater = lambda a, b: a > b
greater_equal = lambda a, b: a >= b
less = lambda a, b: a < b
less_equal = lambda a, b: a <= b
equal = lambda a, b: a == b

comp_list = [
    (greater, "1", "2", False),
    (greater, "-1", "-2", True),
    (less, "0.001", "0.00005", False),
    (less, "-0.001", "0.00005", True),
    (greater_equal, "1.02", "1.02", True),
    (greater_equal, "-1.02", "1.02", False),
    (greater_equal, "1.02", "-1.02", True),
    (equal, "1.001", "1.01", False),
    (equal, "123456.789", "123456.789", True),
    (equal, "123456.7890", "123456.789", True),
    (equal, "-123456.789", "123456.789", False),
    (less_equal, "-5.1", "-6.1", False),
    (less_equal, "5.1", "6.1", True),
]

comp_list_incorrect = [
    (greater, "1", [2]),
    (greater, "-1", [-2]),
    (less, "0.001", (0.00005,)),
    (less, "-0.001", (0.00005,)),
    (greater_equal, 1.02, [1.02]),
    (greater_equal, -1.02, [1.02]),
    (greater_equal, "1.02", [1.02]),
    (equal, "1.001", (1.01,)),
    (less_equal, "5.1", (6.1,)),
]

round_list = [
    (1234567, 4, 3, 123457),
    (1234567, 2, 4, 123456700),
    (1234567, 4, 2, 12346),
    (1234567, 5, 1, 123),
]

to_bool_params = [
    (FixedPoint(0, 0), False),
    (FixedPoint(0, 3), False),
    (FixedPoint(123, 1), True),
    (FixedPoint(-345, 5), True),
]

to_int_params = [
    (FixedPoint(100, 0), 100),
    (FixedPoint(100, 3), 0),
    (FixedPoint(150, 2), 2),
    (FixedPoint(149, 2), 1),
]

to_float_params = [
    (FixedPoint(1234, 3), 1.234),
    (FixedPoint(1, 0), 1.0),
    (FixedPoint(1500000, 6), 1.5),
]
