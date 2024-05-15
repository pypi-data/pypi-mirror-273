# Built-in imports
import unittest

# Local imports
from ..contract_primitives import (
    Side,
)

# TODO add tests for leverage, role and nominal units


class TestContractSide(unittest.TestCase):
    def test_from_string_works_for_known_api_values(self):
        self.assertEqual(Side.from_string('short'), Side.SHORT)
        self.assertEqual(Side.from_string('hedge'), Side.SHORT)
        self.assertEqual(Side.from_string('long'), Side.LONG)


if __name__ == '__main__':
    unittest.main()
