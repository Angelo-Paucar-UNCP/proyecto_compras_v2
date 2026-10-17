import requests
import time

API_URL = "http://127.0.0.1:8000/predecir"

def solicitar_dato(mensaje, tipo_esperado=int, fallback="Disculpa, no entendí eso. ¿Podrías ingresar solo el número?"):
    """Recolecta datos paso a paso (slots) manejando errores (fallback)."""
    intentos = 0
    while intentos < 3:
        entrada = input(f"🤖 Asistente: {mensaje}\n👤 Tú: ")
        
        # Opción de salida o derivación humana directa
        if entrada.lower() in ['ayuda', 'humano', 'asesor', 'salir']:
            return "DERIVAR"
            
        try:
            # Intentar convertir al tipo de dato esperado
            valor = tipo_esperado(entrada)
            return valor
        except ValueError:
            print(f"🤖 Asistente: {fallback}")
            intentos += 1
            
    print("🤖 Asistente: Parece que estamos teniendo problemas de comunicación. Te pasaré con un asesor humano.")
    return "DERIVAR"

def iniciar_conversacion():
    print("\n" + "="*50)
    print("🤖 Asistente: ¡Hola! Soy tu asistente virtual de la tienda.")
    print("🤖 Asistente: Estoy aquí para ayudarte a encontrar lo que buscas o conectarte con un experto.")
    print("🤖 Asistente: (Escribe 'ayuda' en cualquier momento para hablar con un humano)")
    print("="*50 + "\n")
    
    # Recolección paso a paso (Slots)
    # NOTA: Estas preguntas deben mapearse a las columnas numéricas/categóricas de tu dataset real
    paginas_vistas = solicitar_dato("¿Cuántas páginas de productos has mirado hoy?")
    if paginas_vistas == "DERIVAR": return derivar_a_humano()
        
    minutos = solicitar_dato("¿Aproximadamente cuántos minutos llevas navegando en nuestra web?")
    if minutos == "DERIVAR": return derivar_a_humano()
    
    # Construir el diccionario con los datos EXACTOS que tu preprocesador espera
    # Rellena el resto de columnas con valores por defecto (moda/mediana) si el chatbot no las pregunta
    datos_cliente = {
        "ProductRelated": paginas_vistas,
        "ProductRelated_Duration": float(minutos),
        "BounceRates": 0.0,
        "ExitRates": 0.0,
        "PageValues": 0.0,
        "SpecialDay": 0.0,
        "Month": "Nov",
        "OperatingSystems": 1,
        "Browser": 1,
        "Region": 1,
        "TrafficType": 1,
        "VisitorType": "Returning_Visitor",
        "Weekend": False
        # Ajusta estas claves a las columnas exactas que quedaron en tu dataset después de la limpieza
    }
    
    print("\n🤖 Asistente: Dame un segundito, estoy revisando el sistema...")
    time.sleep(1.5)
    
    # Consumir la API
    try:
        respuesta = requests.post(API_URL, json={"datos": datos_cliente})
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            
            # Lógica de negocio basada en la predicción de la API
            if resultado['prediccion'] == 0: # Predicción de abandono
                print("🤖 Asistente: Veo que llevas un rato mirando. ¡Tengo un cupón del 15% de descuento solo para ti si finalizas tu compra hoy!")
                print("🤖 Asistente: ¿Te gustaría que un asesor te ayude a aplicarlo?")
                derivar_a_humano()
            else:
                print("🤖 Asistente: ¡Genial! Tus productos seleccionados son excelentes. ¿Te ayudo a ir a la caja?")
        else:
            print("🤖 Asistente: Uy, mi sistema interno está un poco lento hoy. Te comunicaré con mi compañero humano.")
            derivar_a_humano()
            
    except requests.exceptions.ConnectionError:
        print("🤖 Asistente: (Error) No puedo conectar con mi cerebro (API apagada). Te pasaré con un humano.")

def derivar_a_humano():
    """Derivación a una persona de soporte."""
    print("\n" + "-"*50)
    print("📞 TRANSFIRIENDO A UN ASESOR HUMANO...")
    print("👩🏽‍💻 Asesor real: ¡Hola! Soy el asesor de ventas. ¿En qué te puedo ayudar?")
    print("-"*50 + "\n")

if __name__ == "__main__":
    iniciar_conversacion()