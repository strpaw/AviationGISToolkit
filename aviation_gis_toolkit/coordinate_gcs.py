"""
coordinate_gcs module contains common tools to handle coordinate: longitude and latitude
"""
from aviation_gis_toolkit.const import *
from aviation_gis_toolkit.angle_base import *

COORD_GCS_STRING_FORMATS = {
    AT_LON: {
        AF_HDMS_ALL_SEP: '{hem} {d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_SEP: '{hem}{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_DMSH_ALL_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f} {hem}',
        AF_DMSH_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
        AF_HDMS_COMP: '{hem}{d:03d}{m:02d}{s:0{sec_length}.{sec_prec}f}',
        AF_DMSH_COMP: '{d:02d}{m:02d}{s:0{sec_length}.{sec_prec}f}{hem}',
        AF_DMSH_SEP_SYMBOLS: '{d:03d}\xb0{m:02d}\''
                             '{s:0{sec_length}.{sec_prec}f}\'\' {hem}',
        AF_HDMS_SEP_SYMBOLS: '{hem} {d:03d}\xb0{m:02d}\''
                             '{s:0{sec_length}.{sec_prec}f}\'\''
    },
    AT_LAT: {
        AF_HDMS_ALL_SEP: '{hem} {d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_SEP: '{hem}{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_DMSH_ALL_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f} {hem}',
        AF_DMSH_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
        AF_HDMS_COMP: '{hem}{d:02d}{m:02d}{s:0{sec_length}.{sec_prec}f}',
        AF_DMSH_COMP: '{d:02d}{m:02d}{s:0{sec_length}.{sec_prec}f}{hem}',
        AF_DMSH_SEP_SYMBOLS: '{d:02d}\xb0{m:02d}\''
                             '{s:0{sec_length}.{sec_prec}f}\'\' {hem}',
        AF_HDMS_SEP_SYMBOLS: '{hem} {d:02d}\xb0{m:02d}\''
                             '{s:0{sec_length}.{sec_prec}f}\'\''
    }
}


class CoordinateGCS(AngleBase):

    def __init__(self, ang_src, ang_type):
        BasicTools.__init__(self)
        self.ang_src = ang_src
        self.ang_type = ang_type
        self.ang_dd = None
        self.is_valid = None
        self.err_msg = ''

    @staticmethod
    def get_hemisphere_character(sign, ang_type):
        """ Returns hemisphere character e.g. S, N
        :param sign: str, character '-', '+'
        :param ang_type: str, angle type
        :return: str: hemisphere character: N, E, S or W
        """
        if ang_type == AT_LAT:
            if sign == -1:
                return 'S'
            elif sign == 1:
                return 'N'
        elif ang_type == AT_LON:
            if sign == -1:
                return 'W'
            elif sign == 1:
                return 'E'

    def get_angle_dms(self, ang_str_format, prec=3):
        """ Converts angle from decimal degrees format to degrees, minutes, seconds space separated format.
        :param: ang_str_format: str
        :param prec: int, positive number of decimal point of seconds
        :return: str: bearing in DMS format.
        """

        def sign(a_dd): return 1 if a_dd >= 0 else -1
        hem = CoordinateGCS.get_hemisphere_character(sign(self.ang_dd), self.ang_type)
        return self._dd_to_dms(COORD_GCS_STRING_FORMATS[self.ang_type][ang_str_format], self.ang_dd, prec, hem)
