"""
Validate serialization logic of FixedPoint objects.
"""

import copy

import pytest

from tno.mpc.communication.packers import DefaultDeserializerOpts, DefaultSerializerOpts

from tno.mpc.encryption_schemes.utils.fixed_point import FixedPoint
from tno.mpc.encryption_schemes.utils.test.fixed_point_test_parameters import (
    string_params,
)


@pytest.mark.parametrize("_value, _precision, true_fxp", string_params)
def test_floating_point_serialization(
    _value: int, _precision: int, true_fxp: FixedPoint
) -> None:
    """
    Test the serialization logic.

    :param _value: a string representation of the fixed point (unused)
    :param _precision: the precision of the string representation of the fixed
        point (unused)
    :param true_fxp: the FixedPoint object corresponding to the string
        representation, to test the serialization logic on
    """
    obj = copy.deepcopy(true_fxp)
    obj_prime = FixedPoint.deserialize(
        obj.serialize(opts=DefaultSerializerOpts), opts=DefaultDeserializerOpts
    )
    assert obj == obj_prime
