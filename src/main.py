import pyautogui
import pyperclip
import time
import pandas as pd
import urllib.parse
import os

def open_whatsapp(numero):
    # Crear el enlace usando whatsapp://
    link = f'whatsapp://send?phone={numero}'
    print(f"\nEnviando mensaje a {numero}...")
    print(f"Enlace generado: {link}")
    
    # Abrir el enlace correctamente con comillas dobles
    resultado = os.system(f'start "" "{link}"')
    print(f"Resultado de abrir enlace: {resultado}")
    # Verificar si el enlace se abrió correctamente
    if resultado != 0:
       print(f"Error al abrir WhatsApp para el número {numero}.")

def go_to_insert_text():
    for i in range(11):
        pyautogui.press("tab", interval=0.1)

def close_whatsapp():
    print("Cerrando WhatsApp Desktop...")
    os.system("taskkill /IM WhatsApp.exe /F")
def insert_msg(msg):
    pyperclip.copy(msg)  # Copia el mensaje al portapapeles
    pyautogui.hotkey("ctrl", "v")  # Pega el mensaje con Ctrl + V)
    pyautogui.press("enter")

def enviar_mensaje(numero, mensaje):
    # Crear el enlace usando whatsapp://
    open_whatsapp(numero)

    # Esperar que se abra WhatsApp
    print("Esperando que se abra WhatsApp...")
    time.sleep(5)

    go_to_insert_text()
    print(mensaje)
    insert_msg(mensaje)
    
    time.sleep(1)
	
    close_whatsapp()
    
    # Esperar un poco antes de pasar al siguiente
    time.sleep(3)
    print("Mensaje enviado correctamente.")


def main(excel_file = "pruebaExcel_macu.xlsm"):
    # Leer el archivo Excel
    df = pd.read_excel(excel_file)

    print("Iniciando envío de mensajes...")

    # Iterar sobre los contactos y enviar mensajes
    for index, row in df.iterrows():
        numero = str(row['Telefono'])
        mensaje = row['Mensaje']
        enviar_mensaje(numero, mensaje)    

    print("\nProceso completado.")

if _name_ == '_main_':
    import sys
    file = None
    if len(sys.argv) >= 2:
        file = sys.argv[1]
    main(file)