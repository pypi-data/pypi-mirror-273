import numpy as np
from pinkie import Color
from typing import Callable
from PIL import Image, ImageDraw

from .graph import Graph


class FuncGraph(Graph):
    """
    Class representing a function graph.

    ## WARNING
    `tan()` and similar functions can be drawn incorrectly
    since we cannot determine the asymptotes automatically.
    Instead of using raw `tan()`, you should make a custom solution:
    ```
    res_x, res_y = (40, 40)

    def tangent(x: float) -> float | None:
        step = math.pi
        diap = 1 / (res_x * 3)
        current = math.pi / 2
        while current < res_x:
            if abs(x) > current - diap and abs(x) < current + diap:
                return None
            current += step
        return math.tan(x)

    graph = FuncGraph(
        (1000, 1000), 
        func=tangent, 
        thickness=16,
        res=(res_x, res_y),
        step=0.1
    )
    ```
    """

    def __init__(
        self,
        size: tuple[int, int],
        *,
        func: Callable[[float], float],
        thickness: int = 1,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] = ...,
        res: tuple[int, int] = (10, 10),
        npoints: int | None = None
    ) -> None:
        """
        Attributes
        ----------
        size: `tuple[int, int]`
            Image width and height.
        func: `Callable[[float], float]`
            Function for building a graph based on.
        thickness: `int`
            Line thickness.
        outline: `Color`
            Line color. If = `...`, generates a random color.
        res: `tuple[int, int]`
            Numbers of points from the center to x and y end respectively.
            Higher value = smaller scale.
        npoints: `int` | `None`
            Total number of points. Higher value = smoother result.
            If `None`, equals to image width divided by half of thickness.
        """
        super().__init__()

        self.size = size
        self.func = func
        self.thickness = thickness
        self.outline = outline
        self.res = res
        self.npoints = npoints

    @property
    def size(self) -> tuple[int, int]:
        """Image width and height."""
        return self._size
    
    @size.setter
    def size(self, value: tuple[int, int]):
        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError("size should contain 2 items")
            self._size = value
        else:
            raise TypeError(f"size must be a tuple, not {type(value).__name__}")
    
    @property
    def func(self) -> Callable[[float], float]:
        """Graph function."""
        return self._func
    
    @func.setter
    def func(self, value: Callable[[float], float]):
        if callable(value):
            self._func = value
        else:
            raise TypeError("func must be callable")
        
    @property
    def thickness(self) -> int:
        """Line thickness"""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int):
        if isinstance(value, int):
            self._thickness = value
        else:
            raise TypeError(f"thickness must be an int, not {type(value).__name__}")

    @property
    def outline(self) -> Color:
        """Line color."""
        return self._outline
    
    @outline.setter
    def outline(self, value: Color | int | str | tuple):
        if isinstance(value, Color):
            self._outline = value
        elif value is ...:
            self._outline = Color.random()
        else:
            self._outline = Color(value)

    @property
    def res(self) -> tuple[int, int]:
        """Number of points from the center to x and y edge."""
        return self._res
    
    @res.setter
    def res(self, value: tuple[int, int]):
        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError(f"res should contain 2 items")
            self._res = value
        else:
            raise TypeError(f"res must be a tuple, not {type(value).__name__}")

    @property
    def npoints(self) -> int | None:
        """Number of points."""
        return self._npoints
    
    @npoints.setter
    def npoints(self, value: int | None):
        if isinstance(value, int) or value is None:
            self._npoints = value
        else:
            raise TypeError(f"npoints must be an int or None, not {type(value).__name__}")
    
    def draw(self) -> Image.Image:
        image = Image.new('RGBA', self.size)
        draw = ImageDraw.Draw(image)

        w, h = self.size
        func = self.func
        thickness = self.thickness
        radius = thickness / 2
        res_x, res_y = self.res
        outline_rgba = self.outline.rgba
        step = w / self.npoints if self.npoints else w / radius
        lines: list[list[tuple[float, float]]] = [[]]
        
        for x in np.arange(radius, w - radius, step):
            try:
                x_val = (x / w - 0.5) * 2 * res_x
                y_val = func(x_val)

                if y_val is None:
                    lines.append([])
                    continue

                y = h - (y_val / (2 * res_y) + 0.5) * h
                    
                lines[-1].append((x, y))
            except Exception:
                lines.append([])
        
        for line in lines:
            if len(line) == 0:
                continue
            
            draw.line(
                line,
                fill=outline_rgba, 
                width=thickness, 
                joint='curve'
            )

            for x, y in (line[0], line[-1]):
                draw.ellipse(
                    (
                        (x - radius, y - radius),
                        (x + radius, y + radius)
                    ),
                    fill=outline_rgba,
                    width=0
                )
        
        return image


