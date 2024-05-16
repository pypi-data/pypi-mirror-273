import math
import numpy as np
from scipy.interpolate import interp1d
from typing import Literal


Interpolation = Literal[
    'linear',
    'nearest',
    'nearest-up',
    'zero',
    'slinear',
    'quadratic',
    'cubic',
    'previous',
    'next'
]


def rgb_to_hex(_rgb: tuple[int, int, int], /):
    return '{:02x}{:02x}{:02x}'.format(_rgb[0], _rgb[1], _rgb[2])


def hex_to_rgb(_hex: str, /):
    return tuple(int(_hex.strip('#')[i:i+2], 16) for i in (0, 2, 4))


def num_to_rgb(_num: int, /):
    return (
        (_num >> 16) & 255,
        (_num >> 8) & 255,
        _num & 255
    )


def rgb_to_num(_rgb: tuple[int, int, int], /):
    return (_rgb[0] << 16) + (_rgb[1] << 8) + _rgb[2]


def circle_xy(radius: int, distance: int, angle: int):
    rad = math.radians(angle)
    return (
        radius + distance * math.cos(rad),
        radius + distance * math.sin(rad)
    )


def interpolate(
    points: list[tuple[int, int]], 
    num: int | None = None, 
    kind: str = 'linear'
) -> list[tuple[int, int]]:
    """
    Interpolate a list of points to make a smooth curve.

    Attributes
    ----------
    points: `list[tuple[int, int]]`
        List of points. Every point must be a tuple containing 2 integers: x and y.
    num: `int` | `None`
        Number of points. If `None`, double the length of the list of points is set.
    kind: `Interpolation`
        The kind of interpolation.
    """
    x, y = zip(*points)
    inter = interp1d(x, y, kind=kind)

    if not num:
        num = len(points) * 2

    x_new = np.linspace(min(x), max(x), num)
    y_new = np.clip(inter(x_new), min(y), max(y))

    return list(zip(x_new, y_new))


def limit(
    values: list[int | float],
    minv: int | float,
    maxv: int | float,
    *,
    copy: bool = True
) -> np.ndarray:
    """
    Limit array to specific range.

    Attributes
    ----------
    values: `list[int | float]`
        List of values.
    minv: `int | float`
        Minimum (bottom) value.
    maxv: `int | float`
        Maximum (top) value.
    copy: `bool`
        Copy an array or not.
    """
    array = np.array(values, copy=copy)
    _min, _max = min(array), max(array)

    if _max == _min:
        return array

    m = (maxv - minv) / (_max - _min)
    b = maxv - m * _max

    return m * array + b


def linear_to_circle(
    points: list[tuple[int, int]], 
    radius: int, 
    min_radius: int = 0, 
    angle: int = 0
) -> list[tuple[int, int]]:
    """
    Convert linear points to circular.

    Attributes
    ----------
    points: `list[tuple[int, int]]`
        List of points.
    radius: `int`
        Max radius.
    min_radius: `int`
        Min radius.
    angle: `int`
        Rotation angle.
    """
    y = [p[1] for p in points]
    max_y = max(y)
    ang = 360 / (len(points) - 1)
    radii = limit([max_y - i for i in y], min_radius, radius)

    return [
        circle_xy(radius, rad, i * ang + angle)
        for i, rad in enumerate(radii)
    ]