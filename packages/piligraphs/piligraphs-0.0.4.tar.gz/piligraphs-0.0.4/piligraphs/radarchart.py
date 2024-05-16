from pinkie import Color
from PIL import Image, ImageDraw

from .graph import NodeGraph
from .utils import interpolate, linear_to_circle, Interpolation


class RadarChart(NodeGraph):
    """Class representing a radar chart."""

    def __init__(
        self,
        radius: int,
        *,
        thickness: int = 1,
        fill: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        outline: Color | int | str | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
        pwidth: int = 0,
        onlysrc: bool = True,
        npoints: int | None = None,
        interp: Interpolation = 'linear',
        angle: int | float = 0,
        minr: int = 0
    ) -> None:
        """
        Attributes
        ----------
        radius: `int`
            Radius of the chart shape.
        thickness: `int`
            Line thickness.
        fill: `Color`
            Fill color. If = `...`, generates a random color.
        outline: `Color`
            Line color. If = `...`, generates a random color.
        pwidth: `int`
            Point width.
        onlysrc: `bool`
            To draw bold dots only in source points (without interpolated ones).
        npoints: `int` | `None`
            Number of points. If `None`, equals to the number of nodes.
        interp: `str`
            Kind of interpolation. Used to make a smooth curve.
        angle: `int` | `float`
            Start angle of the chart.
        minr: `int`
            Minimum distance between the center and a point.
        """
        super().__init__()

        self.radius = radius
        self.thickness = thickness
        self.fill = fill
        self.outline = outline
        self.pwidth = pwidth
        self.onlysrc = onlysrc
        self.npoints = npoints
        self.interp = interp
        self.angle = angle
        self.minr = minr

    @property
    def radius(self) -> int:
        """Chart radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        if isinstance(value, int):
            self._radius = value
        else:
            raise TypeError(f"radius must be an int, not {type(value).__name__}")
        
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
    def angle(self) -> int | float:
        """Start angle."""
        return self._angle
    
    @angle.setter
    def angle(self, value: int | float):
        if isinstance(value, (int, float)):
            self._angle = value
        else:
            raise TypeError(f"angle must be an int or float, not {type(value).__name__}")
        
    @property
    def minr(self) -> int:
        """Minimal distance from center to point."""
        return self._minr
    
    @minr.setter
    def minr(self, value: int):
        if isinstance(value, int):
            self._minr = value
        else:
            raise TypeError(f"minr must be an int, not {type(value).__name__}")

    def draw(self) -> Image.Image:
        w = self.radius * 2
        image = Image.new('RGBA', (w, w))

        if len(self.nodes) == 0:
            return image

        nodes = self.nodes.copy()
        nodes.append(nodes[0])
        num_nodes = len(nodes)
        
        draw = ImageDraw.Draw(image)

        thickness = self.thickness
        num = self.npoints if self.npoints is not None else num_nodes
        max_weight = max((i.weight for i in nodes))
        radius = self.pwidth / 2 if self.pwidth > 0 else thickness / 2
 
        source_p = list(zip(
            [w / (num_nodes - 1) * i for i in range(num_nodes)], 
            [max_weight - node.weight for node in nodes]
        ))
        smooth_p = interpolate(source_p, num, kind=self.interp)
        circle_p = linear_to_circle(
            smooth_p, 
            self.radius - self.pwidth, 
            self.minr,
            self.angle
        )

        if self.fill:
            draw.polygon(
                circle_p,
                fill=self.fill.rgba, 
                outline=self.outline.rgba,
                width=0
            )

        if self.outline:
            draw.line(
                circle_p, 
                fill=self.outline.rgba, 
                width=thickness, 
                joint='curve'
            )

            bold_p = (circle_p[0],)
            if self.pwidth > 0:
                step = num // num_nodes
                bold_p = circle_p[::step] if self.onlysrc and step else circle_p

            for p in bold_p:
                draw.ellipse(
                    (p[0] - radius, p[1] - radius,
                    p[0] + radius, p[1] + radius),
                    fill=self.outline.rgba, 
                    width=0
                )

        return image

