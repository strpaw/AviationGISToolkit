import math
from .const import *
from .base_tools import BasicTools


# ANGLE DMS string formats
ANG_STRING_FORMATS = {AT_LAT: {AF_HDMS_ALL_SEP: '{hem} {d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
                               AF_HDMS_SEP: '{hem}{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
                               AF_DMSH_ALL_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f} {hem}',
                               AF_DMSH_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
                               AF_HDMS_COMP: '{hem}{d:02d}{m:02d}{s:0{sec_length}.{sec_prec}f}',
                               AF_DMSH_COMP: '{d:02d}{m:02d}{s:0{sec_length}.{sec_prec}f}{hem}',
                               AF_DMSH_SEP_SYMBOLS: '{d:02d}\xb0{m:02d}\''
                                                    '{s:0{sec_length}.{sec_prec}f}\'\' {hem}',
                               AF_HDMS_SEP_SYMBOLS: '{hem} {d:02d}\xb0{m:02d}\''
                                                    '{s:0{sec_length}.{sec_prec}f}\'\''},
                      AT_LON: {AF_HDMS_ALL_SEP: '{hem} {d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
                               AF_HDMS_SEP: '{hem}{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
                               AF_DMSH_ALL_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f} {hem}',
                               AF_DMSH_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
                               AF_HDMS_COMP: '{hem}{d:03d}{m:02d}{s:0{sec_length}.{sec_prec}f}',
                               AF_DMSH_COMP: '{d:02d}{m:02d}{s:0{sec_length}.{sec_prec}f}{hem}',
                               AF_DMSH_SEP_SYMBOLS: '{d:03d}\xb0{m:02d}\''
                                                    '{s:0{sec_length}.{sec_prec}f}\'\' {hem}',
                               AF_HDMS_SEP_SYMBOLS: '{hem} {d:03d}\xb0{m:02d}\''
                                                    '{s:0{sec_length}.{sec_prec}f}\'\''}}


