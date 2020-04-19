"""
coordinate_predetermined.py
coordinate_predetermined module provides functionality to validate and convert coordinate (latitude, longitude)
from known format in advance, such as degrees, minutes, seconds, hemisphere (DMSH) into decimal degrees (DD)
format.
"""
from .const import *
import re

# --------------- Regular expressions for coordinate formats  --------------- #

# Note: Patterns does not take into account if coordinate is valid or not,
# for example if longitude does not exceed 180 degrees.
TMPL_LON_DMSH_COMP = re.compile('''(?P<deg>^180|^1[0-7]\d|^0\d{2})  # Degrees
                                   (?P<min>[0-5]\d)  # Minutes
                                   (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Seconds
                                   (?P<hem>[EW]$)  # Hemisphere
                                ''', re.VERBOSE)

TMPL_LAT_DMSH_COMP = re.compile('''(?P<deg>^90|^[0-8]\d)  # Degrees
                                   (?P<min>[0-5]\d)  # Minutes
                                   (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Seconds
                                   (?P<hem>[NS]$)  # Hemisphere
                                ''', re.VERBOSE)

TMPL_LON_HDMS_COMP = re.compile('''(?P<hem>^[EW])  # Hemisphere
                                   (?P<deg>180|1[0-7]\d|0\d{2})  # Degrees
                                   (?P<min>[0-5]\d)  # Minutes
                                   (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds             
                                ''', re.VERBOSE)

TMPL_LAT_HDMS_COMP = re.compile('''(?P<hem>^[NS])  # Hemisphere
                                   (?P<deg>90|[0-8]\d)  # Degrees
                                   (?P<min>[0-5]\d)  # Minutes
                                   (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds
                                ''', re.VERBOSE)

TMPL_LON_DMH_COMP = re.compile('''(?P<deg>^180|^1[0-7]\d|^0\d{2})  # Degrees
                                  (?P<min>[0-5]\d\.\d+|[0-5]\d)  # Minutes
                                  (?P<hem>[EW]$)  # Hemisphere
                                ''', re.VERBOSE)

TMPL_LAT_DMH_COMP = re.compile('''(?P<deg>^90|^[0-8]\d)  # Degrees
                                  (?P<min>[0-5]\d\.\d+|[0-5]\d)  # Minutes
                                  (?P<hem>[NS]$)  # Hemisphere
                                ''', re.VERBOSE)

TMPL_LON_HDM_COMP = re.compile('''(?P<hem>^[EW])  # Hemisphere
                                   (?P<deg>180|1[0-7]\d|0\d{2})  # Degrees
                                   (?P<min>[0-5]\d\.\d+$|[0-5]\d$)  # Minutes       
                                ''', re.VERBOSE)

TMPL_LAT_HDM_COMP = re.compile('''(?P<hem>^[NS])  # Hemisphere
                                  (?P<deg>90|[0-8]\d)  # Degrees
                                  (?P<min>[0-5]\d\.\d+$|[0-5]\d$)  # Minutes 
                                ''', re.VERBOSE)

TMPL_LON_DH_COMP = re.compile('''(?P<deg>^180\.0+|^180|^[0-1][0-7]\d\.\d+|^[0-1][0-7]\d|^0\d{2}\.\d+|^0\d{2})  # Degrees  
                                 (?P<hem>[EW]$)  # Hemisphere 
                              ''', re.VERBOSE)

TMPL_LAT_DH_COMP = re.compile('''(?P<deg>^90\.0+|^90|[0-8]\d\.\d+|^[0-8]\d)  # Degrees   
                                 (?P<hem>[NS]$)  # Hemisphere
                                ''', re.VERBOSE)

TMPL_LON_HD_COMP = re.compile('''(?P<hem>^[EW])  # Hemisphere
                                 (?P<deg>180\.0+|180|[0-1][0-7]\d\.\d+|[0-1][0-7]\d|0\d{2}\.\d+|0\d{2})  # Degrees   
                              ''', re.VERBOSE)

