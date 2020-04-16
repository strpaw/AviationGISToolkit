import unittest
from aviation_gis_toolkit.coordinate_predetermined import *
from aviation_gis_toolkit.const import *


class CoordinatePredeterminedTests(unittest.TestCase):

    def test_is_given_format(self):
        # DMSH Longitude check
        ang = ''
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1732235.41W'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0430900E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0035959.9E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0000100.00W'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '0015903.15S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1806159.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '002234.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1812343.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        # DMSH Latitude check
        ang = '732235.41S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '093259N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '005959.41N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '001400S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '1235959S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '076352.44N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '592234.15E'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = '912335.15N'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        # HDMS Longitude check
        ang = 'W1732235.41'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E0430900'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E0035959.9'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'W0000100.00'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'S0015903.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E1806159.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E002234.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E1812343.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        # HDMS Latitude check
        ang = 'S732235.41'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N093259'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N005959.41'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'S001400'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'S1235959'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N076352.44'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'E592234.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

        ang = 'N912335.15'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual(False, CoordinatePredetermined.is_given_format(ang, regex))

    def test_get_dms_coordinate_parts(self):

        # DMSH Longitude
        ang = '1233456.211W'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LON]
        self.assertEqual((123, 34, 56.211, 'W'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

        # DMSH Latitude
        ang = '233456S'
        regex = ANGLE_PATTERNS[AF_DMSH_COMP][AT_LAT]
        self.assertEqual((23, 34, 56.0, 'S'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

        # HDMS Longitude
        ang = 'E0233456'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LON]
        self.assertEqual((23, 34, 56.0, 'E'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

        # HDMS Latitude
        ang = 'N233456.011'
        regex = ANGLE_PATTERNS[AF_HDMS_COMP][AT_LAT]
        self.assertEqual((23, 34, 56.011, 'N'),
                         CoordinatePredetermined.get_dms_coordinate_parts(ang, regex))

    def test_dms_parts_to_dd(self):
        dms_parts = (100, 30, 0.0, 'S')
        self.assertEqual(-100.5, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (47, 30, 0.0, 'N')
        self.assertEqual(47.5, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (100, 60, 0.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (100, 22, 60.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (180, 60, 0.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

        dms_parts = (180, 0, 0.0, 'E')
        self.assertEqual(180, CoordinatePredetermined.dms_parts_to_dd(dms_parts))

    def test_dms_to_dd(self):

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(-135.5, ang.dms_to_dd('1353000.000W'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(-135.68944444444446, ang.dms_to_dd('1354122.000W'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(None, ang.dms_to_dd('1800100.000W'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(None, ang.dms_to_dd('180000.001E'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LON)
        self.assertEqual(135.5, ang.dms_to_dd('1353000.000E'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LAT)
        self.assertEqual(-35.5, ang.dms_to_dd('353000.000S'))

        ang = CoordinatePredetermined(AF_DMSH_COMP, AT_LAT)
        self.assertEqual(35.5, ang.dms_to_dd('353000.000N'))

        ang = CoordinatePredetermined(AF_HDMS_COMP, AT_LAT)
        self.assertEqual(-35.5, ang.dms_to_dd('S353000.000'))


class CoordinatePredeterminedDMFormatsTest(unittest.TestCase):

    def test_is_given_format(self):
        # DMH longitude
        regex = ANGLE_PATTERNS[AF_DMH_COMP][AT_LON]

        dmh_lon_valid = ['18000E',
                         '18000.0000W',
                         '17900E',
                         '17959.999W',
                         '17000.999W',
                         '09959.99W',
                         '09900E',
                         '00900W',
                         '00900.0000E',
                         '00959.99W',
                         '00059.99E',
                         '00000W',
                         '00000.000E',
                         '00000.001W',
                         '00959.99W',
                         '00009E',
                         '00009.0W',
                         '00000W']

        for ang in dmh_lon_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        # HDM longitude
        regex = ANGLE_PATTERNS[AF_HDM_COMP][AT_LON]

        hdm_lon_valid = ['E18000',
                         'W18000.0000',
                         'E17900',
                         'W17959.999',
                         'W17000.999',
                         'W09959.99',
                         'E09900',
                         'W00900',
                         'E00900.0000',
                         'W00959.99',
                         'E00059.99',
                         'W00000',
                         'E00000.000',
                         'W00000.001',
                         'W00959.99',
                         'E00009',
                         'W00009.0',
                         'W00000']

        for ang in hdm_lon_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        # DMH latitude
        regex = ANGLE_PATTERNS[AF_DMH_COMP][AT_LAT]

        dmh_lat_valid = ['9000N',
                         '9000.0000S',
                         '8900N',
                         '8959.999S',
                         '8000.999S',
                         '0900N',
                         '0900S',
                         '0900.0000N',
                         '0959.99S',
                         '0059.99S',
                         '0000S',
                         '0000.000N',
                         '0000.001S',
                         '0959.99S',
                         '0009N',
                         '0009.0S',
                         '0000S']

        for ang in dmh_lat_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        # HDM latitude
        regex = ANGLE_PATTERNS[AF_HDM_COMP][AT_LAT]

        hdm_lat_valid = ['N9000',
                         'S9000.0000',
                         'N8900',
                         'S8959.999',
                         'S8000.999',
                         'N0900',
                         'S0900',
                         'N0900.0000',
                         'S0959.99',
                         'N0059.99',
                         'S0000',
                         'N0000.000',
                         'S0000.001',
                         'S0959.99',
                         'N0009',
                         'S0009.0',
                         'S0000']

        for ang in hdm_lat_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

    def test_get_dm_coordinate_parts(self):

        # DMH Longitude
        ang = '02334.211W'
        regex = ANGLE_PATTERNS[AF_DMH_COMP][AT_LON]
        self.assertEqual((23, 34.211, 'W'),
                         CoordinatePredetermined.get_dm_coordinate_parts(ang, regex))

        # DMH Latitude
        ang = '2334.56S'
        regex = ANGLE_PATTERNS[AF_DMH_COMP][AT_LAT]
        self.assertEqual((23, 34.56, 'S'),
                         CoordinatePredetermined.get_dm_coordinate_parts(ang, regex))

        # HDM Longitude
        ang = 'E00233.456'
        regex = ANGLE_PATTERNS[AF_HDM_COMP][AT_LON]
        self.assertEqual((2, 33.456, 'E'),
                         CoordinatePredetermined.get_dm_coordinate_parts(ang, regex))

        # HDM Latitude
        ang = 'N0334.56011'
        regex = ANGLE_PATTERNS[AF_HDM_COMP][AT_LAT]
        self.assertEqual((3, 34.56011, 'N'),
                         CoordinatePredetermined.get_dm_coordinate_parts(ang, regex))

    def test_dm_parts_to_dd(self):
        dm_parts = (100, 30.0, 'S')
        self.assertEqual(-100.5, CoordinatePredetermined.dm_parts_to_dd(dm_parts))

        dm_parts = (47, 30.0, 'N')
        self.assertEqual(47.5, CoordinatePredetermined.dm_parts_to_dd(dm_parts))

        dm_parts = (100, 60.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dm_parts_to_dd(dm_parts))

        dm_parts = (180, 60.0, 'S')
        self.assertEqual(None, CoordinatePredetermined.dm_parts_to_dd(dm_parts))

        dm_parts = (180, 0.0, 'E')
        self.assertEqual(180, CoordinatePredetermined.dm_parts_to_dd(dm_parts))

    def test_dm_to_dd(self):

        ang = CoordinatePredetermined(AF_DMH_COMP, AT_LON)
        self.assertEqual(-135.5, ang.dm_to_dd('13530.000W'))

        ang = CoordinatePredetermined(AF_DMH_COMP, AT_LON)
        self.assertEqual(None, ang.dm_to_dd('18001.000W'))

        ang = CoordinatePredetermined(AF_DMH_COMP, AT_LON)
        self.assertEqual(None, ang.dm_to_dd('1800.001E'))

        ang = CoordinatePredetermined(AF_DMH_COMP, AT_LON)
        self.assertEqual(135.5, ang.dm_to_dd('13530.000E'))

        ang = CoordinatePredetermined(AF_DMH_COMP, AT_LAT)
        self.assertEqual(-35.5, ang.dm_to_dd('3530.000S'))

        ang = CoordinatePredetermined(AF_DMH_COMP, AT_LAT)
        self.assertEqual(35.5, ang.dm_to_dd('3530.000N'))

        ang = CoordinatePredetermined(AF_HDM_COMP, AT_LAT)
        self.assertEqual(-35.5, ang.dm_to_dd('S3530.000'))


class CoordinatePredeterminedDHFormatsTest(unittest.TestCase):

    def test_is_given_format(self):
        # DH longitude
        regex = ANGLE_PATTERNS[AF_DH_COMP][AT_LON]

        dh_lon_valid = ['180E',
                        '180.0000W',
                        '179E',
                        '179.5999W',
                        '170.999W',
                        '099.99W',
                        '099E',
                        '009W',
                        '009.0000E',
                        '009.99W',
                        '000.99E',
                        '000W',
                        '000.000E',
                        '000.001W',
                        '000.099W']
        # self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))
        for ang in dh_lon_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        # HD longitude
        regex = ANGLE_PATTERNS[AF_HD_COMP][AT_LON]

        hd_lon_valid = ['E180',
                        'W180.0000',
                        'E179',
                        'W179.999',
                        'W170.999',
                        'W099.99',
                        'E099',
                        'W009',
                        'E009.0000',
                        'W009.99',
                        'E000.99',
                        'W000']

        for ang in hd_lon_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        # DH latitude
        regex = ANGLE_PATTERNS[AF_DH_COMP][AT_LAT]

        dh_lat_valid = ['90N',
                        '90.0000S',
                        '89N',
                        '89.999S',
                        '80.999S',
                        '09N',
                        '09S',
                        '09.0000N',
                        '09.99S',
                        '00.99S',
                        '00S',
                        '00.000N',
                        '00.001S']

        for ang in dh_lat_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

        # HD latitude
        regex = ANGLE_PATTERNS[AF_HD_COMP][AT_LAT]

        hd_lat_valid = ['N90',
                        'S90.0000',
                        'N89',
                        'S89.999',
                        'S80.999',
                        'N09',
                        'S09',
                        'N09.0000',
                        'S09.99',
                        'N00.99',
                        'S00',
                        'N00.000',
                        'S00.001']

        for ang in hd_lat_valid:
            self.assertEqual(True, CoordinatePredetermined.is_given_format(ang, regex))

    def test_get_dh_coordinate_parts(self):

        # DH Longitude
        ang = '023.211W'
        regex = ANGLE_PATTERNS[AF_DH_COMP][AT_LON]
        self.assertEqual((23.211, 'W'),
                         CoordinatePredetermined.get_dh_coordinate_parts(ang, regex))

        # DH Latitude
        ang = '23.56S'
        regex = ANGLE_PATTERNS[AF_DH_COMP][AT_LAT]
        self.assertEqual((23.56, 'S'),
                         CoordinatePredetermined.get_dh_coordinate_parts(ang, regex))

        # HD Longitude
        ang = 'E002.456'
        regex = ANGLE_PATTERNS[AF_HD_COMP][AT_LON]
        self.assertEqual((2.456, 'E'),
                         CoordinatePredetermined.get_dh_coordinate_parts(ang, regex))

        # HD Latitude
        ang = 'N03.56011'
        regex = ANGLE_PATTERNS[AF_HD_COMP][AT_LAT]
        self.assertEqual((3.56011, 'N'),
                         CoordinatePredetermined.get_dh_coordinate_parts(ang, regex))

    def test_dh_parts_to_dd(self):
        dh_parts = (130, 'W')
        self.assertEqual(-130, CoordinatePredetermined.dh_parts_to_dd(dh_parts))

        dh_parts = (47, 'N')
        self.assertEqual(47, CoordinatePredetermined.dh_parts_to_dd(dh_parts))

    def test_dh_to_dd(self):

        ang = CoordinatePredetermined(AF_DH_COMP, AT_LON)
        self.assertEqual(-135.5, ang.dh_to_dd('135.500W'))

        ang = CoordinatePredetermined(AF_DH_COMP, AT_LON)
        self.assertEqual(-180, ang.dh_to_dd('180.00W'))

        ang = CoordinatePredetermined(AF_DH_COMP, AT_LON)
        self.assertEqual(None, ang.dh_to_dd('181E'))

        ang = CoordinatePredetermined(AF_DH_COMP, AT_LAT)
        self.assertEqual(-35.3, ang.dh_to_dd('35.300S'))

        ang = CoordinatePredetermined(AF_HD_COMP, AT_LAT)
        self.assertEqual(-35.999, ang.dh_to_dd('S35.99900'))
