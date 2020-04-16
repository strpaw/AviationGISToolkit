"""
const.py
const module provides common constants as unit of measure, angle types used in aviation_gis_toolkit package.
"""

# ------------------- Units of measure ------------------- #

UOM_M = 'm'
UOM_KM = 'km'
UOM_NM = 'NM'
UOM_FT = 'ft'
UOM_SM = 'SM'

UOM_LIST = [UOM_M, UOM_KM, UOM_NM, UOM_FT, UOM_SM]

# ------------------- Angle types ------------------- #

# Angle types
AT_LON = 'AT_LON'
AT_LAT = 'AT_LAT'

# ------------------- Angle formats ------------------- #

# Degrees, minutes, seconds, hemisphere - compacted formats:
AF_DMSH_COMP = 'AF_DMSH_COMP'  # e.g.: 552243.47N
AF_HDMS_COMP = 'AF_HDMS_COMP'  # e.g.: N552243.47

# Degrees, minutes - compacted formats:
AF_DMH_COMP = 'AF_DMH_COMP'  # e.g.: 5522.47N
AF_HDM_COMP = 'AF_HDM_COMP'  # e.g.: N5522.47

# Degrees, hemisphere - compacted formats:
AF_DH_COMP = 'AF_DH_COMP'  # e.g.: 55.47N
AF_HD_COMP = 'AF_HD_COMP'  # e.g.: N55.47

# 'Separated' formats
AF_DMSH_ALL_SEP = 'AF_DMSH_ALL_SEP'  # e.g.: 55 22 43.47 N
AF_HDMS_ALL_SEP = 'AF_HDMS_ALL_SEP'
AF_DMSH_SEP = 'AF_DMSH_SEP'  # e.g.: 55 22 43.47N
AF_HDMS_SEP = 'AF_HDMS_SEP'
AF_DMSH_SEP_SYMBOLS = 'AF_DMSH_SEP_SYMBOLS'
AF_HDMS_SEP_SYMBOLS = 'AF_HDMS_SEP_SYMBOLS'

