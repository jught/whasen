import json
from dotenv import load_dotenv
import os

load_dotenv()

TEMPLATE_PATH = './app/templates/mensajes.plantilla'

def generar_mensaje(datos):
    """
    Genera un mensaje usando datos de entrada y una plantilla JSON.
    :param datos: Diccionario con las variables {nombre, telefono, etc.}
    :return: Mensaje generado
    """
    try:
        with open(TEMPLATE_PATH, 'r') as f:
            plantilla = json.load(f)
        
        mensaje = plantilla["plantilla"]
        for var in plantilla["variables"]:
            valor = datos.get(var.strip("<>"), "")
            mensaje = mensaje.replace(var, valor)

        return mensaje
    except Exception as e:
        return f"Error generando mensaje: {e}"
