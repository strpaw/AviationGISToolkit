"""
coordinates_gcs module contains common tools to handle coordinate pair: longitude and latitude
"""
from aviation_gis_toolkit.const import *
from aviation_gis_toolkit.angle_base import *

LON_STRING_FORMATS = {
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
}

LAT_STRING_FORMATS = {
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


class CoordinatesGCS(AngleBase):

    def __init__(self, lon_src, lat_src):
        BasicTools.__init__(self)
        self.lon_src = lon_src
        self.lat_src = lat_src
        self.lon_dd = None
        self.lat_dd = None
        self.is_valid = None
        self.err_msg = ''

