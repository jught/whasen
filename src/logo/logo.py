from myicon.myicon import MyIcon

def create_logo(width=900, height=700, font_size=80, bg_color="skyblue", stroke_color="#1C6EA4", stroke_width = 14):
    """
    Create and save the envelope logo with a background.
    """
    icon = MyIcon(
        width=width, height=height, 
        path='./src/logo/whasen_logo', 
        bg_color=bg_color, stroke_color=stroke_color,
        stroke_width = stroke_width
    )
    icon.draw_background(radius=70, transparency=1.0)
    icon.envelope.draw()
    icon.draw_envelope_lines(stroke_width=stroke_width*2)
    if font_size > 0:
        icon.draw_text(font_size=font_size)
    icon.svg()
    icon.ico(scale=10)


def create_logo_simple(width=1024, height=1024, font_size=500, bg_color="#1C6EA4"):
    """
    Create and save a simple logo with a large 'W' in the center.
    """
    icon = MyIcon(
        width=width, height=height, 
        path='./src/logo/whasen_logo_simple', 
        bg_color=bg_color, stroke_color="white",
        stroke_width=0  # No stroke for simplicity
    )
    icon.draw_background(radius=70, transparency=1.0)

    # Añadir texto grande 'W' centrado
    icon.text_group.replace_group()
    icon.text_group.group.add(icon.dwg.text(
        'W',
        insert=(width * 0.5, height * 0.6),  # Centrado en el lienzo
        fill="white",
        font_size=f'{font_size}px',
        font_family='Georgia',  # Fuente chula y llamativa
        font_weight='bold',
        text_anchor='middle'
    ))
    icon.text_group.add_to_dwg()

    icon.svg()
    icon.ico(scale=10)


if __name__ == "__main__":
    try:
        # Crear logo normal
        create_logo(
            1024, 
            1024, 
            font_size=100, 
            bg_color="#F5F5F5", 
            stroke_color="#333333", 
            stroke_width=35
        )
        
        # Crear logo simple con 'W'
        create_logo_simple(1024, 1024, font_size=700, bg_color="#4B89DC")  # Fondo azul oscuro
        print("Simple logo created and saved successfully.")
    except Exception as e:
        print(f"Error: {e}")
