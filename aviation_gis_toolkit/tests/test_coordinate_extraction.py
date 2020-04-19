import unittest
from aviation_gis_toolkit.coordinate_extraction import *


class CoordinatePairExtractionTests(unittest.TestCase):

    def test_get_coordinate_pair_list(self):

        test_txt_latlon_dmsh_comp_space = """
        512942N 0183840E
        513410N 0183538E 522454.3N 0165114.3E,
        514038N 0184547E 522458.0N 0165055.4E,
        514312N 0185425E """

        coord_extractor = CoordinatePairExtraction(LL_ORDER_LATLON, AF_DMSH_COMP, LL_SEP_SPACE)
        extracted_coord_pairs = coord_extractor.get_coordinate_pair_list(test_txt_latlon_dmsh_comp_space)

        coord_pairs = [
            ('512942N', '0183840E'), ('513410N', '0183538E'),  ('522454.3N', '0165114.3E'),
            ('514038N', '0184547E'),  ('522458.0N',  '0165055.4E'), ('514312N', '0185425E')
        ]

        self.assertEqual(coord_pairs, extracted_coord_pairs)

        test_txt_lonlat_dmsh_comp_hyphen = """
        0300108E-512824.111N  0300126E-512943N 
        0300612.7889E-512901N   0301202.445E-512913.4556N 
        0302034E-512325.988N   0301735E-512220N"""

        coord_extractor = CoordinatePairExtraction(LL_ORDER_LONLAT, AF_DMSH_COMP, LL_SEP_HYPHEN)
        extracted_coord_pairs = coord_extractor.get_coordinate_pair_list(test_txt_lonlat_dmsh_comp_hyphen)

        coord_pairs = [
            ('0300108E', '512824.111N'), ('0300126E', '512943N'),  ('0300612.7889E', '512901N'),
            ('0301202.445E', '512913.4556N'), ('0302034E', '512325.988N'), ('0301735E', '512220N')
        ]

        self.assertEqual(coord_pairs, extracted_coord_pairs)
