from whatsapp import enviar_mensaje
from utils import leer_excel
import sys

def main(excel_file="mssgs.xlsx", ntabs = 11):
    df = leer_excel(excel_file)
    if df is None:
        print("No se pudo cargar el archivo Excel.")
        return

    print("Iniciando envío de mensajes...")
    for _, row in df.iterrows():
        numero = str(row['Telefono'])
        mensaje = row['Mensaje']
        enviar_mensaje(numero, mensaje, ntabs)

    print("\nProceso completado.")

import sys
import os

def obtener_argumentos():
    ntabs = 11  # Valor por defecto
    file = "./mssgs.xlsx"  # Archivo por defecto

    # Si hay argumentos
    if len(sys.argv) > 1:
        args = sys.argv[1:]  # Obtener los argumentos (excluyendo el nombre del script)

        # Identificar cuál es el número de pestañas (entero) y cuál es el archivo
        for arg in args:
            if arg.isdigit():
                ntabs = int(arg)  # Asignar el valor como entero
            elif os.path.exists(arg):
                file = arg  # Asignar el archivo si existe en el sistema

    return ntabs, file


# Ejemplo de uso
if __name__ == "__main__":
    ntabs, file = obtener_argumentos()
    print(f"Número de pestañas: {ntabs}")
    print(f"Archivo: {file}")
    main(file, ntabs)