TMPL_LAT_HD_COMP = re.compile('''(?P<hem>^[NS])  # Hemisphere
                                 (?P<deg>90\.0+$|90$|[0-8]\d\.\d+$|[0-8]\d$)  # Degrees   
                                ''', re.VERBOSE)

ANGLE_PATTERNS = {AF_DMSH_COMP: {AT_LON: TMPL_LON_DMSH_COMP,
                                 AT_LAT: TMPL_LAT_DMSH_COMP},
                  AF_HDMS_COMP: {AT_LON: TMPL_LON_HDMS_COMP,
                                 AT_LAT: TMPL_LAT_HDMS_COMP},
                  AF_DMH_COMP: {AT_LON: TMPL_LON_DMH_COMP,
                                AT_LAT: TMPL_LAT_DMH_COMP},
                  AF_HDM_COMP: {AT_LON: TMPL_LON_HDM_COMP,
                                AT_LAT: TMPL_LAT_HDM_COMP},
                  AF_DH_COMP: {AT_LON: TMPL_LON_DH_COMP,
                               AT_LAT: TMPL_LAT_DH_COMP},
                  AF_HD_COMP: {AT_LON: TMPL_LON_HD_COMP,
                               AT_LAT: TMPL_LAT_HD_COMP}}


class CoordinatePredetermined:
    """ Class to check if angle (longitude, latitude) is in predetermined (known in advance) format and
    to convert it from human friendly format (such as degrees, minutes and seconds) into decimal degrees format.
    Supported formats:
    DMSH compacted: Degrees, minutes, seconds, hemisphere indicator not separated.
    HDMS compacted: Hemisphere indicator, degrees, minutes, seconds, hemisphere indicator not separated.
    DMH compacted: Degrees, minutes hemisphere indicator not separated.
    HDM compacted: Hemisphere indicator, degrees, minutes  not separated.
    DH compacted: Degrees, hemisphere indicator not separated
    HD compacted: Hemisphere indicator, degrees not separated

    Attributes:
    -----------
    ang_format : str
        Constants, angle format, e. g. AF_DMSH_COMP.
    ang_type: str
        Constant, angle type, e. g. AT_LON.
    regex: regular expression object
        regular expression object for given angle format and angle type. """

    DMS_FORMATS = [AF_DMSH_COMP, AF_HDMS_COMP]
    DM_FORMATS = [AF_DMH_COMP, AF_HDM_COMP]
    DH_FORMATS = [AF_DH_COMP, AF_HD_COMP]

    def __init__(self, ang_format=None, ang_type=None):
        self.ang_format = ang_format
        self.ang_type = ang_type
        self.regex = None
        self.set_regex()

    def set_regex(self):
        """ Sets regular expression pattern for given angle type and angle format. """
        self.regex = ANGLE_PATTERNS[self.ang_format][self.ang_type]

    @staticmethod
    def is_given_format(ang, regex):
        """ Checks if angle is in given format.
        :param ang: str, angle to check
        :param regex: regular expression object
        :return: bool: True if angle matches regular expression regex
        """
        return bool(regex.match(ang))

    # --------------- DMSH, HDMS formats  --------------- #

    @staticmethod
    def get_dms_coordinate_parts(ang, regex):
        """ Converts angle string to DMS parts: degrees, minutes, seconds.
        :param ang: str, angle
        :param regex: regex
        :return: tuple: tuple of parts:
                        d - degrees, int,
                        m - minutes, int,
                        s - seconds, float,
                        h - hemisphere indicator, str
                        If not able to extract DMS parts returns None. """

        dmsh_parts = regex.search(ang)
        d = int(dmsh_parts.group('deg'))
        m = int(dmsh_parts.group('min'))
        s = float(dmsh_parts.group('sec'))
        h = dmsh_parts.group('hem')
        return d, m, s, h

    @staticmethod
    def dms_parts_to_dd(dms_parts):
        """ Converts coordinates parts into degrees minutes format.
        :param dms_parts: tuple of degrees (int), minutes (int), seconds (float) and hemisphere character (str)
        :return: dd: float
        """
        d, m, s, h = dms_parts
        if (d == 180 or d == 90) and (m > 0 or s > 0):
            return
        elif m >= 60 or s >= 60:
            return
        else:
            dd = d + m / 60 + s / 3600
            if h in ['W', 'S']:
                return -dd
            else:
                return dd

    def dms_to_dd(self, ang):
        """ Converts DMS coordinate to DD format.
        :param ang: str, angle to convert
        """
        if self.is_given_format(ang, self.regex):
            dms_parts = self.get_dms_coordinate_parts(ang, self.regex)
            dd = self.dms_parts_to_dd(dms_parts)
            return dd

    # --------------- DMH, HDM formats  --------------- #
    @staticmethod
    def get_dm_coordinate_parts(ang, regex):
        """ Converts angle string to DM parts: degrees, minutes.
        :param ang: str, angle
        :param regex: regex
        :return: tuple: tuple of parts:
                        d - degrees, int
                        m - minutes, float,
                        h - hemisphere indicator, str
                        If not able to extract DMS parts returns None. """

        dmh_parts = regex.search(ang)
        d = int(dmh_parts.group('deg'))
        m = float(dmh_parts.group('min'))
        h = dmh_parts.group('hem')
        return d, m, h

    @staticmethod
    def dm_parts_to_dd(dm_parts):
        """ Converts coordinates parts into degrees minutes format.
        :param dm_parts: tuple of degrees (int), minutes (float) and hemisphere character (str)
        :return: dd: float
        """
        d, m, h = dm_parts
        if (d == 180 or d == 90) and m > 0:
            return
        elif m >= 60:
            return
        else:
            dd = d + m / 60
            if h in ['W', 'S']:
                return -dd
            else:
                return dd

    def dm_to_dd(self, ang):
        """ Converts DM coordinate to DD format.
        :param ang: str, angle to convert
        :return: dd: float
        """
        if self.is_given_format(ang, self.regex):
            dm_parts = self.get_dm_coordinate_parts(ang, self.regex)
            dd = self.dm_parts_to_dd(dm_parts)
            return dd

    # --------------- DH, HD formats  --------------- #

    @staticmethod
    def get_dh_coordinate_parts(ang, regex):
        """ Converts angle string to DH parts: degrees, hemisphere.
        :param ang: str, angle
        :param regex: regex
        :return: tuple: tuple of parts:
                        d - degrees, float
                        h - hemisphere indicator, str
                        If not able to extract DMS parts returns None. """

        dh_parts = regex.search(ang)
        d = float(dh_parts.group('deg'))
        h = dh_parts.group('hem')
        return d, h

    @staticmethod
    def dh_parts_to_dd(dh_parts):
        """ Converts coordinates parts into degrees minutes format.
        :param dh_parts: tuple of degrees (int), minutes (float) and hemisphere character (str)
        :return: dd: float
        """
        d, h = dh_parts
        if h in ['W', 'S']:
            return -d
        else:
            return d

    def dh_to_dd(self, ang):
        """ Converts DM coordinate to DD format
        :param ang: str, angle to convert
        :return: dd: float
        """
        if self.is_given_format(ang, self.regex):
            dh_parts = self.get_dh_coordinate_parts(ang, self.regex)
            dd = self.dh_parts_to_dd(dh_parts)
            return dd

    # --------------- Coordinate to DD  --------------- #

    def coordinate_to_dd(self, ang):
        """ Converts coordinate in supported format to decimal degrees format.
        :param ang: str, angle to convert
        :return: float: coordinate in decimal degrees
        """
        if self.ang_format in CoordinatePredetermined.DMS_FORMATS:
            return self.dms_to_dd(ang)
        elif self.ang_format in CoordinatePredetermined.DM_FORMATS:
            return self.dm_to_dd(ang)
        elif self.ang_format in CoordinatePredetermined.DH_FORMATS:
            return self.dh_to_dd(ang)
