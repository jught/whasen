import pandas as pd

def leer_excel(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return None

from PIL import Image
import cairosvg
import io

def convertir_svg_a_ico(svg_path, output_ico):
    # Leer y convertir el SVG a PNG
    png_bytes = cairosvg.svg2png(url=svg_path)
    
    # Abrir como imagen con PIL
    img = Image.open(io.BytesIO(png_bytes))
    
    # Redimensionar para tamaños de icono estándar (opcional)
    img = img.resize((256, 256), Image.LANCZOS)
    
    # Guardar como .ico
    img.save(output_ico, format='ICO')
    print(f"Icono guardado como: {output_ico}")

# Ejemplo de uso
convertir_svg_a_ico("icono.svg", "icono.ico")
