"""
bearing.py
bearing module provides functionality to deal with bearings: conversion, validation
"""
import re
import math

# Bearing regular expressions
BRNG_REGEX = {
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


class Bearing:
    """ Class covers actions related to bearing: validation, conversion, reduction to azimuth."""

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
