from svgwrite import Drawing
from PIL import Image
import cairosvg
import io
from .mygroup import MyGroup


class Rectangle(MyGroup):
    def __init__(self, dwg, group_id, width, height, x_offset=0, y_offset=0, stroke_width=8, fill_color="none"):
        """
        Initialise the Rectangle with configurable dimensions and offsets.
        """
        super().__init__(dwg, group_id, stroke_color="black", fill_color=fill_color)
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.stroke_width = stroke_width

    def draw(self):
        """
        Draw or update the rectangle on the drawing.
        """
        self.replace_group()
        self.group.add(self.dwg.rect(
            insert=(self.x_offset, self.y_offset),
            size=(self.width, self.height),
            fill=self.fill_color,
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        ))
        self.add_to_dwg()


class MyIcon:
    def __init__(
            self, 
            width=900, height=700, 
            profile='tiny', path='envelope', 
            bg_color="white", stroke_color="#58D7DF",
            stroke_width=None
        ):
        """
        Initialise the drawing canvas with specified dimensions.
        """
        self.dwg = Drawing(size=(width, height), profile=profile)
        self.path = path
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.stroke_color = stroke_color
        self.stroke_width=stroke_width

        # Envelope dimensions - 75% of width and height
        rect_width = self.width * 0.75
        rect_height = self.height * 0.6
        x_offset = (self.width - rect_width) / 2
        y_offset = (self.height - rect_height) / 2

        self.envelope = Rectangle(
            self.dwg, 'rectangle',
            width=rect_width,
            height=rect_height,
            x_offset=x_offset,
            y_offset=y_offset,
            stroke_width=stroke_width
        )
        self.text_group = MyGroup(self.dwg, 'text', stroke_color="black")

    def draw_background(self, radius=30, transparency=0.6):
        """
        Draw a rounded rectangle as the background (message bubble effect).
        """
        self.dwg.add(self.dwg.rect(
            insert=(0, 0),  # Top-left corner
            size=(self.width, self.height),  # Full canvas size
            rx=radius,
            ry=radius,
            fill="skyblue",
            fill_opacity=transparency
        ))

    def draw_envelope_lines(self, stroke_width=None):
        """
        Draw the lines to simulate the envelope's folding, using the rectangle's height and offset.
        """
        if self.stroke_width is None: self.stroke_width = stroke_width
        line_group = MyGroup(self.dwg, 'resolutions', stroke_color=self.stroke_color)
        line_group.replace_group()

        # Use rectangle's position and size as reference
        env_x = self.envelope.x_offset
        env_y = self.envelope.y_offset
        env_width = self.envelope.width
        env_height = self.envelope.height
        sw = self.stroke_width if stroke_width is None else stroke_width
        # Draw folding triangle
        line_group.group.add(self.dwg.polyline(
            points=[
                (env_x, env_y + env_height),  # Bottom left
                (env_x + env_width / 2, env_y),  # Top center
                (env_x + env_width, env_y + env_height)  # Bottom right
            ],
            fill="none",
            stroke=line_group.stroke_color,
            stroke_width=sw
        ))

        # Vertical lines
        line_group.vertical_line(env_x, env_y, env_height, stroke_width=sw)
        line_group.vertical_line(env_x + env_width, env_y, env_height, stroke_width=sw)

    def draw_text(self, text='WHASEN', font_size=None, font_size_ratio=0.1):
        """
        Draw text below the envelope, scaling font size dynamically to fit the full width.
        """
        self.text_group.replace_group()

        max_width = self.width * 0.9
        base_font_size = int(self.width * font_size_ratio)
        font_size = font_size or base_font_size

        approx_char_width = font_size * 0.6
        text_width = approx_char_width * len(text)

        # Scale down if necessary
        if text_width > max_width:
            scaled_font_size = font_size * (max_width / text_width)
        else:
            scaled_font_size = font_size
        text_y_position = self.envelope.y_offset + self.envelope.height*1.2  # Ajuste debajo del sobre

        text_element = self.dwg.text(
            text,
            insert=(self.width * 0.5, text_y_position),
            fill=self.text_group.stroke_color,
            font_size=f'{int(scaled_font_size)}px',
            font_family='Arial',
            font_weight='bold',
            text_anchor='middle'
        )

        self.text_group.group.add(text_element)
        self.text_group.add_to_dwg()

    def svg(self):
        self.dwg.saveas(f'{self.path}.svg')

    def ico(self, scale=6):
        try:
            self.svg()
            png_bytes = cairosvg.svg2png(url=f'{self.path}.svg', output_width=256*scale, output_height=256*scale)
            img = Image.open(io.BytesIO(png_bytes))
            img = img.crop(img.getbbox())
            img = img.resize((256, 256), Image.LANCZOS)
            img.save(
                f'{self.path}.ico', 
                format='ICO', 
                sizes=[
                    (24,24),
                    (32,32),
                    (48,48),
                    (64,64),
                    (128,128),
                    (256, 256)                    
                ]
            )
        except Exception as e:
            raise RuntimeError(f"Error during SVG to ICO conversion: {e}")
