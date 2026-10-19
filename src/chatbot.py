import requests
import time

API_URL = "http://127.0.0.1:8000/predecir"

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
        "Administrative": 0,
        "Administrative_Duration": 0.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": int(paginas_vistas),
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

if __name__ == "__main__":
    iniciar_conversacion()

>>>>>>> e79bed5aa8c6377e3b5f3871b948f1b36665b26c

if __name__ == "__main__":
    iniciar_conversacion()
