import sys
import os
import pytest

# Añade la raíz del proyecto al PATH de Python para poder importar desde src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocesamiento_api import preparar_datos_entrada

def test_preparar_datos_validos():
    """Verifica que un diccionario válido genere un DataFrame estructurado de 1 fila."""
    datos = {
        "ProductRelated": 10,
        "ProductRelated_Duration": 120.0,
        "Month": "May"
    }
    df = preparar_datos_entrada(datos)
    assert len(df) == 1
    assert "Administrative" in df.columns
    assert "ProductRelated" in df.columns

def test_faltan_obligatorias():
    """Verifica que lance ValueError si faltan columnas obligatorias."""
    datos_incompletos = {
        "Month": "May"
    }
    with pytest.raises(ValueError):
        preparar_datos_entrada(datos_incompletos)

def test_valor_invalido_tasa():
    """Verifica que lance ValueError si una tasa excede el rango permitido (0 a 1)."""
    datos_invalidos = {
        "ProductRelated": 5,
        "ProductRelated_Duration": 50.0,
        "ExitRates": 2.5  # Tasa fuera de rango (> 1)
    }
    with pytest.raises(ValueError):
        preparar_datos_entrada(datos_invalidos)

def test_numero_negativo():
    """Verifica que lance ValueError si hay duraciones o valores negativos."""
    datos_negativos = {
        "ProductRelated": -5,
        "ProductRelated_Duration": 100.0
    }
    with pytest.raises(ValueError):
        preparar_datos_entrada(datos_negativos)

def test_mes_invalido():
    """Verifica que lance ValueError si el mes no pertenece a la lista válida."""
    datos_mes = {
        "ProductRelated": 10,
        "ProductRelated_Duration": 120.0,
        "Month": "Enero"  # Mes no permitido
    }
    with pytest.raises(ValueError):
        preparar_datos_entrada(datos_mes)
