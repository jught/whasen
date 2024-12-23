from svgwrite.container import Group

class MyGroup:
    def __init__(self, dwg, group_id, stroke_color="#333333", fill_color="none", **kwargs):
        """
        Base class for SVG groups that can draw shapes.
        """
        self.dwg = dwg
        self.group_id = group_id
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.kwargs = kwargs

    def draw(self):
        raise NotImplementedError("The draw method should be implemented in subclasses.")

    def replace_group(self):
        """
        Replace the current group by removing it from the drawing if it exists.
        """
        self.dwg.elements = [el for el in self.dwg.elements if el.get_id() != self.group_id]
        self.group = Group(id=self.group_id)

    def add_to_dwg(self):
        """
        Add the group to the drawing.
        """
        self.dwg.add(self.group)

    def vertical_line(self, x, y_0, height, stroke_width=8):
        """
        Draw a vertical line at the specified position.
        
        Parameters:
        - x: X-coordinate for the line.
        - y_0: Y-coordinate where the line starts.
        - height: Length of the line (from y_0 downwards).
        - stroke_width: Width of the line.
        """
        self.group.add(self.dwg.line(
            start=(x, y_0),
            end=(x, y_0 + height),
            stroke=self.stroke_color,
            stroke_width=stroke_width
        ))
        self.add_to_dwg()
