import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Agregamos la carpeta src/ al sistema para poder importar tus archivos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from datos import cargar_datos
from api import app
from chatbot import solicitar_dato

# Cliente de pruebas para simular peticiones web a la API sin encenderla
client = TestClient(app)

# 1. Prueba de Datos
def test_carga_datos_no_esta_vacio():
    df = cargar_datos()
    assert not df.empty, "El dataset no debería estar vacío"

# 2. Prueba de API
def test_api_health_check_responde_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "activo"

# 3. Prueba de Chatbot (Usa monkeypatch para simular que un usuario escribe)
def test_chatbot_deriva_a_humano_si_pide_ayuda(monkeypatch):
    # Simulamos que el usuario teclea "ayuda"
    monkeypatch.setattr('builtins.input', lambda _: 'ayuda')
    resultado = solicitar_dato("¿Cuántas páginas visitaste?")
    
    assert resultado == "DERIVAR", "El chatbot debe derivar si el usuario pide ayuda"