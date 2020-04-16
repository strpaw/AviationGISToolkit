"""
base_tools.py - common features
"""


class BasicTools:

    def __init__(self):
        """ Class with basic functionality common to objects such as angle, coordinates par, bearing, point.

        Attributes:
        -----------
        is_valid : bool
            to inform is given instance of object (e.g. LatLon coordinates pair) is valid or not
        err_msg : str
            to keeps information why given instance of object (e.g. LatLon coordinates pair) is not valid,
            e. g. 'Latitude not valid'
        """
        self.is_valid = None
        self.err_msg = ''

    @staticmethod
    def get_normalized_src_value(src_value):
        """ Normalizes source (input)  value for further processing.
        Method trims leading and trailing white characters, new line character and replace comma separated character
        into decimal point, e.g.:
        '   n 45 45 22,77733  ' -> 'N 45 45 22.7733'
        This method is useful for parsing coordinates, magnetic variation, bearing, distance etc.
        :param src_value: str, input angle string to normalize
        :return: norm_src_value: str, normalized angle string
        """
        norm = str(src_value).strip()
        norm = norm.replace(',', '.')
        norm = norm.upper()
        return norm

    @staticmethod
    def is_within_range(number, range_min, range_max):
        """ Checks if number is within specified range.
        :param number: float, number to check is within range
        :param range_min: float, minimum range
        :param range_max: float, maximum range
        :return: bool: True if number is within range, False otherwise
        """
        return bool(range_min <= float(number) <= range_max)

    @staticmethod
    def get_value_as_float_number(num):
        """ Converts argument num to float type.
        Useful to check if string contains only float number e.g. '-45.3555'
        :param num: float, angle in DD format
        :return bool: True if is, False otherwise
        """
        try:
            n = float(num)
        except ValueError:
            return None
        else:
            return n

    @staticmethod
    def get_value_as_int_number(num):
        """ Converts argument num to int type.
        Useful to check if string contains only int number e.g. '5'
        :param num: float, angle in DD format
        :return bool: True if is, False otherwise
        """
        try:
            n_str = str(num)
            if n_str.find('.') == -1:  # No decimal point in string
                return int(num)
            else:
                return None
        except ValueError:
            return None
