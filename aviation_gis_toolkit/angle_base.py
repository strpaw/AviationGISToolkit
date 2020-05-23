"""
angle_base module contains common tools to handle angle.
"""
from aviation_gis_toolkit.base_tools import BasicTools
import re
import math

AT_LON_REGEXS = {
    'DMS_COMP': re.compile(r'''
                ^  # Start of the string
                (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                (?P<deg>\d{3})  # Degrees
                (?P<min>\d{2})  # Minutes
                (?P<sec>\d{2}(\.\d+)?)  # Seconds
                (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                $  # End of the string
               ''', re.VERBOSE),
    'DMS_SEP': re.compile(r'''
                ^  # Start of the string
                (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                (\s)?
                (?P<deg>\d{1,3})  # Degrees
                (\W)
                (?P<min>\d{1,2})  # Minutes
                (\W)
                (?P<sec>\d{1,2}(\.\d+)?)  # Seconds
                (\W){,2}
                (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                $  # End of the string
                ''', re.VERBOSE),
    'DM_COMP': re.compile(r'''
                ^  # Start of the string
                (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                (?P<deg>\d{3})  # Degrees
                (?P<min>\d{2}(\.\d+)?)  # Minutes
                (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                $  # End of the string
               ''', re.VERBOSE)
}
AT_LAT_REGEXS = {
    'DMS_COMP': re.compile(r'''
            ^  # Start of the string
            (?P<hem_prefix>[-+NS]?)  # Hemisphere prefix
            (?P<deg>\d{2})  # Degrees
            (?P<min>\d{2})  # Minutes
            (?P<sec>\d{2}(\.\d+)?)  # Seconds
            (?P<hem_suffix>[NS]?)  # Hemisphere suffix
            $  # End of the string
           ''', re.VERBOSE),
    'DMS_SEP': re.compile(r'''
            ^  # Start of the string
            (?P<hem_prefix>[-+NS]?)  # Hemisphere prefix
            (\s)?
            (?P<deg>\d{1,2})  # Degrees
            (\W)
            (?P<min>\d{1,2})  # Minutes
            (\W)
            (?P<sec>\d{1,2}(\.\d+)?)  # Seconds
            (\W){,2}
            (?P<hem_suffix>[NS]?)  # Hemisphere suffix
            $  # End of the string
            ''', re.VERBOSE),
    'DM_COMP': re.compile(r'''
            ^  # Start of the string
            (?P<hem_prefix>[-+NS]?)  # Hemisphere prefix
            (?P<deg>\d{2})  # Degrees
            (?P<min>\d{2}(\.\d+)?)  # Minutes
            (?P<hem_suffix>[NS]?)  # Hemisphere suffix
            $  # End of the string
           ''', re.VERBOSE)
}

AT_BRNG_REGEXS = {
    'DMS_SEP': re.compile(r'''^
                              (?P<deg>\d{1,3})  # Degrees
                               \W  # Separator: space, hyphen, degree sign
                               (?P<min>\d{1,2})  # Minutes
                               \W  # Separator: space, hyphen, minute sign: '
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


class AngleBase(BasicTools):

    DIRECTION_NEGATIVE = ['-', 'S', 'W']

    def __init__(self, ang_src=None, ang_type=None):
        BasicTools.__init__(self)
        self.ang_src = ang_src
        self.ang_type = ang_type
        self.ang_dd = None

    # -------------- Conversion DD to DMS format -------------- #

    @staticmethod
    def _dd_to_dms_parts(ang_dd, prec=3):
        """ Converts angle given in DD format into DMS 'parts': degrees, minutes, seconds.
        :param ang_dd: float, angle in DD format.
        :param prec: int, positive number of decimal point of seconds, default value is 3.
        :return tuple: tuple of d, m, s (int, int, float).
        """

        d_frac_part, d_whole_part = math.modf(math.fabs(ang_dd))  # frac_part - fractional part
        m_frac_part, m_whole_part = math.modf(d_frac_part * 60)
        s_part = m_frac_part * 60

        def sign(a_dd): return 1 if a_dd >= 0 else -1
        d = int(d_whole_part)
        m = int(m_whole_part)
        s = round(s_part, prec)

        if s == 60:
            m += 1
            s = 0
        if m == 60:
            d += 1
            m = 0

        return sign(ang_dd), d, m, s

    @staticmethod
    def _dd_to_dms(format_template, ang, prec=3):
        """ Converts angle from decimal degrees format into degrees, minutes, seconds space separated format.
        :param format_template: str, DMS format template
        :param ang: float, bearing in DD format.
        :param prec: int, positive number of decimal point of seconds
        :return: str: bearing in DMS format.
        """
        sign, d, m, s = AngleBase._dd_to_dms_parts(ang, prec)

        sec_length = 2
        if prec > 0:
            sec_length = prec + 3

        dms = format_template.format(d=d, m=m, s=s, sec_length=sec_length, sec_prec=prec)
        return dms

    # -------------- Conversion DMS, DM formats into DD format -------------- #

    @staticmethod
    def _dms_parts_to_dd(parts):
        """ Computes decimal degrees of DMS (degrees, minutes, seconds) parts.
        :param parts: tuple (d, m, s):
        :return: float
        """
        d = int(parts.group('deg'))
        m = float(parts.group('min'))
        s = float(parts.group('sec'))

        if m <= 60 and s <= 60:
            return d + m / 60 + s / 3600

    @staticmethod
    def _dm_parts_to_dd(parts):
        """ Computes decimal degrees of DM (degrees, minutes) parts.
        :param parts: tuple (d, m):
        :return: float
        """
        d = int(parts.group('deg'))
        m = float(parts.group('min'))
        if m <= 60:
            return d + m / 60

    @staticmethod
    def _angle_to_dd(ang, ang_regexs):
        """ Converts angle from DMS, DM format into DD format.
        Note: Correct value of hemisphere will be checked in child class Coordinate and MagneticVariation.
        :param ang: str.
        :param ang_regexs: dict, dictionary with regular expressions of angle patterns.
        :return: float
        """
        for ang_regex in ang_regexs:
            if ang_regexs[ang_regex].match(ang):
                ang_parts = ang_regexs[ang_regex].search(ang)
                if ang_regex in ['DMS_COMP', 'DMS_SEP']:
                    return AngleBase._dms_parts_to_dd(ang_parts)
                elif ang_regex in ['DM_COMP', 'DM_SEP']:
                    return AngleBase._dm_parts_to_dd(ang_parts)
