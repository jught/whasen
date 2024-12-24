from whatsapp import open_whatsapp, send_mssg
from utils import leer_excel
import logging
import sys
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Asegurar que EXCEL_FILE_PATH sea relativo al script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, os.getenv('EXCEL_FILE_PATH', 'mssgs.xlsm'))
TABS = int(os.getenv('TABS', 10))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def obtener_argumentos():
    """
    Obtiene argumentos de línea de comandos (pestañas y archivo Excel).
    Usa valores por defecto desde .env si no se pasan argumentos.

    :return: (ntabs, file) - Número de pestañas y ruta del archivo Excel.
    """
    ntabs = int(sys.argv[1]) if len(sys.argv) > 1 else TABS
    file = sys.argv[2] if len(sys.argv) > 2 else EXCEL_FILE_PATH
    return ntabs, file


def main(excel_file, ntabs):
    """
    Función principal que lee un archivo Excel y envía mensajes por WhatsApp.

    :param excel_file: Ruta al archivo Excel.
    :param ntabs: Número de pestañas para navegación.
    """
    try:
        df = leer_excel(excel_file)
        if df is None:
            logging.error("No se pudo cargar el archivo Excel.")
            return

        logging.info("Iniciando el envío de mensajes...")
        for _, row in df.iterrows():
            numero = str(row['Telefono'])
            mensaje = row['Mensaje']

            if not numero.isdigit():
                logging.warning(f"Número inválido: {numero}. Saltando.")
                continue
            open_whatsapp(numero)
            send_mssg(numero, mensaje, ntabs)
            logging.info(f"Mensaje enviado a {numero}: {mensaje}")

        logging.info("Proceso completado.")
    
    except Exception as e:
        logging.critical(f"Error crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    ntabs, file = obtener_argumentos()
    print(f"Número de pestañas: {ntabs}")
    print(f"Archivo: {file}")
    main(file, ntabs)

