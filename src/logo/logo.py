from svgwrite import Drawing
from svgwrite.container import Group
from PIL import Image
import cairosvg
import io

def convertir_svg_a_ico(svg_path, output_ico):
    scale = 6
    
    # Convertir SVG a PNG de alta resolución
    png_bytes = cairosvg.svg2png(url=svg_path, output_width=256*scale, output_height=256*scale)
    img = Image.open(io.BytesIO(png_bytes))
    
    # Recortar bordes vacíos automáticamente
    img = img.crop(img.getbbox())  # TRIM del espacio vacío
    
    # Redimensionar a 256x256 para garantizar tamaño correcto
    img = img.resize((256, 256), Image.LANCZOS)
    
    # Guardar solo la versión grande del icono
    img.save(output_ico, format='ICO', sizes=[(256, 256)])
    print(f"Icono guardado correctamente como: {output_ico}")


def draw_envelope(dwg):
    envelope_group = Group(id='envelope')
    
    envelope_group.add(dwg.rect(
        insert=(100, 300),
        size=(300, 150),
        fill="none",
        stroke="black",
        stroke_width=8
    ))
    
    envelope_group.add(dwg.polyline(
        points=[(100, 450), (250, 300), (400, 450)],
        fill="none",
        stroke="#58D7DF",
        stroke_width=8
    ))
    
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
    text_group = Group(id='text')
    text_group.add(dwg.text(
        'HASEN',
        insert=(180, 425),
        fill='black',
        font_size='40px',
        font_family='Arial',
        font_weight='normal'
    ))
    dwg.add(text_group)
    return dwg


def create_logo():
    dwg = Drawing(size=(900, 700), profile='tiny')
    draw_envelope(dwg).saveas('./envelope.svg')
    draw_text(dwg).saveas('./whasen_logo.svg')


if __name__ == "__main__":
    create_logo()
    convertir_svg_a_ico("envelope.svg", "whasen_logo.ico")
