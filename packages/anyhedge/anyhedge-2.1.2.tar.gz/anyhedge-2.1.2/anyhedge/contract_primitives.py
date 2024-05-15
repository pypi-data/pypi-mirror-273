# Built-in imports
from __future__ import annotations  # allow pre-definition use of types

# Local imports
from . import validators
from .bch_primitives import (
    SATS_PER_BCH,
    SCRIPT_INT_MAX,
)

# Built-in imports
from enum import Enum


class Role(str, Enum):
    MAKER = 'Maker'
    TAKER = 'Taker'
    SETTLEMENT_SERVICE = 'Settlement Service'
    PLATFORM = 'Platform'
    OTHER = 'Other'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()


class Side(str, Enum):
    SHORT = 'Short'
    LONG = 'Long'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    @property
    def other_side(self) -> Side:
        # use a lookup to ensure KeyError with unknown value
        return {Side.SHORT: Side.LONG, Side.LONG: Side.SHORT}[self]

    @classmethod
    def from_string(cls, side_string: str) -> Side:
        # use a lookup to ensure KeyError with unknown value
        lookup = {
            'short': cls.SHORT,
            'hedge': cls.SHORT,
            'long': cls.LONG,
        }
        return lookup[side_string.lower()]


class NominalOracleUnitsXSatsPerBch(int):
    def __init__(self, value):
        super().__init__()
        validators.instance(value, int)  # i.e. don't allow silent coercion
        validators.less_equal(self, SCRIPT_INT_MAX)
        validators.greater_equal(self, SATS_PER_BCH)  # i.e. minimum is 1 nominal oracle unit


class ShortLeverage(float):
    min_allowed: float = 1.0
    max_allowed: float = 50.0

    def __init__(self, _):
        super().__init__()
        validators.less_equal(self, self.max_allowed * 1.00001)  # some room for floating point error
        validators.greater_equal(self, self.min_allowed)  # strict boundary for flat hedge position, below one is undefined


class LongLeverage(float):
    min_allowed: float = 1.1
    max_allowed: float = 50.0

    def __init__(self, _):
        super().__init__()
        validators.less_equal(self, self.max_allowed * 1.00001)  # some room for floating point error
        validators.greater_equal(self, self.min_allowed * 0.99999)  # some room for floating point error
