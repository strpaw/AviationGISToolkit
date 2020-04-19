"""
coordinate_extraction.py module provides functionality to extracts coordinates from plain text.
"""
# -*- coding: utf-8 -*-
import re
from collections import namedtuple
from aviation_gis_toolkit.const import *

# Longitude, latitude order
LL_ORDER_LATLON = 'LL_ORDER_LATLON'
LL_ORDER_LONLAT = 'LL_ORDER_LONLAT'

# Coordinate format constants
DMSH_SEP = 'DMSH_SEP'
HDMS_SEP = 'HDMS_SEP'

# Longitude, latitude separators separates latitude and longitude in pair, not pairs!
LL_SEP_NONE = r''  # Longitude and latitude not separated
LL_SEP_SPACE = r' '
LL_SEP_HYPHEN = r'-'
LL_SEP_SLASH = r'/'
LL_SEP_BACKSLASH = '\\'
LL_SEP_USER = ''  # User defined separator

_coord_pair = namedtuple('coord_pair', 'lon lat')

# Used in building example of coordinate pair to extract from plain text
lat_h = ['74', '56', '32.55', 'N']
lon_h = ['013', '37', '38.21', 'E']
h_lat = ['N', '74', '56', '32.55']
h_lon = ['E', '013', '37', '38.21']


class CoordinatePairExtraction:

    COORD_PATTERNS = {
        AF_DMSH_COMP: _coord_pair(r'\d{7}\.\d+[EW]|\d{7}[EW]', r'\d{6}\.\d+[NS]|\d{6}[NS]'),
        AF_HDMS_COMP: _coord_pair(r'[EW]\d{7}\.\d+|[EW]\d{7}', r'[NS]\d{6}\.\d+|[NS]\d{6}'),
        DMSH_SEP: _coord_pair(r'''\d{1,3}\W\d{1,2}\W\d{1,2}\.\d+\W{1,2}[EW]|\d{1,3}\W\d{1,2}\W\d{1,2}\W{1,2}[EW]''',
                              r'''\d{1,2}\W\d{2}\W\d{1,2}\.\d+\W{1,2}[NS]|\d{1,2}\W\d{1,2}\W\d{1,2}\W{1,2}[NS]'''),
        HDMS_SEP: _coord_pair(r'''[EW]\d{1,3}\W\d{1,2}\W\d{1,2}\.\d+\W{1,2}|[EW]\d{1,3}\W\d{1,2}\W\d{1,2}\{1,2}W''',
                              r'''[NS]\d{1,2}\W\d{2}\W\d{1,2}\.\d+\W{1,2}|[NS]\d{1,2}\W\d{1,2}\W\d{1,2}\W{1,2}''')
    }

    def __init__(self, coord_order, coord_format, coord_sep):
        """
        :param coord_order: str, constant that defines longitude and latitude order in coordinate pair,
                            e.g. LL_ORDER_LATLON.
        :param coord_format: str, constant that defines format of coordinate, e.g. AF_DMSH_COMP.
        :param coord_sep: str, defines separator between longitude and latitude, e.g. LL_SEP_SPACE.
        """
        self.coord_order = coord_order
        self.coord_format = coord_format
        self.coord_sep = coord_sep
        self.coord_regex_str = self.create_coord_pair_pattern()

    def create_coord_pair_pattern(self):
        """ Creates regular expression string based coordinates order, coordinates format and sepeartor
        between longitude and latitude. """
        regex_str = ''

        # Initialize longitude and latitude patterns
        lon_pattern, lat_pattern = CoordinatePairExtraction.COORD_PATTERNS.get(self.coord_format)

        # Create pattern for coordinate pair
        if self.coord_order == LL_ORDER_LONLAT:
            regex_str = r'(?P<lon>' + lon_pattern + ')' + \
                        re.escape(self.coord_sep) + \
                        '(?P<lat>' + lat_pattern + ')'

        elif self.coord_order == LL_ORDER_LATLON:
            regex_str = r'(?P<lat>' + lat_pattern + ')' +\
                        re.escape(self.coord_sep) +\
                        '(?P<lon>' + lon_pattern + ')'
        return regex_str

    def get_coord_regex(self):
        return re.compile(self.coord_regex_str)

    @staticmethod
    def create_coord_raw_str(raw_str):
        """ Creates 'continuous' string without new lines characters. It is for case when one coordinate (
        longitude, latitude) might be in two lines.
        :param raw_str: str, text from which coordinates are extracted.
        :return: shape_str: str, string without new line character
        """
        shape_str = ''
        for line in raw_str:
            shape_str += line.strip('\n')
        return shape_str

    def get_coordinate_pair_list(self, text):
        """ Gets list of coordinate pairs from text
        :param text: str, text from which coordinates are extracted.
        :return: fetched_list: list of tuples with extracted coordinate pairs.
                Note: longitude latitude order is the same as in self.coord_order attribute.
         """
        # Create string from raw text, note: raw text may contain new line characters
        searched_text = self.create_coord_raw_str(text)
        coord_pair_regex = self.get_coord_regex()
        fetched_list = re.findall(coord_pair_regex, searched_text)
        return fetched_list

    def get_coordinate_pair_example(self):
        """ Gets example of coordinate pair for extraction based on:
        coordinate order, separator and format. """
        sample = ''
        lon, lat = '', ''
        if self.coord_format == AF_DMSH_COMP:
            lon, lat = ''.join(lon_h), ''.join(lat_h)
        elif self.coord_format == AF_HDMS_COMP:
            lon, lat = ''.join(h_lon), ''.join(h_lat)
        elif self.coord_format == DMSH_SEP:
            lon, lat = ' '.join(lon_h), ' '.join(lat_h)
        elif self.coord_format == HDMS_SEP:
            lon, lat = ' '.join(h_lon), ' '.join(h_lat)

        if self.coord_order == LL_ORDER_LONLAT:
            sample = '{lon}{sep}{lat}'.format(lon=lon, sep=self.coord_sep, lat=lat)
        elif self.coord_order == LL_ORDER_LATLON:
            sample = '{lat}{sep}{lon}'.format(lon=lon, sep=self.coord_sep, lat=lat)

        return sample
