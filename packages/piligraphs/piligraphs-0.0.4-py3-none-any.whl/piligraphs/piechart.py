from PIL import Image, ImageDraw

from .graph import NodeGraph
from .utils import circle_xy, limit


class PieChart(NodeGraph):
    """Class representing a pie chart."""

    def __init__(
        self,
        radius: int,
        *,
        thickness: int | None = None,
        angle: int | float = 0,
        emboss: int = 0,
        gap: int = 0
    ) -> None:
        """
        Attributes
        ----------
        radius: `int`
            Radius of the chart circle.
        thickness: `int` | `None`
            If `None`, graph will be pie-shaped.
            Otherwise, graph will be donut-shaped with specified thickness.
        angle: `int` | `float`
            Start angle of the chart.
        emboss: `int`
            Difference between the largest and smallest slice.
            If < 0, slice size inverts (bigger value = smaller radius).
        gap: `int`
            Space between the pie slices.
        """
        super().__init__()

        self.radius = radius
        self.thickness = thickness
        self.angle = angle
        self.emboss = emboss
        self.gap = gap

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
    def thickness(self) -> int | None:
        """Donut-shaped chart thickness."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value: int | None):
        if isinstance(value, int) or value is None:
            self._thickness = value
        else:
            raise TypeError(f"thickness must be an int or None, not {type(value).__name__}")
        
    @property
    def angle(self) -> int | float:
        """Start angle."""
        return self._angle
    
    @angle.setter
    def angle(self, value: int | float):
        if isinstance(value, (int, float)):
            self._angle = value
        else:
            raise TypeError(f"angle must be an int, not {type(value).__name__}")
        
    @property
    def emboss(self) -> int:
        """Difference between the largest and smallest slice."""
        return self._emboss
    
    @emboss.setter
    def emboss(self, value: int):
        if isinstance(value, int):
            self._emboss = value
        else:
            raise TypeError(f"emboss must be an int, not {type(value).__name__}")
    
    @property
    def gap(self) -> int:
        """Space between the pie slices."""
        return self._gap
    
    @gap.setter
    def gap(self, value: int):
        if isinstance(value, int):
            self._gap = value
        else:
            raise TypeError(f"gap must be an int, not {type(value).__name__}")

    def draw(self) -> Image.Image:
        radius = self.radius
        w = radius * 2
        image = Image.new('RGBA', (w, w))
        num_nodes = len(self.nodes)

        if num_nodes == 0:
            return image
        
        draw = ImageDraw.Draw(image)

        weights = [node.weight for node in self.nodes]
        total_weight = sum(weights)
        start_angle = self.angle
        emboss = self.emboss
        gap = self.gap
        clear_co = (0, 0, 0, 0)
        eq_angle = 360 / num_nodes
        w_angle = 360 / total_weight

        offsets = limit(
            weights, 
            0 if emboss < 0 else abs(emboss), 
            abs(emboss) if emboss < 0 else 0
        )

        for num, node in enumerate(self.nodes):
            offset = offsets[num]
            angle = eq_angle if total_weight == 0 else w_angle * node.weight 
            end_angle = start_angle + angle

            if node.color is not None:
                draw.pieslice(
                    (
                        (offset, offset), 
                        (w - offset, w - offset)
                    ),
                    start_angle, 
                    end_angle,
                    fill=node.color.rgba,
                    width=0
                )
                
                if gap > 0 and num:
                    draw.line(
                        (
                            (radius, radius), 
                            circle_xy(radius, radius, start_angle)
                        ),
                        fill=clear_co, 
                        width=gap
                    )
                
                if self.thickness > 0:
                    l_space = self.thickness - offset
                    r_space = w - l_space

                    draw.pieslice(
                        ((l_space, l_space), (r_space, r_space)),
                        start_angle,
                        end_angle,
                        fill=clear_co,
                        width=0
                    )

            start_angle += angle

        if gap:
            draw.line(
                (
                    (radius, radius), 
                    circle_xy(radius, radius, start_angle)
                ),
                fill=clear_co, 
                width=gap
            )
            
            half_gap = gap / 2

            draw.ellipse(
                (
                    (radius - half_gap, radius - half_gap), 
                    (radius + half_gap, radius + half_gap)
                ),
                fill=clear_co, 
                width=0
            )
            
        return image
