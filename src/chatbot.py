
import json
import time

import requests

<<<<<<< HEAD
def solicitar_dato(mensaje, tipo_esperado=int, fallback="Disculpa, no entendí eso. ¿Podrías ingresar solo un número válido?"):
    """
    Recolecta datos paso a paso (slots) con validación de entradas 
    y límite de reintentos (fallback).
    """
    intentos = 0
    while intentos < 3:
        entrada = input(f"🤖 Asistente: {mensaje}\n👤 Tú: ")
        
        # Opción de salida o derivación humana directa
        if entrada.strip().lower() in ['ayuda', 'humano', 'asesor', 'salir']:
            return "DERIVAR"
            
        try:
            valor = tipo_esperado(entrada)
            return valor
        except ValueError:
            print(f"🤖 Asistente: {fallback}")
            intentos += 1
            
    print("\n🤖 Asistente: Parece que estamos teniendo problemas de comunicación. Te transferiré con un asesor humano para ayudarte mejor.")
    return "DERIVAR"

def derivar_a_humano():
    """Simula la transferencia a un operador de soporte humano."""
    print("\n" + "-"*60)
    print("📞 TRANSFIRIENDO A UN ASESOR HUMANO EN VIVO...")
    print("👩🏽‍💻 Asesor real: ¡Hola! Soy el asesor de ventas. ¿En qué te puedo colaborar hoy?")
    print("-" * 60 + "\n")

