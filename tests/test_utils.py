import pytest
import pandas as pd
from src.utils import leer_excel

@pytest.fixture
def sample_excel(tmpdir):
    """
    Crea un archivo Excel temporal con datos de prueba para verificar:
    - Lectura de acentos y caracteres especiales.
    - Saltos de línea dentro de celdas.
    - Detección de celdas vacías en la columna 'Telefono'.
    """
    file_path = tmpdir.join("test.xlsx")
    data = {
        'Telefono': ['123456789', '987654321', ''],  # Última fila sin teléfono
        'Mensaje': [
            'Hola, ¿cómo estás?\nEspero que bien.',   # Salto de línea
            'Feliz cumpleaños, disfruta tu día.',
            'Mensaje sin número'
        ],
        'Nombre': ['José Álvarez', 'María Niño', 'Sofía López']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return file_path


def test_leer_excel_ok(sample_excel):
    """
    Verifica que el archivo Excel se lea correctamente:
    - Se mantienen los acentos y caracteres especiales.
    - Los saltos de línea se conservan.
    - La columna 'Telefono' tiene valores correctos (excepto el vacío).
    """
    df = leer_excel(sample_excel)
    assert df is not None
    assert len(df) == 3
    assert df['Nombre'].iloc[0] == 'José Álvarez'  # Acentos
    assert '¿cómo estás?' in df['Mensaje'].iloc[0]  # Caracteres especiales
    assert '\n' in df['Mensaje'].iloc[0]            # Salto de línea


def test_leer_excel_fail_on_empty_phone(sample_excel):
    """
    Prueba que el programa falle si hay teléfonos vacíos o no numéricos:
    - Se recorre el DataFrame en busca de celdas vacías o incorrectas.
    - Si se encuentra un teléfono vacío, lanza ValueError.
    """
    with pytest.raises(ValueError):
        df = leer_excel(sample_excel)
        for index, row in df.iterrows():
            if not row['Telefono'].isdigit():
                raise ValueError(f"Fila {index+1} tiene teléfono inválido: {row['Telefono']}")
