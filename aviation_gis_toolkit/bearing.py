"""
bearing module provides functionality to deal with bearings: conversion, validation
"""
from aviation_gis_toolkit.angle_base import *

# Formatting bearing in degrees, minutes, seconds separated format
BRNG_STRING_FORMAT = '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}'


class Bearing(AngleBase):
    """ Class covers actions related to bearing: validation, conversion, reduction to azimuth.
        Attributes:
    -----------
    src_brng : str or float or int
        Keeps source value of bearing, note that this value can be with comma decimal separator not dot decimal
        separator, example: 109,25 109.25.
    brng_dd: float
        Keeps float value of bearing, DD format of src_brng.
    is_valid: bool
        True if src_brng value is valid bearing, False otherwise
    err_msg: str
        Keeps error message in case src_brng value is not supported bearing format

    """
    def __init__(self, src_brng):
        BasicTools.__init__(self)
        self.src_brng = src_brng
        self.brng_dd = None
        self.is_valid = None
        self.err_msg = ''
        self.bearing_to_dd()

    def get_bearing_dms(self, prec=3):
        """ Converts bearing from decimal degrees format to degrees, minutes, seconds space separated format.
        :param prec: int, positive number of decimal point of seconds
        :return: str: bearing in DMS format.
        """
        return self._dd_to_dms(BRNG_STRING_FORMAT, self.brng_dd, prec)

    def bearing_to_dd(self):
        """ Converts bearing from source value to DD format. """
        norm_brng = self.get_normalized_src_value(self.src_brng)

        if norm_brng:
            # Check if source bearing is in DD format:
            try:
                dd = float(norm_brng)
            except ValueError:
                # Check if source bearing is in DMS or DM formats
                dd = self._angle_to_dd(norm_brng, AT_BRNG_REGEXS)

            # If converted into DD - check if angle is within range for bearing
            if dd is not None:
                if self.is_within_range(dd, 0, 360):
                    self.brng_dd = dd
                    self.is_valid = True
                    self.err_msg = ''
                else:
                    self.is_valid = False
                    self.err_msg = 'Value {} is not supported bearing format'.format(self.src_brng)
        else:
            self.is_valid = False
            self.err_msg = 'Enter bearing.'
