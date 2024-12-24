import pytest
import os
from src.whatsapp import open_whatsapp
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()
MY_PHONE = os.getenv('MY_PHONE')


def test_open_whatsapp_success():
    """
    Prueba que WhatsApp se abre correctamente con un número válido.
    - Se usa el número de teléfono almacenado en .env (MY_PHONE).
    """
    if MY_PHONE:
        resultado = open_whatsapp(MY_PHONE)
        assert resultado is None, "No se debería devolver error al abrir WhatsApp"
    else:
        pytest.skip("No se encontró MY_PHONE en .env")


def test_open_whatsapp_fail():
    """
    Verifica que se maneje correctamente un fallo al abrir WhatsApp.
    - Se usa un número inválido para forzar el error.
    """
    with pytest.raises(RuntimeError):
        open_whatsapp("000000000")  # Número inválido que debería fallar
