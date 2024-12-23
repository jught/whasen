import sys
import pandas as pd
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Guarda en app.log
        logging.StreamHandler()           # Muestra en consola
    ]
)

def leer_excel(file_path):
    try:
        logging.info(f"Reading Excel file: {file_path}")
        return pd.read_excel(file_path)
    except Exception as e:
        logging.error(f"Failed to read Excel file: {e}")
        return None
    
# Bloque para testear utils.py de forma independiente
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        df = leer_excel(file_path)
        if df is not None:
            logging.info("Excel file loaded successfully!")
            print(df.head())  # Muestra las primeras filas
        else:
            logging.error("Failed to load Excel file.")
    else:
        logging.error("Please provide an Excel file path.")
