from svgwrite import Drawing
from svgwrite.container import Group


def draw_envelope(dwg):
    """
    Draw an upside-down envelope with a 'W' shaped flap in light blue.
    """
    envelope_group = Group(id='envelope')
    # Black rectangle for the envelope body
    envelope_group.add(dwg.rect(
        insert=(100, 300),
        size=(300, 150),
        fill="none",
        stroke="black",
        stroke_width=8
    ))
    # Light blue 'W' flap (upside down)
    envelope_group.add(dwg.polyline(
        points=[(100, 450), (250, 300), (400, 450)],
        fill="none",
        stroke="#58D7DF",
        stroke_width=8
    ))
    # Light blue sides
    envelope_group.add(dwg.line(
        start=(100, 300),
        end=(100, 450),
        stroke="#58D7DF",
        stroke_width=8
    ))
    envelope_group.add(dwg.line(
        start=(400, 300),
        end=(400, 450),
        stroke="#58D7DF",
        stroke_width=8
    ))
    dwg.add(envelope_group)
    return dwg


def draw_text(dwg):
    """
    Draw the 'HASEN' text to the right of the envelope, ensuring no cut-off.
    """
    text_group = Group(id='text')
    text_group.add(dwg.text(
        'HASEN',
        insert=(180, 425),  # Align with the center of the envelope
        fill='black',
        font_size='40px',
        font_family='Arial',
        font_weight='normal'
    ))
    dwg.add(text_group)
    return dwg


def create_logo():
    """
    Create an SVG logo with an envelope and the text 'HASEN' to the right.
    """
    dwg = Drawing(size=(900, 700), profile='tiny')  # Adjusted width to fit the design
    draw_envelope(dwg).saveas('./envelope.svg')
    draw_text(dwg).saveas('./whasen_logo.svg')

if __name__ == "__main__":
    create_logo()
