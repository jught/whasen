import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def leer_excel(file_path=None):
    """
    Lee un archivo Excel. Si no se proporciona un archivo, usa el de la configuración (.env).

    :param file_path: Ruta opcional al archivo Excel.
    :return: DataFrame de pandas o None si falla.
    """
    path = file_path or EXCEL_FILE_PATH
    try:
        logging.info(f"Leyendo archivo Excel: {path}")
        return pd.read_excel(path)
    except Exception as e:
        logging.error(f"Error al leer el archivo Excel: {e}")
        return None
