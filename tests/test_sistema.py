import pytest
from fastapi.testclient import TestClient
from src.api import app

def test_sistema_completo_integracion():
    """Verifica que el pipeline completo devuelva 200 con datos correctos."""
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
        resultado = respuesta.json()
        assert "prediccion" in resultado
        assert "probabilidad_compra" in resultado

def test_faltan_obligatorias():
    """Verifica que el sistema rechace peticiones incompletas."""
    with TestClient(app) as client:
        payload = {"datos": {"Month": "Nov"}}
        respuesta = client.post("/predecir", json=payload)
        assert respuesta.status_code == 422

def test_valor_invalido_tipo():
    """Verifica que el sistema rechace tipos de datos incorrectos."""
    with TestClient(app) as client:
        payload = {
            "datos": {
                "Administrative": "texto_invalido", 
                "Administrative_Duration": 15.5, "Informational": 0,
                "Informational_Duration": 0.0, "ProductRelated": 12, "ProductRelated_Duration": 150.2,
                "BounceRates": 0.01, "ExitRates": 0.02, "PageValues": 10.5, "SpecialDay": 0.0,
                "Month": "Nov", "OperatingSystems": 2, "Browser": 2, "Region": 1,
                "TrafficType": 2, "VisitorType": "Returning_Visitor", "Weekend": True
            }
        }
        respuesta = client.post("/predecir", json=payload)
        assert respuesta.status_code == 422