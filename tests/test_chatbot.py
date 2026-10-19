import pytest
from unittest.mock import patch
import requests
from src.chatbot import iniciar_conversacion

@patch('builtins.input', side_effect=['texto uno', 'texto dos', 'texto tres'])
def test_deriva_despues_de_tres_intentos_invalidos(mock_input, capsys):
    """Prueba que el fallback actúe tras 3 errores de tipeo y derive a humano."""
    iniciar_conversacion()
    captured = capsys.readouterr()
    assert "TRANSFIRIENDO A UN ASESOR HUMANO EN VIVO" in captured.out
    assert "Parece que estamos teniendo problemas de comunicación" in captured.out

@patch('builtins.input', side_effect=['ayuda'])
def test_palabra_ayuda_deriva_a_persona(mock_input, capsys):
    """Prueba el camino alternativo donde el usuario pide ayuda en el primer turno."""
    iniciar_conversacion()
    captured = capsys.readouterr()
    assert "TRANSFIRIENDO A UN ASESOR HUMANO EN VIVO" in captured.out

@patch('builtins.input', side_effect=['5', '10'])
@patch('requests.post')
def test_error_de_conexion_deriva_a_persona(mock_post, mock_input, capsys):
    """Prueba el camino de error cuando la API de FastAPI está caída."""
    # Simulamos una caída del servidor
    mock_post.side_effect = requests.exceptions.RequestException("Error de red")
    
    iniciar_conversacion()
    captured = capsys.readouterr()
    
    assert "Ocurrió un inconveniente al conectar con el servidor interno" in captured.out
    assert "TRANSFIRIENDO A UN ASESOR HUMANO EN VIVO" in captured.out