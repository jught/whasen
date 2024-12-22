import pyautogui
import pyperclip
import os
import time

def open_whatsapp(numero):
    link = f'whatsapp://send?phone={numero}'
    print(f"\nEnviando mensaje a {numero}...")
    print(f"Enlace generado: {link}")
    resultado = os.system(f'start "" "{link}"')
    if resultado != 0:
       print(f"Error al abrir WhatsApp para el número {numero}.")

def go_to_insert_text(ntabs = 11):
    for i in range(ntabs):
        print(f"tab {i+1}/{ntabs}")
        pyautogui.press("tab", interval=0.1)
    time.sleep(1)

def insert_msg(mssg):
    pyperclip.copy(mssg)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)
    pyautogui.press("enter")

def close_whatsapp():
    print("Cerrando WhatsApp Desktop...")
    os.system("taskkill /IM WhatsApp.exe /F")

def enviar_mensaje(numero, mensaje, ntabs = 11):
    open_whatsapp(numero)
    print("Esperando que se abra WhatsApp...")
    time.sleep(2)
    go_to_insert_text(ntabs)
    insert_msg(mensaje)
    time.sleep(1)
    #close_whatsapp()
    print("Mensaje enviado correctamente.\n")
