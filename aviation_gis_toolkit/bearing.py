"""
bearing module provides functionality to deal with bearings: conversion, validation
"""
from aviation_gis_toolkit.base_tools import BasicTools
import re
import math

# Bearing regular expressions
BRNG_REGEXS = {
    'DMS_SEP': re.compile(r'''^
                              (?P<deg>\d{1,3})  # Degrees
                               \W  # Separator: space, hyphen, degree sign
                               (?P<min>\d{1,2})  # Minutes
                               \W{1,2}  # Separator: space, hyphen, minute sign: '
                               (?P<sec>\d{1,2}|\d{1,2}\.\d+)  # Seconds
                               \W{,2} # Separator: space, hyphen, second sign: or '', or "
                               $
                             ''', re.VERBOSE),
    'DMS_COMP': re.compile(r'''^
                               (?P<deg>\d{3})  # Degrees
                               (?P<min>\d{2})  # Minutes
                               (?P<sec>\d{2}|\d{2}\.\d+)  # Seconds
                               $
                             ''', re.VERBOSE)
}

# Formatting bearing in degrees, minutes, seconds separated format
BRNG_STRING_FORMAT = '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}'


class Bearing(BasicTools):
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

    @staticmethod
    def _dd_to_dms_parts(ang_dd, prec=3):
        """ Converts angle given in DD format into DMS format in 'parts', e. g. DD, MM, SEC
        :param ang_dd: float, angle in DD format
        :param prec: int, positive number of decimal point of seconds, default value is 3
        :return tuple: tuple of dd, mm, sec - float
        """

        d_frac_part, d_whole_part = math.modf(math.fabs(ang_dd))  # frac_part - fractional part
        m_frac_part, m_whole_part = math.modf(d_frac_part * 60)
        s_part = m_frac_part * 60

        def sign(a_dd): return 1 if a_dd >= 0 else -1
        dd = int(d_whole_part)
        mm = int(m_whole_part)
        sec = round(s_part, prec)

        return sign(ang_dd), dd, mm, sec

    @staticmethod
    def bearing_dd_to_dms(brng, prec=3):
        """ Converts bearing from decimal degrees format to degrees, minutes, seconds space separated format.
        :param brng: float, bearing in DD format.
        :param prec: int, positive number of decimal point of seconds
        :return: str: bearing in DMS format.
        """
        sign, d, m, s = Bearing._dd_to_dms_parts(brng, prec)

        sec_length = 2
        if prec > 0:
            sec_length = prec + 3

        dms = BRNG_STRING_FORMAT.format(d=d, m=m, s=s, sec_length=sec_length, sec_prec=prec)
        return dms

    @staticmethod
    def _get_dms_parts(brng):
        """ Gets degrees, minutes, seconds from bearing in DMS format.
        :param brng: str, bearing in DMS format (separated or compacted).
        :return: tuple:
        """
        for brng_regex in BRNG_REGEXS.values():
            mo = brng_regex.match(brng)  # Check if there is matching object for given pattern
            if mo:  # If it is - get parts of bearing in DMS format
                d = int(mo.group('deg'))
                m = int(mo.group('min'))
                s = float(mo.group('sec'))
                return d, m, s

    @staticmethod
    def _dms_parts_to_dd(parts):
        """ Converts dms parts to float value of DMS format
        :param parts: tuple
        :return: float: DMS bearing in DD format
        """
        d, m, s = parts
        if m < 60 and s < 60:
            return d + m / 60 + s / 3600

    @staticmethod
    def _bearing_dms_to_dd(brng):
        """ Converts bearing from DMS format to DD format.
        :param brng: str, normalized source bearing value
        :return: float: bearing in DD format, None if it is wrong source bearing value
        """
        parts = Bearing._get_dms_parts(brng)
        return Bearing._dms_parts_to_dd(parts)

    def bearing_to_dd(self):
        """ Converts bearing from source value to DD format. """
        norm_brng = self.get_normalized_src_value(self.src_brng)
        # Check DMS formats
        dd = self._bearing_dms_to_dd(norm_brng)
        # Check if brng is withing range
        if dd is not None:
            if self.is_within_range(dd, 0, 360):
                self.brng_dd = dd
                self.is_valid = True
                self.err_msg = ''
            else:
                self.is_valid = False
                self.err_msg = 'Value {} is not supported bearing format'.format(self.src_brng)
