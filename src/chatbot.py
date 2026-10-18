import json
import time

import requests

try:
    from .rutas import RUTA_DEFAULTS
except ImportError:
    from rutas import RUTA_DEFAULTS

API_URL = "http://127.0.0.1:8000/predecir"

MESES_ES = {
    "febrero": "Feb",
    "marzo": "Mar",
    "mayo": "May",
    "junio": "June",
    "julio": "Jul",
    "agosto": "Aug",
    "septiembre": "Sep",
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
        with open(RUTA_DEFAULTS, encoding="utf-8") as f:
            return json.load(f)
    return {
        "Administrative": 0,
        "Administrative_Duration": 0,
        "Informational": 0,
        "Informational_Duration": 0,
        "ProductRelated": 1,
        "ProductRelated_Duration": 0,
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


def solicitar_dato(mensaje, parsear, fallback="No entendí eso. Prueba de nuevo, por favor."):
    intentos = 0
    while intentos < 3:
        entrada = input(f"🤖 Asistente: {mensaje}\n👤 Tú: ")
        if entrada.strip().lower() in {"ayuda", "humano", "asesor", "salir"}:
            return "DERIVAR"
        try:
            return parsear(entrada)
        except (ValueError, TypeError):
            print(f"🤖 Asistente: {fallback}")
            intentos += 1
    print("🤖 Asistente: Mejor te paso con una persona de la tienda.")
    return "DERIVAR"


def parsear_entero(texto):
    valor = int(texto.strip())
    if valor < 0:
        raise ValueError("negativo")
    return valor


def parsear_minutos(texto):
    valor = float(texto.strip().replace(",", "."))
    if valor < 0:
        raise ValueError("negativo")
    return valor


def parsear_visitante(texto):
    t = texto.strip().lower()
    if t in {"nuevo", "nueva", "new", "1"}:
        return "New_Visitor"
    if t in {"recurrente", "antiguo", "returning", "2"}:
        return "Returning_Visitor"
    if t in {"otro", "other", "3"}:
        return "Other"
    raise ValueError("visitante")


def parsear_si_no(texto):
    t = texto.strip().lower()
    if t in {"si", "sí", "yes", "true", "1"}:
        return True
    if t in {"no", "false", "0"}:
        return False
    raise ValueError("bool")


def parsear_mes(texto):
    clave = texto.strip().lower()
    if clave not in MESES_ES:
        raise ValueError("mes")
    return MESES_ES[clave]


def derivar_a_humano():
    print("\n" + "-" * 50)
    print("📞 TRANSFIRIENDO A UN ASESOR HUMANO...")
    print("Asesor: Hola, soy del equipo de ventas. ¿En qué te ayudo?")
    print("-" * 50 + "\n")


def iniciar_conversacion():
    print("\n" + "=" * 50)
    print("🤖 Asistente: Hola, soy el asistente de la tienda.")
    print("🤖 Asistente: Te haré unas preguntas cortas para ver si te conviene un apoyo.")
    print("🤖 Asistente: Escribe 'ayuda' si quieres hablar con una persona.")
    print("=" * 50 + "\n")

    visitante = solicitar_dato(
        "¿Es tu primera visita o ya has comprado antes? (nuevo / recurrente)",
        parsear_visitante,
        "Responde 'nuevo' o 'recurrente'.",
    )
    if visitante == "DERIVAR":
        return derivar_a_humano()

    paginas = solicitar_dato(
        "¿Cuántas páginas de productos has abierto hoy?",
        parsear_entero,
        "Necesito un número entero, por ejemplo 8.",
    )
    if paginas == "DERIVAR":
        return derivar_a_humano()

    minutos = solicitar_dato(
        "¿Cuántos minutos llevas en la web, más o menos?",
        parsear_minutos,
        "Necesito un número, por ejemplo 12.",
    )
    if minutos == "DERIVAR":
        return derivar_a_humano()

    weekend = solicitar_dato(
        "¿Estás navegando en fin de semana? (sí / no)",
        parsear_si_no,
        "Responde sí o no.",
    )
    if weekend == "DERIVAR":
        return derivar_a_humano()

    mes = solicitar_dato(
        "¿En qué mes estás? (marzo, mayo, noviembre...)",
        parsear_mes,
        "Dime el mes en palabras, por ejemplo noviembre.",
    )
    if mes == "DERIVAR":
        return derivar_a_humano()

    datos_cliente = cargar_defaults()
    datos_cliente.update(
        {
            "VisitorType": visitante,
            "ProductRelated": paginas,
            "ProductRelated_Duration": float(minutos) * 60.0,
            "Weekend": weekend,
            "Month": mes,
        }
    )

    print("\n🤖 Asistente: Un segundo, estoy revisando tu sesión...")
    time.sleep(1)

    try:
        respuesta = requests.post(API_URL, json={"datos": datos_cliente}, timeout=10)
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            if resultado["prediccion"] == 0:
                print(
                    "🤖 Asistente: Veo que todavía estás comparando. "
                    "Puedo ofrecerte un cupón del 15% si cierras tu compra hoy."
                )
                print("🤖 Asistente: Si quieres, te paso con un asesor para aplicarlo.")
                derivar_a_humano()
            else:
                print(
                    "🤖 Asistente: Tus productos se ven bien encaminados. "
                    "¿Te acompaño a la caja?"
                )
        elif respuesta.status_code == 400:
            print("🤖 Asistente: Algún dato no me cuadró. Te paso con un asesor.")
            derivar_a_humano()
        else:
            print("🤖 Asistente: El sistema está lento. Te comunico con una persona.")
            derivar_a_humano()
    except requests.exceptions.RequestException:
        print("🤖 Asistente: No pude conectar con el sistema. Te paso con un humano.")
        derivar_a_humano()


if __name__ == "__main__":
    iniciar_conversacion()
