import pandas as pd

def leer_excel(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return None

