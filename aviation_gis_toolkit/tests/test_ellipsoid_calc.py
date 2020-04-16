import unittest
from aviation_gis_toolkit.ellipsoid_calc import *


class AngleTests(unittest.TestCase):

    def test_vincenty_direct_solution(self):

        lon_initial = 0.0
        lat_initial = 0.0
        azimuth_initial = 0.0
        distance = 10000.0
        ellipsoid_name = 'WGS84'
        self.assertEqual((0.0, 0.09043694695356691),
                         vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name))

        lon_initial = 0.0
        lat_initial = 0.0
        azimuth_initial = 90.0
        distance = 10000.0
        ellipsoid_name = 'WGS84'
        self.assertEqual((0.08983152841248263, 5.5376636427532604e-18),
                         vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name))

        lon_initial = 0.0
        lat_initial = 0.0
        azimuth_initial = 180.0
        distance = 1000.0
        ellipsoid_name = 'WGS84'
        self.assertEqual((0.0, -0.009043694727216058),
                         vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name))

        lon_initial = 0.0
        lat_initial = 0.0
        azimuth_initial = 270.0
        distance = 10000
        ellipsoid_name = 'WGS84'
        self.assertEqual((-0.08983152841248263, -1.661299092825978e-17),
                         vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name))

        lon_initial = 0.0
        lat_initial = 0.0
        azimuth_initial = 360.0
        distance = 100000.0
        ellipsoid_name = 'WGS84'
        self.assertEqual((0.0, 0.9043687229398173),
                         vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name))

        lon_initial = 137.5
        lat_initial = -32.5
        azimuth_initial = 127.5
        distance = 243855.411
        ellipsoid_name = 'WGS84'
        self.assertEqual((139.58969185673908, -33.8212028224309),
                         vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name))
