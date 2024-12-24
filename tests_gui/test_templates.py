import pytest
from app.templates import generar_mensaje

def test_generar_mensaje():
    datos = {"nombre": "Carlos", "telefono": "123456789"}
    resultado = generar_mensaje(datos)
    assert "Bienvenido al sistema, Carlos" in resultado
    assert "123456789" in resultado
