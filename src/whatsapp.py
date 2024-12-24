import pyautogui
import os
import time
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
WAIT_TIME = int(os.getenv('WAIT_TIME', 5))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def open_whatsapp(numero):
    """
    Abre WhatsApp con el número indicado usando un enlace directo.

    :param numero: Número de teléfono al que enviar el mensaje.
    :raises RuntimeError: Si falla al abrir WhatsApp.
    """
    link = f'whatsapp://send?phone={numero}'
    logging.info(f"Abriendo WhatsApp para el número {numero}")
    resultado = os.system(f'start "" "{link}"')
    time.sleep(WAIT_TIME)

    if resultado != 0:
        logging.error(f"Error al abrir WhatsApp para el número {numero}")
        raise RuntimeError(f"No se pudo abrir WhatsApp para {numero}")

def close_whatsapp():
    print("Cerrando WhatsApp Desktop...")
    os.system("taskkill /IM WhatsApp.exe /F")

def go_to_insert_text(ntabs=11):
    """
    Navega por la interfaz de WhatsApp usando la tecla TAB para llegar al campo de texto.

    :param ntabs: Número de veces que se presiona la tecla TAB.
    """
    try:
        for i in range(ntabs):
            logging.info(f"Navegando por tabulador {i+1}/{ntabs}")
            pyautogui.press("tab", interval=0.1)
    except Exception as e:
        logging.error(f"Error durante la navegación por WhatsApp: {e}")
        raise RuntimeError("Error al navegar en WhatsApp.")

def send_mssg(numero, mensaje, ntabs=11):
    """
    Abre WhatsApp y envía un mensaje al número especificado.
    Si ocurre un error, se guarda inmediatamente en un archivo Excel y se envía una notificación de error.

    :param numero: Número de teléfono del destinatario.
    :param mensaje: Mensaje a enviar.
    :param ntabs: Número de pestañas para moverse hasta el campo de texto.
    """
    try:
        open_whatsapp(numero)
        go_to_insert_text(ntabs)
        pyautogui.write(mensaje)
        pyautogui.press("enter")
        logging.info(f"Mensaje enviado correctamente a {numero}")
        close_whatsapp()
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error al enviar mensaje a {numero}: {error_msg}")
        
        # Guardar error inmediatamente
        guardar_errores_excel(numero, mensaje, error_msg)
        
        # Notificar por WhatsApp
        my_phone = os.getenv('MY_PHONE')
        if my_phone:
            notificar_error_whatsapp(my_phone, f"Error con {numero}: {error_msg}")
        
        close_whatsapp()

def notificar_error_whatsapp(numero, error_msg):
    """
    Envía un mensaje de error a un número de teléfono cuando ocurre un fallo.

    :param numero: Número al que se enviará la notificación (MY_PHONE).
    :param error_msg: Mensaje de error a enviar.
    """
    try:
        open_whatsapp(numero)
        time.sleep(3)  # Esperar para asegurar que la ventana esté abierta
        pyautogui.write(f"🚨 whaSEN ERROR 🚨: {error_msg}")
        pyautogui.press("enter")
        logging.info(f"Notificación de error enviada a {numero}")
    except Exception as e:
        logging.error(f"No se pudo enviar notificación de error: {e}")

def guardar_errores_excel(numero, mensaje, error_msg):
    """
    Guarda un error en el archivo Excel 'casos_fallidos.xlsx' de inmediato.

    :param numero: Número de teléfono con fallo.
    :param mensaje: Mensaje que no se pudo enviar.
    :param error_msg: Descripción del error.
    """
    nuevo_error = pd.DataFrame([{
        "Telefono": numero,
        "Mensaje": mensaje,
        "Error": error_msg
    }])

    # Guardar directamente en el Excel
    if os.path.exists('casos_fallidos.xlsx'):
        df_existente = pd.read_excel('casos_fallidos.xlsx')
        nuevo_error = pd.concat([df_existente, nuevo_error], ignore_index=True)
    
    nuevo_error.to_excel('casos_fallidos.xlsx', index=False)
    logging.info(f"Error guardado en casos_fallidos.xlsx: {numero}")
