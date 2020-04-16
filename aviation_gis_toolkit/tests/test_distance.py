import unittest
from aviation_gis_toolkit.distance import Distance
from aviation_gis_toolkit.const import *


class DistanceTests(unittest.TestCase):

    def test_get_normalized_src_value(self):
        self.assertEqual('152.11', Distance.get_normalized_src_value(' 152,11   '))

    def test_is_dist_number(self):

        is_number, err_msg, num = Distance.is_dist_number(35.55)
        self.assertEqual(True, is_number)
        self.assertEqual('', err_msg)
        self.assertEqual(35.55, num)

        is_number, err_msg, num = Distance.is_dist_number('  35,55 ')
        self.assertEqual(True, is_number)
        self.assertEqual('', err_msg)
        self.assertEqual(35.55, num)

        is_number, err_msg, num = Distance.is_dist_number('')
        self.assertEqual(False, is_number)
        self.assertEqual('Distance error. Distance value can not be empty.', err_msg)
        self.assertEqual(None, num)

        is_number, err_msg, num = Distance.is_dist_number('            ')
        self.assertEqual(False, is_number)
        self.assertEqual('Distance error. Distance value can not be empty.', err_msg)
        self.assertEqual(None, num)

        is_number, err_msg, num = Distance.is_dist_number('test')
        self.assertEqual(False, is_number)
        self.assertEqual('Distance error. Value test can not be converted to number.', err_msg)
        self.assertEqual(None, num)

        is_number, err_msg, num = Distance.is_dist_number('t143.55')
        self.assertEqual(False, is_number)
        self.assertEqual('Distance error. Value t143.55 can not be converted to number.', err_msg)
        self.assertEqual(None, num)

        is_number, err_msg, num = Distance.is_dist_number('-435,22')
        self.assertEqual(False, is_number)
        self.assertEqual('Distance error. Distance not be less than 0.', err_msg)
        self.assertEqual(None, num)


    def test_is_uom(self):

        is_uom, err_msg = Distance.is_uom(UOM_M)
        self.assertEqual(True, is_uom)
        self.assertEqual('', err_msg)

        is_uom, err_msg = Distance.is_uom('           ')
        self.assertEqual(False, is_uom)
        self.assertEqual('Distance error. UOM is required and cannot be empty.', err_msg)

        is_uom, err_msg = Distance.is_uom('TEST')
        self.assertEqual(False, is_uom)
        self.assertEqual('Distance error. UOM TEST is not valid.', err_msg)

        is_uom, err_msg = Distance.is_uom(1)
        self.assertEqual(False, is_uom)
        self.assertEqual('Distance error. UOM must be a string.', err_msg)

    def test_check_distance(self):
        """ Note: check_distance method is called during class instance initialization """
        dist = Distance('', 'TEST')
        self.assertEqual(False, dist.is_valid)
        self.assertEqual('Distance error. Distance value can not be empty.Distance error. UOM TEST is not valid.', dist.err_msg)

        dist = Distance('')
        self.assertEqual(False, dist.is_valid)
        self.assertEqual('Distance error. Distance value can not be empty.', dist.err_msg)

        dist = Distance(123, 1)
        self.assertEqual(False, dist.is_valid)
        self.assertEqual('Distance error. UOM must be a string.', dist.err_msg)

        dist = Distance(-123, 1)
        self.assertEqual(False, dist.is_valid)
        self.assertEqual('Distance error. Distance not be less than 0.Distance error. UOM must be a string.', dist.err_msg)

    def test_convert_dist_to_m(self):
        dist = Distance(135.75)
        dist.convert_dist_to_m()
        self.assertEqual(135.75, dist.convert_dist_to_m())

        dist = Distance(1.0455, UOM_KM)
        dist.convert_dist_to_m()
        self.assertEqual(1045.5, dist.convert_dist_to_m())

        dist = Distance(17.355, UOM_NM)
        dist.convert_dist_to_m()
        self.assertEqual(32141.46, dist.convert_dist_to_m())

        dist = Distance(783.2, UOM_FT)
        dist.convert_dist_to_m()
        self.assertAlmostEqual(238.71936, dist.convert_dist_to_m())

        dist = Distance(5.8, UOM_SM)
        dist.convert_dist_to_m()
        self.assertEqual(9334.1952, dist.convert_dist_to_m())

    def test_convert_m_to_given_uom(self):
        self.assertEqual(1000, Distance.convert_m_to_given_uom(1000, UOM_M))
        self.assertEqual(0.45522, Distance.convert_m_to_given_uom(455.22, UOM_KM))
        self.assertAlmostEqual(1, Distance.convert_m_to_given_uom(1852, UOM_NM))
        self.assertAlmostEqual(841.53543307086600, Distance.convert_m_to_given_uom(256.5, UOM_FT))
        self.assertAlmostEqual(4.880994989262710000, Distance.convert_m_to_given_uom(7855.2, UOM_SM))

    def test_convert_dist_to_uom(self):

        dist = Distance(1455)
        self.assertEqual(1455, dist.convert_dist_to_uom(UOM_M))
        self.assertEqual(1.455, dist.convert_dist_to_uom(UOM_KM))
        self.assertEqual(0.7856371490280778, dist.convert_dist_to_uom(UOM_NM))
        self.assertEqual(4773.622047244095, dist.convert_dist_to_uom(UOM_FT))
        self.assertEqual(0.9040950847053209, dist.convert_dist_to_uom(UOM_SM))

        dist = Distance(1.455, UOM_KM)
        self.assertEqual(1455, dist.convert_dist_to_uom(UOM_M))
        self.assertEqual(1.455, dist.convert_dist_to_uom(UOM_KM))
        self.assertAlmostEqual(0.7856371490280778, dist.convert_dist_to_uom(UOM_NM))
        self.assertAlmostEqual(4773.622047244095, dist.convert_dist_to_uom(UOM_FT))
        self.assertAlmostEqual(0.9040950847053209, dist.convert_dist_to_uom(UOM_SM))

        dist = Distance(2.79, UOM_NM)
        self.assertEqual(5167.08, dist.convert_dist_to_uom(UOM_M))
        self.assertEqual(5.16708, dist.convert_dist_to_uom(UOM_KM))
        self.assertEqual(2.79, dist.convert_dist_to_uom(UOM_NM))
        self.assertAlmostEqual(16952.3622047244000, dist.convert_dist_to_uom(UOM_FT))
        self.assertAlmostEqual(3.21067465998568, dist.convert_dist_to_uom(UOM_SM))

        dist = Distance(3722.5, UOM_FT)
        self.assertAlmostEqual(1134.6180000000002, dist.convert_dist_to_uom(UOM_M))
        self.assertAlmostEqual(1.1346180000000002, dist.convert_dist_to_uom(UOM_KM))
        self.assertAlmostEqual(0.6126447084233262, dist.convert_dist_to_uom(UOM_NM))
        self.assertEqual(3722.5, dist.convert_dist_to_uom(UOM_FT))
        self.assertAlmostEqual(0.7050189393939394, dist.convert_dist_to_uom(UOM_SM))

        dist = Distance(2.3, UOM_SM)
        self.assertAlmostEqual(3701.4912, dist.convert_dist_to_uom(UOM_M))
        self.assertAlmostEqual(3.7014912, dist.convert_dist_to_uom(UOM_KM))
        self.assertAlmostEqual(1.9986453563714903, dist.convert_dist_to_uom(UOM_NM))
        self.assertEqual(12144.0, dist.convert_dist_to_uom(UOM_FT))
        self.assertAlmostEqual(2.3, dist.convert_dist_to_uom(UOM_SM))
