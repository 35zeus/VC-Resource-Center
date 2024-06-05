import unittest
from models import AnnualType


class TestAnnualType(unittest.TestCase):
    test_case = AnnualType('June', '1st', 'Sat')

    def test_is_instance(self):
        self.assertIsInstance(self.test_case, AnnualType)


if __name__ == "__main__":
    unittest.main()
