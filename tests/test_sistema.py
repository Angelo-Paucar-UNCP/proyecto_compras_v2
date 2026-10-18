import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from api import app
from chatbot import parsear_mes, parsear_visitante, solicitar_dato
from datos import cargar_datos
from preprocesamiento_api import ErrorValidacion, validar_entrada

client = TestClient(app)

SESION_VALIDA = {
    "Administrative": 0,
    "Administrative_Duration": 0,
    "Informational": 0,
    "Informational_Duration": 0,
    "ProductRelated": 10,
    "ProductRelated_Duration": 600,
    "BounceRates": 0.01,
    "ExitRates": 0.04,
    "PageValues": 0,
    "SpecialDay": 0,
    "Month": "Nov",
    "OperatingSystems": 2,
    "Browser": 2,
    "Region": 1,
    "TrafficType": 2,
    "VisitorType": "Returning_Visitor",
    "Weekend": False,
}


def test_carga_datos_no_esta_vacio():
    df = cargar_datos()
    assert not df.empty
    assert "Revenue" in df.columns


def test_api_health_check_responde_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "activo"


def test_api_rechaza_entrada_incompleta():
    response = client.post("/predecir", json={"datos": {"ProductRelated": 3}})
    assert response.status_code == 400
    assert "Faltan campos" in response.json()["detail"]


def test_api_rechaza_mes_invalido():
    datos = dict(SESION_VALIDA)
    datos["Month"] = "Enero"
    response = client.post("/predecir", json={"datos": datos})
    assert response.status_code == 400


def test_validar_entrada_ok():
    df = validar_entrada(SESION_VALIDA)
    assert df.shape == (1, 17)


def test_validar_entrada_rango():
    datos = dict(SESION_VALIDA)
    datos["BounceRates"] = 2
    try:
        validar_entrada(datos)
        assert False, "debía fallar"
    except ErrorValidacion:
        pass


def test_chatbot_deriva_a_humano_si_pide_ayuda(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "ayuda")
    resultado = solicitar_dato("¿Cuántas páginas visitaste?", int)
    assert resultado == "DERIVAR"


def test_chatbot_parsea_visitante_y_mes():
    assert parsear_visitante("nuevo") == "New_Visitor"
    assert parsear_mes("noviembre") == "Nov"
