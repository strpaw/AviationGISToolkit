import unittest
from aviation_gis_toolkit.base_tools import BasicTools


class BasicToolsTests(unittest.TestCase):

    def test_normalize_src_value(self):
        self.assertEqual(BasicTools.get_normalized_src_value(-10.55), '-10.55')
        self.assertEqual(BasicTools.get_normalized_src_value('   n 10 20 30,55   \n'), 'N 10 20 30.55')

    def test_is_within_range(self):
        self.assertEqual(BasicTools.is_within_range(-10.1, -10, 10), False)
        self.assertEqual(BasicTools.is_within_range(-10, -10, 10), True)
        self.assertEqual(BasicTools.is_within_range(10, -10, 10), True)
        self.assertEqual(BasicTools.is_within_range(10.1, -10, 10), False)

    def test_get_value_as_float(self):
        self.assertEqual(BasicTools.get_value_as_float_number(-10.5), -10.5)
        self.assertEqual(BasicTools.get_value_as_float_number(10), 10.0)
        self.assertEqual(BasicTools.get_value_as_float_number('-10.5'), -10.5)
        self.assertEqual(BasicTools.get_value_as_float_number('10'), 10)
        self.assertEqual(BasicTools.get_value_as_float_number('test'), None)

    def test_get_value_as_int(self):
        self.assertEqual(BasicTools.get_value_as_int_number(-1), -1)
        self.assertEqual(BasicTools.get_value_as_int_number(1.5), None)
        self.assertEqual(BasicTools.get_value_as_int_number('1.5'), None)
        self.assertEqual(BasicTools.get_value_as_int_number('1'), 1)
        self.assertEqual(BasicTools.get_value_as_int_number('test'), None)