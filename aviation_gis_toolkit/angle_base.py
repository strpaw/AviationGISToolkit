"""
angle_base module contains common tools to handle angle.
"""
from aviation_gis_toolkit.base_tools import BasicTools
from aviation_gis_toolkit.const import *
import re
import math


ANGLE_PATTERNS = {
    AT_LON: {
        'DMS_COMP': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                        (?P<deg>\d{3})  # Degrees
                        (?P<min>\d{2})  # Minutes
                        (?P<sec>\d{2}(\.\d+)?)  # Seconds
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
                       ''', re.VERBOSE),
        'DMS_SEP_SPACE': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                        (\s)?
                        (?P<deg>\d{3})  # Degrees
                        (\s)
                        (?P<min>\d{2})  # Minutes
                        (\s)
                        (?P<sec>\d{2}(\.\d+)?)  # Seconds
                        (\s)?
                        (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                        $  # End of the string
                       ''', re.VERBOSE),
        'DMS_SEP_HYPHEN': re.compile(r'''
                ^  # Start of the string
                (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                (\s)?
                (?P<deg>\d{3})  # Degrees
                (-)
                (?P<min>\d{2})  # Minutes
                (-)
                (?P<sec>\d{2}(\.\d+)?)  # Seconds
                (\s)?
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
                (\W)?
                (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                $  # End of the string
               ''', re.VERBOSE),
    },
    AT_LAT: {
        'DMS_COMP': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+NS]?)  # Hemisphere prefix
                        (?P<deg>\d{2})  # Degrees
                        (?P<min>\d{2})  # Minutes
                        (?P<sec>\d{2}(\.\d+)?)  # Seconds
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

    @staticmethod
    def dms_groups_to_dd(parts):
        if parts.group('hem_prefix') and parts.group('hem_suffix'):
            return
        else:
            d = int(parts.group('deg'))
            m = int(parts.group('min'))
            s = float(parts.group('sec'))
            h = parts.group('hem_prefix') + parts.group('hem_suffix')
            dd = d + m / 60 + s / 3600
            if h in AngleBase.DIRECTION_NEGATIVE:
                dd = -dd
            return dd

    @staticmethod
    def dm_groups_to_dd(parts):
        if parts.group('hem_prefix') and parts.group('hem_suffix'):
            return
        else:
            d = int(parts.group('deg'))
            m = float(parts.group('min'))
            h = parts.group('hem_prefix') + parts.group('hem_suffix')
            dd = d + m / 60
            if h in AngleBase.DIRECTION_NEGATIVE:
                dd = -dd
            return dd

    def compacted_format_to_dd(self, ang):
        ang_type_patterns = ANGLE_PATTERNS[self.ang_type]
        for pattern in ang_type_patterns:
            if ang_type_patterns[pattern].match(ang):
                print(pattern)
                parts = ang_type_patterns[pattern].search(ang)
                if pattern in ['DMS_COMP', 'DMS_SEP_SPACE', 'DMS_SEP_HYPHEN', 'DMS_SEP']:
                    return self.dms_groups_to_dd(parts)
                elif pattern == 'DM_COMP':
                    return self.dm_groups_to_dd(parts)

    def angle_to_dd(self, ang):
        ang_norm = AngleBase.get_normalized_src_value(ang)
        dd = self.compacted_format_to_dd(ang)
        return dd




lons = [
    'W125 44 32',
    '125 44 32.111 E',
    'W 125 44 31.56',
    '125 44 1 E',
    '125 44 1',
    'W125 44 1 E'
]

LON_TEST = re.compile(r'''^  # Starts of the longitude
                        (?P<hem_prefix>[EW]?)  # Hemisphere prefix
                        \s?
                        (?P<deg>\d{1,3})  # Degrees
                        \W  # Degree sign
                        (?P<min>\d{1,2})  # Minutes
                        \W{1,2}  # Minute sign        
                        #(?P<sec>\d{1,2}(\.\d+)?)  # Seconds   
                        (?P<sec>\d{1,2}|\d{1,2}\.\d+)  # Seconds   
                        \W{,2}?  # Second sign    
                        \s?  
                        (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                        $  # End of the longitude
                        ''', re.VERBOSE)


for lon in lons:
    mo = LON_TEST.match(lon)
    if mo:
        print(lon, ' ', mo.groups())