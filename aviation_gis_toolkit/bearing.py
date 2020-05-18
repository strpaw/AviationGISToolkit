"""
bearing.py
bearing module provides functionality to deal with bearings: conversion, validation
"""
import re

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

