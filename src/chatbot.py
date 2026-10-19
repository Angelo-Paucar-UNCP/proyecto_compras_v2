import json
import time

import requests

try:
    from .rutas import RUTA_DEFAULTS
except ImportError:
    from rutas import RUTA_DEFAULTS


API_URL = "http://127.0.0.1:8001/predecir"

MESES_ES = {
    "enero": "Feb",
    "febrero": "Feb",
    "marzo": "Mar",
    "abril": "May",
    "mayo": "May",
    "junio": "June",
    "julio": "Jul",
    "agosto": "Aug",
    "septiembre": "Sep",
    "setiembre": "Sep",
    "octubre": "Oct",
    "noviembre": "Nov",
    "diciembre": "Dec",
    "feb": "Feb",
    "mar": "Mar",
    "may": "May",
    "june": "June",
    "jun": "June",
    "jul": "Jul",
    "aug": "Aug",
    "ago": "Aug",
    "sep": "Sep",
    "oct": "Oct",
    "nov": "Nov",
    "dec": "Dec",
    "dic": "Dec",
}


def cargar_defaults():
    if RUTA_DEFAULTS.exists():
        with open(RUTA_DEFAULTS, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        datos["Weekend"] = (
            datos.get("Weekend", False) is True
            or datos.get("Weekend", False) == 1
        )
        return datos

    return {
        "Administrative": 0,
        "Administrative_Duration": 0.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": 1,
        "ProductRelated_Duration": 0.0,
        "BounceRates": 0.0,
        "ExitRates": 0.04,
        "PageValues": 0.0,
        "SpecialDay": 0.0,
        "Month": "May",
        "OperatingSystems": 2,
        "Browser": 2,
        "Region": 1,
        "TrafficType": 2,
        "VisitorType": "Returning_Visitor",
        "Weekend": False,
    }


def solicitar_dato(mensaje, parsear, fallback="No entendí eso. Prueba de nuevo."):
    intentos = 0

    while intentos < 3:
        entrada = input(f"🤖 Asistente: {mensaje}\n👤 Tú: ")

        if entrada.strip().lower() in {
            "ayuda", "humano", "asesor", "salir"
        }:
            return "DERIVAR"

        try:
            return parsear(entrada)
        except (ValueError, TypeError):
            print(f"⚠️ Asistente: {fallback}")
            intentos += 1

    print("🙋 Asistente: Te comunicaré con una persona de la tienda.")
    return "DERIVAR"


def parsear_entero(texto):
    valor = int(texto.strip())

    if valor < 0:
        raise ValueError("El valor no puede ser negativo.")

    return valor


def parsear_minutos(texto):
    valor = float(texto.strip().replace(",", "."))

    if valor < 0:
        raise ValueError("El valor no puede ser negativo.")

    return valor


def parsear_visitante(texto):
    texto = texto.strip().lower()

    if texto in {"nuevo", "nueva", "new", "1"}:
        return "New_Visitor"

    if texto in {"recurrente", "antiguo", "returning", "2"}:
        return "Returning_Visitor"

    if texto in {"otro", "other", "3"}:
        return "Other"

    raise ValueError("Tipo de visitante inválido.")


def parsear_mes(texto):
    clave = texto.strip().lower()

    if clave not in MESES_ES:
        raise ValueError("Mes no reconocido.")

    return MESES_ES[clave]


def derivar_a_humano():
    print("\n" + "─" * 50)
    print("🙋 TRANSFERENCIA A UN ASESOR HUMANO")
    print("🗣️ Asesor: ¡Hola! 😊 ¿En qué te puedo ayudar?")
    print("─" * 50 + "\n")


def iniciar_conversacion():
    print("\n" + "═" * 50)
    print("🛍️ ¡Hola! Soy el asistente virtual de la tienda.")
    print("😊 Te haré unas preguntas breves sobre tu visita.")
    print("💡 Escribe 'ayuda' si deseas hablar con una persona.")
    print("═" * 50 + "\n")

    visitante = solicitar_dato(
        "👋 ¿Es tu primera visita o ya has comprado antes? "
        "(nuevo / recurrente)",
        parsear_visitante,
        "Escribe 'nuevo', 'recurrente' u otra opción válida.",
    )
    if visitante == "DERIVAR":
        return derivar_a_humano()

    paginas = solicitar_dato(
        "📄 ¿Cuántas páginas de productos has abierto?",
        parsear_entero,
        "Escribe un número entero, por ejemplo 8.",
    )
    if paginas == "DERIVAR":
        return derivar_a_humano()

    minutos = solicitar_dato(
        "⏱️ ¿Cuántos minutos llevas en la web?",
        parsear_minutos,
        "Escribe un número, por ejemplo 12.",
    )
    if minutos == "DERIVAR":
        return derivar_a_humano()

    mes = solicitar_dato(
        "📅 ¿En qué mes estás? (marzo, mayo, noviembre...)",
        parsear_mes,
        "Escribe un mes reconocido, por ejemplo mayo.",
    )
    if mes == "DERIVAR":
        return derivar_a_humano()

    datos_cliente = cargar_defaults()
    datos_cliente.update({
        "VisitorType": visitante,
        "ProductRelated": paginas,
        "ProductRelated_Duration": minutos * 60.0,
        "Month": mes,
    })

    print("\n🔎 Asistente: Estoy analizando tu visita...")
    time.sleep(1)

    try:
        respuesta = requests.post(
            API_URL,
            json={"datos": datos_cliente},
            timeout=10,
        )

        if respuesta.status_code == 200:
            resultado = respuesta.json()
            prediccion = resultado.get("prediccion")

            if prediccion == 0:
                print("\n📉 Asistente: La intención de compra estimada es baja.")
                print("🎁 Puedes consultar nuestras promociones.")
                print("🙋 Si lo prefieres, puedes hablar con un asesor.")

            elif prediccion == 1:
                print("\n🛒 Asistente: ¡La intención de compra estimada es alta!")
                print("😊 ¿Te gustaría continuar con tu compra?")

            else:
                print("⚠️ Asistente: La respuesta del modelo no es válida.")
                derivar_a_humano()
                return

            if "probabilidad_compra" in resultado:
                probabilidad = resultado["probabilidad_compra"]
                print(
                    f"📊 Probabilidad estimada de compra: "
                    f"{probabilidad:.2%}"
                )

            print("\n✨ ¡Gracias por visitar nuestra tienda!")

        elif respuesta.status_code == 400:
            print("⚠️ Asistente: Los datos enviados no son válidos.")
            print("Detalle:", respuesta.text)
            derivar_a_humano()

        else:
            print(
                f"⚠️ Asistente: El sistema respondió con HTTP "
                f"{respuesta.status_code}."
            )
            print("Detalle:", respuesta.text)
            derivar_a_humano()

    except requests.exceptions.RequestException as error:
        print("❌ Asistente: No pude conectar con la API.")
        print("Detalle:", error)
        derivar_a_humano()

    except (ValueError, TypeError) as error:
        print("❌ Asistente: La respuesta de la API no es válida.")
        print("Detalle:", error)
        derivar_a_humano()


if __name__ == "__main__":
    iniciar_conversacion()