class Angle(BasicTools):
    """ Class used to conversion angle between various formats.
    Also to check if given value is correct angle """

    HEM_CHARS = ['N', 'S', 'E', 'W']
    HEM_CHAR_LAT = ['N', 'S']
    HEM_CHAR_LON = ['E', 'W']
    HEM_CHAR_POSITIVE = ['N', 'E']
    HEM_CHAR_NEGATIVE = ['S', 'W']

    def __init__(self, ang_src=None, ang_type=None):
        BasicTools.__init__(self)
        self.ang_src = ang_src
        self.ang_type = ang_type
        self.ang_dd = None

    # General methods common to all types of angle

    @staticmethod
    def is_angle_within_range(ang_dd, ang_type):
        """  Checks if angle is within range for specified angle type.
        :param ang_dd: float, angle to check
        :param ang_type: const(str): type of angle
        :return:
        """
        if ang_type == AT_LAT:
            return bool(-90 <= ang_dd <= 90)
        elif ang_type == AT_LON:
            return bool(-180 <= ang_dd <= 180)

    # Conversion from decimal degrees format to degrees, minutes, seconds format

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

    @staticmethod
    def dd_to_dms_parts(ang_dd, prec=3):
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
    def dd_to_dms_string(ang_dd, ang_type, ang_format=AF_DMSH_ALL_SEP, prec=3):
        """ Converts angle in DD format into more human readable DMS format
        :param ang_dd: float, angle in DD
        :param ang_type: str, angle type
        :param ang_format: str, desired format of angle in DMS format
        :param prec:  int, positive number of decimal point of seconds, default value is 3
        :return: ang_dms: str, input angle in DMS format
        """
        if Angle.is_angle_within_range(ang_dd, ang_type):
            sign, d, m, s = Angle.dd_to_dms_parts(ang_dd, prec)
            hem = Angle.get_hemisphere_character(sign, ang_type)

            if prec > 0:
                sec_length = prec + 3
            elif prec == 0:
                sec_length = 2
            else:
                return None

            formatted_dms_string = ANG_STRING_FORMATS[ang_type][ang_format]
            return formatted_dms_string.format(d=d, m=m, s=s,
                                               sec_length=sec_length,
                                               sec_prec=prec,
                                               hem=hem)

    # Conversion from DMS to DD format

    @staticmethod
    def get_hemisphere_prefix_from_angle(ang):
        """ Checks is first character in ang string is a hemisphere suffix character.
        :param ang: str, angle string
        :return: str: hemisphere character, if not found returns None
        """
        if len(ang) > 2:
            for hem in Angle.HEM_CHARS:
                if ang.find(hem) == 0:
                    return hem

    @staticmethod
    def get_hemisphere_suffix_from_angle(ang):
        """ Checks is last character in ang string is a hemisphere suffix character.
        :param ang: str, angle string
        :return: str: hemisphere character, if not found returns None
        """
        if len(ang) > 2:
            for hem in Angle.HEM_CHARS:
                if ang.find(hem) == len(ang) - 1:
                    return hem

    @staticmethod
    def get_dms_parts(ang, sep=' '):
        """ Converts angle string to DMS parts: degrees, minutes, seconds
        :param ang: str, angle in DMS format without hemisphere designator or sign (positive or negative)
        :param sep: str, separator indicator
        :return: tuple: tuple of parts:
                        degree - int
                        minutes - int,
                        seconds - float If not able to extract DMS parts returns None.
        """
        if type(ang) == str and sep == ' ':
            dms_parts = ang.split(sep)

            if len(dms_parts) == 3:
                d = Angle.get_value_as_int_number(dms_parts[0])
                m = Angle.get_value_as_int_number(dms_parts[1])
                s = Angle.get_value_as_float_number(dms_parts[2])

                if d is not None and m is not None and s is not None:
                    return d, m, s

    @staticmethod
    def dms_separated_no_hemisphere_to_dd(ang, ang_type, sep=' '):
        """ Converts angle in DMS format separated into DD format.
        :param ang: str, angle in DMS format without hemisphere designator or sign (positive or negative)
        :param ang_type: const(str): type of angle
        :param sep: str, separator indicator
        :return: float: ang in DD format, None if ang is not valid for specified angle type
        """
        t_dms_parts = Angle.get_dms_parts(ang, sep)
        if t_dms_parts is not None:  # Result is tuple of deg, min, sec
            d, m, s = t_dms_parts
            # Checks if d is within range for specified angle type
            if Angle.is_angle_within_range(d, ang_type):
                if Angle.is_within_range(m, 0, 59) and (0 <= s < 60):
                        dd = math.fabs(d) + m / 60 + s / 3600
                        if Angle.is_angle_within_range(dd, ang_type):
                            if d < 0:
                                return -dd
                            else:
                                return dd

    @staticmethod
    def dms_compacted_no_hemisphere_to_dd(ang, ang_type):
        """

        :param ang:
        :param ang_type:
        :return:
        """
        ang_parts = ang.split('.')
        if len(ang_parts[0]) >= 6:  # Minimum length of string for latitude DDMMSS
            # Check if first character is minus or plus and trim if is
            if ang[0] in '-+':
                ang_mod = ang[1:]
            else:
                ang_mod = ang

            try:
                if ang_type == AT_LAT:
                    d = Angle.get_value_as_int_number(ang_mod[0:2])
                    m = Angle.get_value_as_int_number(ang_mod[2:4])
                    s = Angle.get_value_as_float_number(ang_mod[4:])
                elif ang_type == AT_LON:
                    d = Angle.get_value_as_int_number(ang_mod[0:3])
                    m = Angle.get_value_as_int_number(ang_mod[3:5])
                    s = Angle.get_value_as_float_number(ang_mod[5:])
            except IndexError:
                return None
            else:
                if d is not None and m is not None and s is not None:
                    if Angle.is_angle_within_range(d, ang_type):
                        if Angle.is_within_range(m, 0, 59) and (0 <= s < 60):
                            dd = d + m / 60 + s / 3600
                            if Angle.is_angle_within_range(dd, ang_type):
                                if ang[0] == '-':
                                    return -dd
                                else:
                                    return dd

    @staticmethod
    def angle_no_hemisphere_to_dd(ang, ang_type, sep=' '):
        """ Converts angle to DD format from format: DMS separated or compacted. Also checks if
        ang is in DD format.
        :param ang: str, angle in format DD, DMS, HDMS, DMSH
        :param ang_type: str, angle type
        :param sep: str, separator between degrees, minutes and seconds parts
        :return: dd: float, decimal degrees
        """
        ang_norm = Angle.get_normalized_src_value(ang)

        # Check if angle is in DD format
        dd = Angle.get_value_as_float_number(ang_norm)
        if dd is not None:
            if Angle.is_angle_within_range(dd, ang_type):
                return dd
            else:
                # Got number, but it can be actually angle in DMS compacted format
                # Check if angle is ind DMS compacted format without suffix or prefix
                return Angle.dms_compacted_no_hemisphere_to_dd(ang_norm, ang_type)
        else:
            # Check if angle is in DMS format, without hemisphere suffix or prefix
            return Angle.dms_separated_no_hemisphere_to_dd(ang_norm, ang_type, sep)

    def get_angle_dd(self):
        """ Converts source value of angle into decimal degrees format.
        If conversion fails - angle is considered as not valid and appropriate error message is assign to err_msg
        attribute """
        self.ang_dd = self.angle_no_hemisphere_to_dd(self.ang_src, self.ang_type)
        if self.ang_dd is None:
            self.is_valid = False
            self.err_msg = 'Value: {} is not correct or supported angle type: {}'.format(self.ang_src, self.ang_type)
        else:
            self.is_valid = True
            self.err_msg = ''
