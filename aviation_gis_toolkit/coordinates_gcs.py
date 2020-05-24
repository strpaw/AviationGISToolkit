"""
coordinates_gcs module contains common tools to handle coordinate pair: longitude and latitude
"""

from aviation_gis_toolkit.angle_base import *


class CoordinatesGCS(AngleBase):

    def __init__(self, lon_src, lat_src):
        BasicTools.__init__(self)
        self.lon_src = lon_src
        self.lat_src = lat_src
        self.lon_dd = None
        self.lat_dd = None
        self.is_valid = None
        self.err_msg = ''

