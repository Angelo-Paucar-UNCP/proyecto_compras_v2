import pytest
from fastapi.testclient import TestClient
from src.api import app

def test_health_check():
    """Verifica que el endpoint de monitoreo funcione y cargue el modelo."""
    # Usar 'with' obliga a FastAPI a ejecutar el evento de 'startup' y cargar los modelos
    with TestClient(app) as client:
        respuesta = client.get("/health")
        assert respuesta.status_code == 200
        assert respuesta.json()["status"] == "ok"
        assert respuesta.json()["modelo_cargado"] is True

def test_prediccion_exitosa():
    """Verifica una predicción exitosa con datos correctos."""
    with TestClient(app) as client:
        payload = {
            "datos": {
                "Administrative": 3, "Administrative_Duration": 15.5, "Informational": 0,
                "Informational_Duration": 0.0, "ProductRelated": 12, "ProductRelated_Duration": 150.2,
                "BounceRates": 0.01, "ExitRates": 0.02, "PageValues": 10.5, "SpecialDay": 0.0,
                "Month": "Nov", "OperatingSystems": 2, "Browser": 2, "Region": 1,
                "TrafficType": 2, "VisitorType": "Returning_Visitor", "Weekend": True
            }
        }
        respuesta = client.post("/predecir", json=payload)
        assert respuesta.status_code == 200
        assert "prediccion" in respuesta.json()
        assert "probabilidad_compra" in respuesta.json()

def test_prediccion_error_422_columnas_faltantes():
    """FastAPI debe devolver 422 Unprocessable Entity si faltan datos del esquema."""
    with TestClient(app) as client:
        payload = {"datos": {"Month": "Nov"}} # Faltan casi todos los campos
        respuesta = client.post("/predecir", json=payload)
        assert respuesta.status_code == 422