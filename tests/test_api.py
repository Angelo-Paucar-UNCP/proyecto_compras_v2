
import os
import sys

from fastapi.testclient import TestClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.api import app

client = TestClient(app)


def payload_valido():
    return {
        "Administrative": 0,
        "Administrative_Duration": 0.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": 10,
        "ProductRelated_Duration": 120.0,
        "BounceRates": 0.01,
        "ExitRates": 0.03,
        "PageValues": 12.5,
        "SpecialDay": 0.0,
        "Month": "Nov",
        "OperatingSystems": 2,
        "Browser": 2,
        "Region": 1,
        "TrafficType": 1,
        "VisitorType": "Returning_Visitor",
        "Weekend": False,
    }


def test_salud():
    response = client.get("/salud")
    assert response.status_code == 200

    data = response.json()
    assert data["estado"] == "OK"
    assert "modelo" in data
    assert data["modelo_cargado"] is True


def test_health_alternativo():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "activo"


def test_raiz():
    response = client.get("/")
    assert response.status_code == 200


def test_prediccion_predict_datos_planos():
    response = client.post("/predict", json=payload_valido())
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["prediccion"] in (0, 1)
    assert 0.0 <= data["probabilidad_compra"] <= 1.0
    assert "mensaje" in data


def test_prediccion_predecir_datos_anidados():
    response = client.post(
        "/predecir",
        json={"datos": payload_valido()},
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["prediccion"] in (0, 1)
    assert 0.0 <= data["probabilidad_compra"] <= 1.0
    assert "mensaje" in data


def test_prediccion_error_400_valor_invalido():
    payload = payload_valido()
    payload["ProductRelated"] = -5

    response = client.post("/predict", json=payload)
    assert response.status_code == 400, response.text


def test_prediccion_error_400_columnas_faltantes():
    response = client.post(
        "/predecir",
        json={"datos": {"ProductRelated": 5}},
    )
    assert response.status_code == 400, response.text


def test_prediccion_error_400_datos_no_objeto():
    response = client.post(
        "/predecir",
        json={"datos": "datos incorrectos"},
    )
    assert response.status_code == 400, response.text
