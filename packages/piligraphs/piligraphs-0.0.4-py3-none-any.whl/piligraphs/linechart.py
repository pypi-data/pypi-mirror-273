from pinkie import Color
from PIL import Image, ImageDraw

from .graph import NodeGraph
from .utils import limit, interpolate, Interpolation


class LineChart(NodeGraph):
    """Class representing a line chart."""

    def __init__(
        self,
        size: tuple[int, int],
        *,
        thickness: int = 1,
        fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        pwidth: int = 0,
        onlysrc: bool = False,
        npoints: int | None = None,
        interp: Interpolation = 'linear',
        minh: int = 0
    ) -> None:
        """
        Attributes
        ----------
        size: `tuple[int, int]`
            Image width and height.
        thickness: `int`
            Line thickness.
        fill: `Color` | `None`
            Fill color. If = `...`, generates a random color.
        outline: `Color` | `None`
            Line color. If = `...`, generates a random color.
        pwidth: `int`
            Point width.
        onlysrc: `bool`
            To draw bold dots only in source points (without interpolated ones).
        npoints: `int`
            Number of points. If <= 0, equals to the number of nodes.
        interp: `str`
            Kind of interpolation. Used to make a smooth curve.
        minh: `int`
            Minimum height from the bottom of the graph.
        """
        super().__init__()

        self.size = size
        self.thickness = thickness
        self.fill = fill
        self.outline = outline
        self.pwidth = pwidth
        self.onlysrc = onlysrc
        self.npoints = npoints
        self.interp = interp
        self.minh = minh

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
    def thickness(self) -> int:
        """Line thickness."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int):
        if isinstance(value, int):
            self._thickness = value
        else:
            raise TypeError(f"thickness must be an int, not {type(value).__name__}")

    @property
    def fill(self) -> Color | None:
        """Shape color. If `None`, no shape will be drawn."""
        return self._fill
    
    @fill.setter
    def fill(self, value: Color | int | str | tuple | None):
        if isinstance(value, Color) or value is None:
            self._fill = value
        elif value is ...:
            self._fill = Color.random()
        else:
            self._fill = Color(value)

    @property
    def outline(self) -> Color | None:
        """Line color. If `None`, no line will be drawn."""
        return self._outline
    
    @outline.setter
    def outline(self, value: Color | int | str | tuple | None):
        if isinstance(value, Color) or value is None:
            self._outline = value
        elif value is ...:
            self._outline = Color.random()
        else:
            self._outline = Color(value)

    @property
    def pwidth(self) -> int:
        """Point width."""
        return self._pwidth
    
    @pwidth.setter
    def pwidth(self, value: int):
        if isinstance(value, int):
            self._pwidth = value
        else:
            raise TypeError(f"pwidth must be an int, not {type(value).__name__}")
    
    @property
    def onlysrc(self) -> bool:
        """To draw only source points without interpolated ones."""
        return self._onlysrc
    
    @onlysrc.setter
    def onlysrc(self, value: bool):
        if isinstance(value, bool):
            self._onlysrc = value
        else:
            raise TypeError(f"onlysrc must be a bool, not {type(value).__name__}")

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
        
    @property
    def interp(self) -> Interpolation:
        """Kind of interpolation."""
        return self._interp
    
    @interp.setter
    def interp(self, value: Interpolation):
        if isinstance(value, Interpolation):
            self._interp = value
        else:
            raise TypeError("interp must be a valid string")
    
    @property
    def minh(self) -> int:
        """Minimal point height."""
        return self._minh
    
    @minh.setter
    def minh(self, value: int):
        if isinstance(value, int):
            self._minh = value
        else:
            raise TypeError(f"minh must be an int, not {type(value).__name__}")

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', self.size)
        num_nodes = len(self.nodes)

        if num_nodes == 0:
            return image
        
        draw = ImageDraw.Draw(image)

        w, h = self.size
        thickness = self.thickness
        num = self.npoints if self.npoints else num_nodes
        max_weight = max((i.weight for i in self.nodes))
        radius = self.pwidth / 2 if self.pwidth > 0 else thickness / 2

        lim_xs = limit(
            [w / (num_nodes - 1) * i for i in range(num_nodes)], 
            radius, 
            w - radius
        )

        if max_weight == 0:
            lim_ys = [h - radius] * num_nodes
        else:
            lim_ys = limit(
                [max_weight - node.weight for node in self.nodes], 
                radius, 
                h - radius - self.minh
            )
        
        source_p = list(zip(lim_xs, lim_ys))
        smooth_p = interpolate(source_p, num, kind=self.interp)

        if self.fill:
            draw.polygon(
                [(radius, h)] + smooth_p + [(w - radius, h)],
                fill=self.fill.rgba, 
                width=0
            )

        if self.outline:
            draw.line(
                smooth_p, 
                fill=self.outline.rgba, 
                width=thickness, 
                joint='curve'
            )

            bald_p = (source_p[0], source_p[num_nodes-1])
            if self.pwidth:
                bald_p = source_p if self.onlysrc else smooth_p

            for x, y in bald_p:
                draw.ellipse(
                    (
                        (x - radius, y - radius),
                        (x + radius, y + radius)
                    ),
                    fill=self.outline.rgba, 
                    width=0
                )

        return image
