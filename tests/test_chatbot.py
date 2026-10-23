import pytest
from unittest.mock import patch
import requests
from src.chatbot import evaluar_cliente

@patch('builtins.input', side_effect=['invalido', 'invalido', 'invalido'])
def test_deriva_despues_de_tres_intentos_invalidos(mock_input, capsys):
    """Prueba que el fallback aborte tras 3 errores."""
    evaluar_cliente()
    captured = capsys.readouterr()
    assert "Demasiados errores. Abortando evaluación actual." in captured.out

@patch('builtins.input', side_effect=['ayuda'])
def test_palabra_ayuda_cancela_proceso(mock_input, capsys):
    """Prueba el camino alternativo donde el vendedor cancela."""
    evaluar_cliente()
    # Si ingresa "ayuda", la función evalúa cliente retorna silenciosamente (CANCELAR)
    # Por lo tanto, no debería llegar al mensaje de la API.
    captured = capsys.readouterr()
    assert "Consultando al modelo predictivo..." not in captured.out

@patch('builtins.input', side_effect=['1', '5', '10', 'mayo'])
@patch('requests.post')
def test_error_de_conexion_api(mock_post, mock_input, capsys):
    """Prueba el camino de error cuando la API de FastAPI está caída."""
    mock_post.side_effect = requests.exceptions.RequestException("Error de red")
    evaluar_cliente()
    captured = capsys.readouterr()
    assert "Servidor API inalcanzable" in captured.out