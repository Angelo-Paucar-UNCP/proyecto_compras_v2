import os
import sys
from fastapi.testclient import TestClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.api import app

client = TestClient(app)

def test_salud():
    response = client.get("/salud")
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "OK"
    assert "modelo" in data

def test_prediccion_exitosa_incompleta():
    payload = {
        "ProductRelated": 10,
        "ProductRelated_Duration": 120.0,
        "BounceRates": 0.01,
        "ExitRates": 0.03,
        "PageValues": 12.5,
        "SpecialDay": 0.0,
        "Month": "Nov",
        "VisitorType": "Returning_Visitor",
        "Weekend": False
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, f"Fallo /predict ({response.status_code}): {response.json()}"
    data = response.json()
    assert "prediccion" in data
    assert "probabilidad_compra" in data
    assert 0.0 <= data["probabilidad_compra"] <= 1.0

def test_prediccion_error_400_valor_invalido():
    payload_invalido = {
        "ProductRelated": -5,
        "ProductRelated_Duration": 120.0,
        "Month": "MesInexistente"
    }
    response = client.post("/predict", json=payload_invalido)
    assert response.status_code == 400, f"Se esperaba 400 pero se obtuvo {response.status_code}: {response.json()}"
