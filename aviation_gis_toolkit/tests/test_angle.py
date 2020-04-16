import unittest
from aviation_gis_toolkit.angle import *


class AngleTests(unittest.TestCase):

    def test_angle_is_within_range(self):
        self.assertEqual(Angle.is_angle_within_range(-90.1, AT_LAT), False)
        self.assertEqual(Angle.is_angle_within_range(-90, AT_LAT), True)
        self.assertEqual(Angle.is_angle_within_range(90, AT_LAT), True)
        self.assertEqual(Angle.is_angle_within_range(90.1, AT_LAT), False)

        self.assertEqual(Angle.is_angle_within_range(-180.1, AT_LON), False)
        self.assertEqual(Angle.is_angle_within_range(-180, AT_LON), True)
        self.assertEqual(Angle.is_angle_within_range(180, AT_LON), True)
        self.assertEqual(Angle.is_angle_within_range(180.1, AT_LON), False)

    def test_get_hemisphere_character(self):
        self.assertEqual(None, Angle.get_hemisphere_character(0, AT_LAT))
        self.assertEqual('S', Angle.get_hemisphere_character(-1, AT_LAT))
        self.assertEqual('N', Angle.get_hemisphere_character(1, AT_LAT))
        self.assertEqual('E', Angle.get_hemisphere_character(1, AT_LON))
        self.assertEqual('W', Angle.get_hemisphere_character(-1, AT_LON))
        self.assertEqual(None, Angle.get_hemisphere_character('-1', AT_LON))

    def test_dd_to_dms_parts(self):
        self.assertEqual(Angle.dd_to_dms_parts(0), (1, 0, 0, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(-1), (-1, 1, 0, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(10), (1, 10, 0, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(45.5), (1, 45, 30, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(1.0169444444444400), (1, 1, 1, 1.0))
        self.assertEqual(Angle.dd_to_dms_parts(100.1694444444444000), (1, 100, 10, 10.0))
        self.assertEqual(Angle.dd_to_dms_parts(-120.3388888888889000), (-1, 120, 20, 20.0))
        self.assertEqual(Angle.dd_to_dms_parts(145.9589599661111, prec=6), (1, 145, 57, 32.255878))

    def test_dd_to_dms_string(self):

        latitude_test_data = [('00 00 00.000 N', 0),
                              (None, -90.1),
                              ('90 00 00.000 S', -90),
                              ('90 00 00.000 N', 90),
                              (None, 90.1),
                              ('01 00 00 N', 1, 0),
                              ('45 30 00.0 N', 45.5, 1),
                              ('45 30 00.00 S', -45.5, 2),
                              ('01 01 01.000 N', 1.0169444444444400),
                              ('45 57 32.256 S', -45.9589599661111000),
                              ('45 57 32.3 N', +45.9589599661111000, 1),
                              ('45 57 32.26 S', -45.9589599661111000, 2),
                              ('45 57 32.256 N', 45.9589599661111000, 3),
                              ('45 57 32.2559 S', -45.9589599661111000, 4),
                              ('45 57 32.25588 N', 45.9589599661111000, 5),
                              ('45 57 32.255878 S', -45.9589599661111000, 6),
                              ('45 57 32.2558780 N', 45.9589599661111000, 7)]

        for test_item in latitude_test_data:
            if len(test_item) == 2:
                self.assertEqual(test_item[0], Angle.dd_to_dms_string(test_item[1], AT_LAT))
            elif len(test_item) == 3:
                self.assertEqual(test_item[0], Angle.dd_to_dms_string(test_item[1], AT_LAT, prec=test_item[2]))

        self.assertEqual('N 45 57 32.256',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_HDMS_ALL_SEP))
        self.assertEqual('N45 57 32.256',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_HDMS_SEP))
        self.assertEqual('45 57 32.256N',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_DMSH_SEP))
        self.assertEqual('45\xb057\'32.256\'\' N',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_DMSH_SEP_SYMBOLS))
        self.assertEqual('N 45\xb057\'32.256\'\'',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_HDMS_SEP_SYMBOLS))
        self.assertEqual('N455732.256',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_HDMS_COMP))
        self.assertEqual('455732.256N',
                         Angle.dd_to_dms_string(45.9589599661111000, AT_LAT, ang_format=AF_DMSH_COMP))

        # Longitude
        longitude_test_data = [('000 00 00.000 E', 0),
                               (None, -180.1),
                               ('180 00 00.000 W', -180),
                               ('180 00 00.000 E', 180),
                               (None, 180.1),
                               ('001 00 00 E', 1, 0),
                               ('045 30 00.0 E', 45.5, 1),
                               ('045 30 00.00 W', -45.5, 2),
                               ('001 01 01.000 E', 1.0169444444444400),
                               ('045 57 32.256 W', -45.9589599661111000),
                               ('045 57 32.3 E', +45.9589599661111000, 1),
                               ('045 57 32.26 W', -45.9589599661111000, 2),
                               ('045 57 32.256 E', 45.9589599661111000, 3),
                               ('045 57 32.2559 W', -45.9589599661111000, 4),
                               ('045 57 32.25588 E', 45.9589599661111000, 5),
                               ('045 57 32.255878 W', -45.9589599661111000, 6),
                               ('145 57 32.2558780 E', 145.9589599661111000, 7)]

        for test_item in longitude_test_data:
            if len(test_item) == 2:
                self.assertEqual(test_item[0], Angle.dd_to_dms_string(test_item[1], AT_LON))
            elif len(test_item) == 3:
                self.assertEqual(test_item[0], Angle.dd_to_dms_string(test_item[1], AT_LON, prec=test_item[2]))

        self.assertEqual('E 145 57 32.256',
                         Angle.dd_to_dms_string(145.9589599661111000, AT_LON, ang_format=AF_HDMS_ALL_SEP))
        self.assertEqual('W145 57 32.256',
                         Angle.dd_to_dms_string(-145.9589599661111000, AT_LON, ang_format=AF_HDMS_SEP))
        self.assertEqual('145 57 32.256E',
                         Angle.dd_to_dms_string(145.9589599661111000, AT_LON, ang_format=AF_DMSH_SEP))
        self.assertEqual('145\xb057\'32.256\'\' W',
                         Angle.dd_to_dms_string(-145.9589599661111000, AT_LON, ang_format=AF_DMSH_SEP_SYMBOLS))
        self.assertEqual('E 145\xb057\'32.256\'\'',
                         Angle.dd_to_dms_string(145.9589599661111000, AT_LON, ang_format=AF_HDMS_SEP_SYMBOLS))
        self.assertEqual('W1455732.256',
                         Angle.dd_to_dms_string(-145.9589599661111000, AT_LON, ang_format=AF_HDMS_COMP))
        self.assertEqual('1455732.256E',
                         Angle.dd_to_dms_string(145.9589599661111000, AT_LON, ang_format=AF_DMSH_COMP))

    def test_get_hemisphere_prefix_from_angle(self):
        self.assertEqual(None, Angle.get_hemisphere_prefix_from_angle(''))
        self.assertEqual(None, Angle.get_hemisphere_prefix_from_angle('test'))
        self.assertEqual('N', Angle.get_hemisphere_prefix_from_angle('N 45 55 21.77'))
        self.assertEqual(None, Angle.get_hemisphere_prefix_from_angle('45N 55 21.77'))
        self.assertEqual(None, Angle.get_hemisphere_prefix_from_angle('45 55 21.77N'))

    def test_get_hemisphere_suffix_from_angle(self):
        self.assertEqual(None, Angle.get_hemisphere_suffix_from_angle(''))
        self.assertEqual(None, Angle.get_hemisphere_suffix_from_angle('test'))
        self.assertEqual(None, Angle.get_hemisphere_suffix_from_angle('N 32 44 55'))
        self.assertEqual('W', Angle.get_hemisphere_suffix_from_angle('101 22 55W'))
        self.assertEqual(None, Angle.get_hemisphere_suffix_from_angle('101 22 W55'))

    def test_get_dms_parts(self):
        self.assertEqual((0, 0, 0.0), Angle.get_dms_parts('0 0 0'))
        self.assertEqual((0, 0, 0.0), Angle.get_dms_parts('00 00 0.00'))
        self.assertEqual((-9, 1, 0.47), Angle.get_dms_parts('-09 01 0.47'))
        self.assertEqual(None, Angle.get_dms_parts('09010.47'))
        self.assertEqual(None, Angle.get_dms_parts('09 01 '))
        self.assertEqual(None, Angle.get_dms_parts(' 01 '))
        self.assertEqual(None, Angle.get_dms_parts('AA TEST TEST'))
        self.assertEqual(None, Angle.get_dms_parts('AA 50 TEST'))
        self.assertEqual(None, Angle.get_dms_parts('1 1.22 3'))
        self.assertEqual(None, Angle.get_dms_parts('1.33 2.55 3.22'))
        self.assertEqual(None, Angle.get_dms_parts('1.55 2 4'))
        self.assertEqual((25, 44, 32.47), Angle.get_dms_parts('25 44 32.47'), )
        self.assertEqual(None, Angle.get_dms_parts(25), None)

    def test_dms_separated_no_hemisphere_to_dd(self):
        # Test Latitude
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('1', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('1 1', AT_LAT))
        self.assertAlmostEqual(0.0, Angle.dms_separated_no_hemisphere_to_dd('0 0 0', AT_LAT))
        self.assertAlmostEqual(1.0, Angle.dms_separated_no_hemisphere_to_dd('1 0 0', AT_LAT))
        self.assertAlmostEqual(90.0, Angle.dms_separated_no_hemisphere_to_dd('90 0 0', AT_LAT))
        self.assertAlmostEqual(-90.0, Angle.dms_separated_no_hemisphere_to_dd('-90 0 0', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('45 60 15', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('45 15 60', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('-91 0 0', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('91 0 0', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('90 01 0', AT_LAT))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('90 00 01.10', AT_LAT))
        self.assertEqual(45.5, Angle.dms_separated_no_hemisphere_to_dd('45 30 00.00', AT_LON))
        self.assertAlmostEqual(1.0169444444444400, Angle.dms_separated_no_hemisphere_to_dd('1 1 1', AT_LAT))
        self.assertAlmostEqual(1.0169444444444400, Angle.dms_separated_no_hemisphere_to_dd('01 01 01.00', AT_LAT))
        self.assertAlmostEqual(10.1694444444444000, Angle.dms_separated_no_hemisphere_to_dd('10 10 10.00', AT_LAT))
        self.assertAlmostEqual(20.3388888888889000, Angle.dms_separated_no_hemisphere_to_dd('20 20 20.00', AT_LAT))
        self.assertAlmostEqual(45.9589599661111000,
                               Angle.dms_separated_no_hemisphere_to_dd('45 57 32.25578', AT_LAT))

        # Test Longitude
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('1', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('1 1', AT_LON))
        self.assertAlmostEqual(0.0, Angle.dms_separated_no_hemisphere_to_dd('0 0 0', AT_LON))
        self.assertAlmostEqual(1.0, Angle.dms_separated_no_hemisphere_to_dd('1 0 0', AT_LON))
        self.assertAlmostEqual(180.0, Angle.dms_separated_no_hemisphere_to_dd('180 0 0', AT_LON))
        self.assertAlmostEqual(-180., Angle.dms_separated_no_hemisphere_to_dd('-180 0 0', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('145 60 15', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('145 15 60', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('-181 0 0', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('181 0 0', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('180 01 0', AT_LON))
        self.assertEqual(None, Angle.dms_separated_no_hemisphere_to_dd('180 00 01.10', AT_LON))
        self.assertEqual(90.5, Angle.dms_separated_no_hemisphere_to_dd('090 30 00.00', AT_LON))
        self.assertAlmostEqual(1.0169444444444400, Angle.dms_separated_no_hemisphere_to_dd('1 1 1', AT_LON))
        self.assertAlmostEqual(1.0169444444444400, Angle.dms_separated_no_hemisphere_to_dd('001 01 01.00', AT_LON))
        self.assertAlmostEqual(100.1694444444444000,
                               Angle.dms_separated_no_hemisphere_to_dd('100 10 10.00', AT_LON))
        self.assertAlmostEqual(120.3388888888889000,
                               Angle.dms_separated_no_hemisphere_to_dd('120 20 20.00', AT_LON))
        self.assertAlmostEqual(145.9589599661111,
                               Angle.dms_separated_no_hemisphere_to_dd('145 57 32.255878', AT_LON))

    def test_dms_compacted_no_hemisphere_to_dd(self):

        lat_compacted_test_data = [(None, ''),
                                   (None, '1'),
                                   (None, '1'),
                                   (None, '45000.000'),
                                   (90, '900000'),
                                   (None, '910000'),
                                   (None, '900100.0'),
                                   (None, '900000.01'),
                                   (None, '906000'),
                                   (None, '900060'),
                                   (-90, '-900000.0000'),
                                   (None, '-900001.1'),
                                   (45.5, '453000.000'),
                                   (20.33888888888889, '202020.000'),
                                   (-45.95895996611112, '-455732.255878')]

        for test_item in lat_compacted_test_data:
            self.assertEqual(test_item[0], Angle.dms_compacted_no_hemisphere_to_dd(test_item[1], AT_LAT))

        lon_compacted_test_data = [(None, ''),
                                   (None, '1'),
                                   (None, '1'),
                                   (None, '45000.000'),
                                   (180, '1800000'),
                                   (None, '1810000'),
                                   (None, '1800100.0'),
                                   (None, '1800000.01'),
                                   (None, '1806000'),
                                   (None, '1800060'),
                                   (-180, '-1800000.0000'),
                                   (None, '-1800001.1'),
                                   (145.5, '1453000.000'),
                                   (20.33888888888889, '0202020.000'),
                                   (145.95895996611112, '1455732.255878')]

        for test_item in lon_compacted_test_data:
            self.assertEqual(test_item[0], Angle.dms_compacted_no_hemisphere_to_dd(test_item[1], AT_LON))

    def test_angle_no_hemisphere_to_dd(self):

        lat_test_data = [(None, ''),
                         (1.0, 1),
                         (None, -90.1),
                         (None, '-90.1'),
                         (-90.0, -90),
                         (-90.0, '-90'),
                         (-90.0, '-90,00'),
                         (90.0, 90),
                         (90.0, '90'),
                         (90.0, '90,0'),
                         (None, 90.1),
                         (None, '90.1'),
                         (None, '90 00 00.01'),
                         (None, '90 00 00,01'),
                         (90.0, '90 00 00,00'),
                         (None, '90 01 00.00'),
                         (None, '91 00 00.00'),
                         (None, '900000.01'),
                         (45.95895996611112, '45 57 32.255878'),
                         (45.95895996611112, '455732.255878'),
                         (-45.95895996611112, '-455732.255878'),
                         (-45.95895996611112, '-45 57 32.255878')]

        for test_item in lat_test_data:
            self.assertEqual(test_item[0], Angle.angle_no_hemisphere_to_dd(test_item[1], AT_LAT))

        lat_test_data = [(None, ''),
                         (1.0, 1),
                         (None, 180.1),
                         (None, '180.1'),
                         (-180.0, -180),
                         (-180.0, '-180'),
                         (-180.0, '-180,00'),
                         (180.0, 180),
                         (180.0, '180'),
                         (180.0, '180,0'),
                         (None, 180.1),
                         (None, '180.1'),
                         (None, '180 00 00.01'),
                         (None, '180 00 00,01'),
                         (180.0, '180 00 00,00'),
                         (None, '180 01 00.00'),
                         (None, '181 00 00.00'),
                         (None, '1800000.01'),
                         (45.95895996611112, '045 57 32.255878'),
                         (45.95895996611112, '0455732.255878'),
                         (-45.95895996611112, '-0455732.255878'),
                         (-45.95895996611112, '-045 57 32.255878')]

        for test_item in lat_test_data:
            self.assertEqual(test_item[0], Angle.angle_no_hemisphere_to_dd(test_item[1], AT_LON))
