"""
distance.py
Distance module provides functionality to distance validation and conversion
"""
from .const import *


class Distance:
    """ Class covers actions related to distance: validation, conversion among various units of measure (UOM).
    Attributes:
    -----------
    src_dist : str or float or int
        Keeps source value of distance, note that this value can be with comma decimal separator not dot decimal
        separator, example: 109,25 109.25.
    src_uom : str
        Keeps source unit of measure of distance, e.g. UOM_M, UOM_KM.
    src_fdist: float
        Keeps source distance as float in source unit of measure, only if src_dist is valid.
    is_valid: bool
        Keeps information if distance is valid or not.
        Distance if considered as valid if src_dist can be converted into float number
        and src_uom is valid unit of measure.
    err_msg: str
        Keeps error message why distance is not valid, for example is unit of measure is not valid.
    """

    def __init__(self, src_dist, src_uom=UOM_M):
        self.src_dist = src_dist
        self.src_uom = src_uom
        self.src_fdist = None
        self.is_valid = None
        self.err_msg = ''
        self.check_distance()

    @staticmethod
    def get_normalized_src_value(src_value):
        """ Normalizes source (input)  value for further processing.
        Method trims leading and trailing white characters, new line character and replace comma separated character
        into decimal point, e.g.:
        '  134,99  ' ->  '134.99'
        :param src_value: str, input source value string to normalize
        :return: norm: str, normalized angle string
        """
        norm = str(src_value).strip()
        norm = norm.replace(',', '.')
        norm = norm.upper()
        return norm

    @staticmethod
    def is_dist_number(dist):
        """ Checks if input parameter can be converted to number and returns input as number in such case.
        :param: dist: str: distance to check if is a number
        :return: bool: True if dist is a number, False otherwise
                 err_msg: str, error message why result if False if it is
        """
        err_msg = ''
        norm_dist = Distance.get_normalized_src_value(dist)
        if norm_dist == '':
            err_msg = 'Distance error. Distance value can not be empty.'
            return False, err_msg, None
        else:
            try:
                num = float(norm_dist)
                if num < 0:
                    err_msg = 'Distance error. Distance not be less than 0.'.format(dist)
                    return False, err_msg, None
            except ValueError:
                err_msg = 'Distance error. Value {} can not be converted to number.'.format(dist)
                return False, err_msg, None
            else:
                return True, err_msg, num

    @staticmethod
    def is_uom(uom):
        """ Checks if input parameter can be converted to number and returns input as number in such case.
        :param: uom: str, const that determine unit of measure
        :return: bool: True if uom parameter is within supported UOMs, False otherwise
                err_msg: str, error message if uom is not valid
        """
        err_msg = ''
        if isinstance(uom, str):
            if uom.strip() == '':
                err_msg = 'Distance error. UOM is required and cannot be empty.'
                return False, err_msg
            elif uom not in UOM_LIST:
                err_msg = 'Distance error. UOM {} is not valid.'.format(uom)
                return False, err_msg
        else:
            err_msg = 'Distance error. UOM must be a string.'
            return False, err_msg

        return True, err_msg

    def check_distance(self):
        """ Checks if source distance and value are valid (a number). """
        is_number, err_number, src_fdist = self.is_dist_number(self.src_dist)
        is_uom, err_uom = self.is_uom(self.src_uom)
        if is_number and is_uom:
            self.src_fdist = src_fdist
            self.is_valid = True
        else:
            self.is_valid = False
            self.err_msg = err_number + err_uom

    def convert_dist_to_m(self):
        """ Converts source distance value from source UOM to meters. """
        if self.is_valid:
            # Convert to meters
            if self.src_uom == UOM_M:
                return self.src_fdist
            elif self.src_uom == UOM_KM:
                return self.src_fdist * 1000
            elif self.src_uom == UOM_NM:
                return self.src_fdist * 1852
            elif self.src_uom == UOM_FT:
                return self.src_fdist * 0.3048
            elif self.src_uom == UOM_SM:
                return self.src_fdist * 1609.344

    @staticmethod
    def convert_m_to_given_uom(dist_m, to_uom):
        """ Converts distance from meters to given UOM. """
        if to_uom in UOM_LIST:
            if to_uom == UOM_M:
                return dist_m
            elif to_uom == UOM_KM:
                return dist_m / 1000
            elif to_uom == UOM_NM:
                return dist_m / 1852
            elif to_uom == UOM_FT:
                return dist_m / 0.3048
            elif to_uom == UOM_SM:
                return dist_m / 1609.344

    def convert_dist_to_uom(self, to_uom):
        """ Convert distance between various units. """
        if self.is_valid:
            if to_uom in UOM_LIST:
                if self.src_uom == to_uom:
                    return self.src_fdist
                else:
                    d_m = self.convert_dist_to_m()  # Convert to meters
                    return self.convert_m_to_given_uom(d_m, to_uom)  # Convert from meters
