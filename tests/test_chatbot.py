
import requests

from src import chatbot


def test_deriva_despues_de_tres_intentos_invalidos(monkeypatch, capsys):
    respuestas = iter(["error", "error", "error"])
    monkeypatch.setattr(
        "builtins.input",
        lambda mensaje: next(respuestas),
    )

    resultado = chatbot.solicitar_dato(
        "Escribe un numero",
        chatbot.parsear_entero,
        "Respuesta invalida",
    )

    salida = capsys.readouterr().out

    assert resultado == "DERIVAR"
    assert salida.count("Respuesta invalida") == 3
    assert "DERIVAR" == resultado


def test_palabra_ayuda_deriva_a_persona(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda mensaje: "ayuda")

    resultado = chatbot.solicitar_dato(
        "Escribe un numero",
        chatbot.parsear_entero,
    )

    assert resultado == "DERIVAR"


def test_error_de_conexion_deriva_a_persona(
    monkeypatch,
    capsys,
):
    respuestas = iter(["nuevo", "5", "2", "no", "mayo"])
    monkeypatch.setattr(
        "builtins.input",
        lambda mensaje: next(respuestas),
    )
    monkeypatch.setattr(chatbot.time, "sleep", lambda segundos: None)

    def simular_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError(
            "Error simulado para la prueba"
        )

    monkeypatch.setattr(chatbot.requests, "post", simular_error)

    chatbot.iniciar_conversacion()
    salida = capsys.readouterr().out

    assert "No pude conectar con la API" in salida
    assert "TRANSFERENCIA A UN ASESOR HUMANO" in salida
