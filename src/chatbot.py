import json
import math
import time
import requests
import os
from pathlib import Path

# Ajuste de ruta para compatibilidad de ejecución
RUTA_DEFAULTS = Path(__file__).parent.parent / "modelos" / "valores_por_defecto.json"
API_URL = "http://127.0.0.1:8001/predecir"

MAX_PAGINAS = 200
MAX_MINUTOS = 240
SEGUNDOS_MIN_POR_PAGINA = 6

MESES_ES = {
    "enero": "Jan", "febrero": "Feb", "marzo": "Mar", "abril": "Apr",
    "mayo": "May", "junio": "June", "julio": "Jul", "agosto": "Aug", 
    "septiembre": "Sep", "octubre": "Oct", "noviembre": "Nov", "diciembre": "Dec",
    "may": "May"
}

def cargar_defaults():
    if RUTA_DEFAULTS.exists():
        with open(RUTA_DEFAULTS, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        datos["Weekend"] = (datos.get("Weekend", False) is True or datos.get("Weekend", False) == 1)
        return datos
    return {
        "Administrative": 0, "Administrative_Duration": 0.0, "Informational": 0,
        "Informational_Duration": 0.0, "ProductRelated": 1, "ProductRelated_Duration": 0.0,
        "BounceRates": 0.0, "ExitRates": 0.04, "PageValues": 0.0, "SpecialDay": 0.0,
        "Month": "May", "OperatingSystems": 2, "Browser": 2, "Region": 1,
        "TrafficType": 2, "VisitorType": "Returning_Visitor", "Weekend": False,
    }

def solicitar_dato(mensaje, parsear, fallback="Dato inválido. Intenta de nuevo."):
    intentos = 0
    while intentos < 3:
        entrada = input(f"🤖 Sistema: {mensaje}\n👨‍💻 Vendedor: ")
        if entrada.strip().lower() in {"salir", "cerrar", "cancelar", "ayuda"}:
            return "CANCELAR"
        try:
            return parsear(entrada)
        except (ValueError, TypeError):
            print(f"⚠️ Sistema: {fallback}")
            intentos += 1
    print("🚨 Sistema: Demasiados errores. Abortando evaluación actual.")
    return "CANCELAR"

def parsear_entero(texto):
    valor = int(texto.strip())
    if not 1 <= valor <= MAX_PAGINAS: raise ValueError("Fuera de rango.")
    return valor

def minimo_minutos(paginas):
    return max(0.5, paginas * SEGUNDOS_MIN_POR_PAGINA / 60)

def crear_parser_minutos(paginas):
    def parsear_minutos(texto):
        valor = float(texto.strip().replace(",", "."))
        if not math.isfinite(valor) or not minimo_minutos(paginas) <= valor <= MAX_MINUTOS:
            raise ValueError("Fuera de rango.")
        return valor
    return parsear_minutos

def parsear_visitante(texto):
    texto = texto.strip().lower()
    if texto in {"nuevo", "1"}: return "New_Visitor"
    if texto in {"recurrente", "2"}: return "Returning_Visitor"
    raise ValueError("Tipo inválido.")

def parsear_mes(texto):
    clave = texto.strip().lower()
    if clave not in MESES_ES: raise ValueError("Mes no reconocido.")
    return MESES_ES[clave]

def evaluar_cliente():
    print("\n" + "═" * 60)
    print("🎯 PANEL DE LEAD SCORING - EVALUACIÓN DE SESIÓN EN VIVO")
    print("═" * 60)

    visitante = solicitar_dato("¿El cliente en línea es nuevo (1) o recurrente (2)?", parsear_visitante)
    if visitante == "CANCELAR": return
    
    paginas = solicitar_dato("¿Cuántas páginas de producto ha visitado en esta sesión?", parsear_entero)
    if paginas == "CANCELAR": return

    minutos = solicitar_dato("¿Cuántos minutos lleva activo?", crear_parser_minutos(paginas))
    if minutos == "CANCELAR": return

    mes = solicitar_dato("¿Mes actual de la sesión? (ej. mayo, noviembre)", parsear_mes)
    if mes == "CANCELAR": return

    datos_cliente = cargar_defaults()
    datos_cliente.update({
        "VisitorType": visitante, "ProductRelated": paginas,
        "ProductRelated_Duration": minutos * 60.0, "Month": mes,
    })

    print("\n⏳ Sistema: Consultando al modelo predictivo...")
    time.sleep(1)

    try:
        respuesta = requests.post(API_URL, json={"datos": datos_cliente}, timeout=10)
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            prediccion = resultado.get("prediccion")
            prob = resultado.get("probabilidad_compra", 0.0)

            print(f"\n📊 Probabilidad de compra: {prob:.2%}")
            
            if prediccion == 1:
                print("🟢 ESTADO: COMPRA ORGÁNICA ASEGURADA.")
                print("🛑 ACCIÓN AUTOMÁTICA: No hacer nada. Pasando de largo para proteger el margen de ganancia.")
            elif prediccion == 0:
                print("🔴 ESTADO: RIESGO DE ABANDONO DETECTADO.")
                print("🎁 ACCIÓN AUTOMÁTICA: Disparando popup con cupón de 15% de descuento para retener la venta.")
            else:
                print("⚠️ Sistema: Error en la salida del modelo.")

        else:
            print(f"⚠️ Sistema: Fallo en API (HTTP {respuesta.status_code}). Detalle: {respuesta.text}")
    except requests.exceptions.RequestException as error:
        print("❌ Sistema: Servidor API inalcanzable. Verifique que uvicorn esté corriendo en el puerto 8001.")

def iniciar_panel():
    while True:
        evaluar_cliente()
        print("\n" + "─" * 60)
        continuar = input("▶️ ¿Deseas evaluar a otro cliente en la fila? (sí/no): ").strip().lower()
        if continuar not in ['si', 'sí', 's', 'yes']:
            print("Cerrando panel de Lead Scoring. ¡Buen turno de ventas!")
            break

if __name__ == "__main__":
    iniciar_panel()