def iniciar_conversacion():
    print("\n" + "="*60)
    print("🤖 Asistente: ¡Hola! Bienvenid@ a nuestra tienda virtual.")
    print("🤖 Asistente: Estoy aquí para ayudarte en tu compra.")
    print("🤖 Asistente: (Recuerda que puedes escribir 'ayuda' en cualquier momento).")
    print("="*60 + "\n")
    
    # 1. Recolección de datos por pasos (Slots)
    paginas_vistas = solicitar_dato("¿Cuántas páginas de productos has visitado hoy?")
    if paginas_vistas == "DERIVAR":
        derivar_a_humano()
        return
        
    minutos = solicitar_dato("¿Aproximadamente cuántos minutos llevas navegando en nuestro sitio?", tipo_esperado=float)
    if minutos == "DERIVAR":
        derivar_a_humano()
        return
    
    # 2. Estructura de datos alineada al preprocesador y modelo entrenado (UCI Shoppers)
    datos_cliente = {
=======
try:
    from .rutas import RUTA_DEFAULTS
except ImportError:
    from rutas import RUTA_DEFAULTS


API_URL = "http://127.0.0.1:8001/predecir"

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
        with open(RUTA_DEFAULTS, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Asegurar que Weekend sea un booleano.
        datos["Weekend"] = (
            datos.get("Weekend", False) is True
            or datos.get("Weekend", False) == 1
        )
        return datos

    return {
>>>>>>> e79bed5aa8c6377e3b5f3871b948f1b36665b26c
        "Administrative": 0,
        "Administrative_Duration": 0.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
<<<<<<< HEAD
        "ProductRelated": int(paginas_vistas),
        "ProductRelated_Duration": float(minutos),
=======
        "ProductRelated": 1,
        "ProductRelated_Duration": 0.0,
>>>>>>> e79bed5aa8c6377e3b5f3871b948f1b36665b26c
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
<<<<<<< HEAD
        "Weekend": False
    }
    
    print("\n🤖 Asistente: Consultando el estado de tu sesión...")
    time.sleep(1)
    
    # 3. Consulta a la API
    try:
        respuesta = requests.post(API_URL, json={"datos": datos_cliente}, timeout=5)
        
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            prediccion = resultado.get("prediccion")
            
            # Lógica de Lead Scoring e Intervención Proactiva
            if prediccion == 0 and float(minutos) > 5.0:
                print("🤖 Asistente: Veo que llevas un buen rato explorando nuestros productos. ¡Tengo una excelente noticia!")
                print("🤖 Asistente: Te he otorgado un cupón exclusivo del 15% de descuento en tu carrito si completas tu pedido ahora.")
                
                # Novedad: Ahora sí espera tu respuesta
                respuesta_usuario = input("🤖 Asistente: ¿Deseas que te transfiera con un asesor para aplicar el cupón? (sí/no)\n👤 Tú: ").strip().lower()
                
                if respuesta_usuario in ['si', 'sí', 's', 'yes', 'claro']:
                    derivar_a_humano()
                else:
                    print("🤖 Asistente: Entendido. ¡El cupón quedará guardado por si cambias de opinión! Sigue disfrutando de nuestra tienda. ¡Hasta pronto!")
                    
            elif prediccion == 0:
                print("🤖 Asistente: ¿Buscas algún producto en especial? Te invito a revisar nuestras promociones destacadas.")
            else:
                print("🤖 Asistente: ¡Genial! Tus productos seleccionados tienen excelente disponibilidad. ¿Te ayudo a dirigirte a la pasarela de pago?")
        else:
            print(f"🤖 Asistente: No pude verificar tu carrito correctamente (Código HTTP {respuesta.status_code}).")
            derivar_a_humano()
            
    except requests.exceptions.RequestException:
        print("🤖 Asistente: Ocurrió un inconveniente al conectar con el servidor interno.")
        derivar_a_humano()
=======
        "Weekend": False,
    }


def solicitar_dato(mensaje, parsear, fallback="No entendí eso. Prueba de nuevo."):
    intentos = 0

    while intentos < 3:
        entrada = input(f"Asistente: {mensaje}\nTú: ")

        if entrada.strip().lower() in {
            "ayuda", "humano", "asesor", "salir"
        }:
            return "DERIVAR"

        try:
            return parsear(entrada)
        except (ValueError, TypeError):
            print(f"Asistente: {fallback}")
            intentos += 1

    print("Asistente: Te comunicaré con una persona de la tienda.")
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


def parsear_si_no(texto):
    texto = texto.strip().lower()

    if texto in {"si", "sí", "yes", "true", "1"}:
        return True

    if texto in {"no", "false", "0"}:
        return False

    raise ValueError("Responde sí o no.")


def parsear_mes(texto):
    clave = texto.strip().lower()

    if clave not in MESES_ES:
        raise ValueError("Mes no reconocido.")

    return MESES_ES[clave]


def derivar_a_humano():
    print("\n" + "-" * 50)
    print("TRANSFERENCIA A UN ASESOR HUMANO")
    print("Asesor: Hola, ¿en qué te puedo ayudar?")
    print("-" * 50 + "\n")


def iniciar_conversacion():
    print("\n" + "=" * 50)
    print("Asistente: Hola, soy el asistente de la tienda.")
    print("Te haré unas preguntas sobre tu visita.")
    print("Escribe 'ayuda' si deseas hablar con una persona.")
    print("=" * 50 + "\n")

    visitante = solicitar_dato(
        "¿Es tu primera visita o ya has comprado antes? "
        "(nuevo / recurrente)",
        parsear_visitante,
        "Responde 'nuevo', 'recurrente' u otra opción válida.",
    )
    if visitante == "DERIVAR":
        return derivar_a_humano()

    paginas = solicitar_dato(
        "¿Cuántas páginas de productos has abierto?",
        parsear_entero,
        "Escribe un número entero, por ejemplo 8.",
    )
    if paginas == "DERIVAR":
        return derivar_a_humano()

    minutos = solicitar_dato(
        "¿Cuántos minutos llevas en la web?",
        parsear_minutos,
        "Escribe un número, por ejemplo 12.",
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
        "Escribe un mes reconocido, por ejemplo mayo.",
    )
    if mes == "DERIVAR":
        return derivar_a_humano()

    datos_cliente = cargar_defaults()
    datos_cliente.update({
        "VisitorType": visitante,
        "ProductRelated": paginas,
        "ProductRelated_Duration": minutos * 60.0,
        "Weekend": weekend,
        "Month": mes,
    })

    print("\nAsistente: Estoy revisando tu sesión...")
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
                print(
                    "Asistente: El modelo estima una intención de compra baja."
                )
                print(
                    "Puedes consultar las promociones disponibles "
                    "o hablar con un asesor."
                )
            elif prediccion == 1:
                print(
                    "Asistente: El modelo estima una intención de compra alta."
                )
                print("¿Te gustaría continuar con tu compra?")
            else:
                print("Asistente: La respuesta del modelo no es válida.")
                derivar_a_humano()

            if "probabilidad_compra" in resultado:
                probabilidad = resultado["probabilidad_compra"]
                print(
                    f"Probabilidad estimada de compra: "
                    f"{probabilidad:.2%}"
                )

        elif respuesta.status_code == 400:
            print("Asistente: Los datos enviados no son válidos.")
            print("Detalle:", respuesta.text)
            derivar_a_humano()

        else:
            print(
                f"Asistente: El sistema respondió con HTTP "
                f"{respuesta.status_code}."
            )
            derivar_a_humano()

    except requests.exceptions.RequestException as error:
        print("Asistente: No pude conectar con la API.")
        print("Detalle:", error)
        derivar_a_humano()

>>>>>>> e79bed5aa8c6377e3b5f3871b948f1b36665b26c

if __name__ == "__main__":
    iniciar_conversacion()
