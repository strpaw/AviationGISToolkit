"""
ellipsoid_calc.py
ellipsoid_calc module provides functionality to various calculation on ellipsoid such as
coordinate point based on the coordinate initial point and distance and bearing,
distance between to points.
"""
import math
from collections import namedtuple

ellipsoid = namedtuple('Ellipsoid', ['A', 'B', 'F'])

ellipsoids = {'WGS84': ellipsoid(A=6378137.0, B=6356752.3141, F=1 / 298.25722210088),
              'WGS72': ellipsoid(A=6378135.0, B=6356750.52, F=1 / 298.26000000000)}


def vincenty_direct_solution(lon_initial, lat_initial, azimuth_initial, distance, ellipsoid_name):
    """ Computes the latitude and longitude of the second point based on latitude, longitude,
    of the first point and distance and azimuth from first point to second point.
    Uses the algorithm by Thaddeus Vincenty for direct geodetic problem.
    For more information refer to: http://www.ngs.noaa.gov/PUBS_LIB/inverse.pdf
    :param lon_initial: float, longitude of the initial  point in decimal degrees format
    :param lat_initial: float, latitude of the initial point in decimal degrees format
    :param azimuth_initial, azimuth from the initial point to the end point in decimal degrees format
    :param distance: float, distance from first point to second point; meters
    :param ellipsoid_name: str, ellipsoid short name, e.g.: WGS84
    :return lon_end, lat_end: float, float longitude and longitude of the end point in decimal degrees format
    """
    # Unpack parameters of ellipsoid
    a, b, f = ellipsoids[ellipsoid_name]

    # Convert latitude, longitude, azimuth of the initial point to radians
    lon1 = math.radians(lon_initial)
    lat1 = math.radians(lat_initial)
    alfa1 = math.radians(azimuth_initial)

    sin_alfa1 = math.sin(alfa1)
    cos_alfa1 = math.cos(alfa1)

    # U1 - reduced latitude
    tan_u1 = (1 - f) * math.tan(lat1)
    cos_u1 = 1 / math.sqrt(1 + tan_u1 * tan_u1)
    sin_u1 = tan_u1 * cos_u1

    # sigma1 - angular distance on the sphere from the equator to initial point
    sigma1 = math.atan2(tan_u1, math.cos(alfa1))

    # sin_alfa - azimuth of the geodesic at the equator
    sin_alfa = cos_u1 * sin_alfa1
    cos_sq_alfa = 1 - sin_alfa * sin_alfa
    u_sq = cos_sq_alfa * (a * a - b * b) / (b * b)
    A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))

    sigma = distance / (b * A)
    sigmap = 1
    sin_sigma, cos_sigma, cos2sigma_m = None, None, None

    while math.fabs(sigma - sigmap) > 1e-12:
        cos2sigma_m = math.cos(2 * sigma1 + sigma)
        sin_sigma = math.sin(sigma)
        cos_sigma = math.cos(sigma)
        d_sigma = B * sin_sigma * (cos2sigma_m + B / 4 * (
                    cos_sigma * (-1 + 2 * cos2sigma_m * cos2sigma_m) - B / 6 * cos2sigma_m * (
                        -3 + 4 * sin_sigma * sin_sigma) * (-3 + 4 * cos2sigma_m * cos2sigma_m)))
        sigmap = sigma
        sigma = distance / (b * A) + d_sigma

    var_aux = sin_u1 * sin_sigma - cos_u1 * cos_sigma * cos_alfa1  # Auxiliary variable

    # Latitude of the end point in radians
    lat2 = math.atan2(sin_u1 * cos_sigma + cos_u1 * sin_sigma * cos_alfa1,
                      (1 - f) * math.sqrt(sin_alfa * sin_alfa + var_aux * var_aux))

    lamb = math.atan2(sin_sigma * sin_alfa1, cos_u1 * cos_sigma - sin_u1 * sin_sigma * cos_alfa1)
    C = f / 16 * cos_sq_alfa * (4 + f * (4 - 3 * cos_sq_alfa))
    L = lamb - (1 - C) * f * sin_alfa * (
                sigma + C * sin_sigma * (cos2sigma_m + C * cos_sigma * (-1 + 2 * cos2sigma_m * cos2sigma_m)))
    # Longitude of the end point in radians
    lon2 = (lon1 + L + 3 * math.pi) % (2 * math.pi) - math.pi

    # Convert to decimal degrees
    lon_end = math.degrees(lon2)
    lat_end = math.degrees(lat2)

    return lon_end, lat_end
