import math
from collections import namedtuple
from deal_longlat import minify_longlat
import functools


def easy_long_lat(func):
    @functools.wraps(func)
    def wrapper(longitude):
        if isinstance(longitude, float) or isinstance(longitude, int):
            long = float(longitude)
            return func(long)
        if isinstance(longitude, str):
            long = minify_longlat(longitude)
            return func(long)
        raise ValueError("输入参数只能是整数、浮点数或者满足要求的字符串")

    return wrapper


@easy_long_lat
def cgcs2000_6deg_zone(longitude):
    return math.ceil(longitude / 6)


def cgcs2000_6deg_cm(longitude):
    return cgcs2000_6deg_zone(longitude) * 6


def cgcs2000_3deg_zone(longitude):
    return math.ceil((longitude - 1.5) / 3)


def cgcs2000_3deg_cm(longitude):
    return cgcs2000_3deg_zone(longitude) * 3


def utm_zone(longitude):
    return math.floor((180 + longitude) / 6) + 1


def utm_cm(longitude):
    return -180 + utm_zone(longitude) * 6 - 3


utm_epsg = namedtuple('utm_epsg', ['north', 'south'])


def get_wgs84utm_epsg(longitude):
    code = utm_zone(longitude)
    north_code = 32600 + code
    south_code = 32700 + code
    return utm_epsg(north_code, south_code)


cgcs2000_epsg = namedtuple('epsg', ['epsg_zone', 'epsg_cm'])


def get_cgcs2000_3deg_epsg(longitude):
    epsg_zone = 4513 + cgcs2000_3deg_zone(longitude) - 25
    epsg_cm = epsg_zone + 21
    return cgcs2000_epsg(epsg_zone, epsg_cm)


def get_cgcs2000_6deg_epsg(longitude):
    epsg_zone = 4491 + cgcs2000_6deg_zone(longitude) - 13
    epsg_cm = epsg_zone + 11
    return cgcs2000_epsg(epsg_zone, epsg_cm)
