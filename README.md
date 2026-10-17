# Proyecto Parcial: Predicción de Intención de Compra Online

Este proyecto predice si un usuario abandonará su carrito de compras o finalizará la transacción, con el objetivo de ofrecer descuentos estratégicos en tiempo real.

## Requisitos

- Python 3.10 o superior

## Instalación desde cero

1. Clonar el repositorio.
2. Crear y activar el entorno virtual:
   `python -m venv .venv`
   `.\.venv\Scripts\Activate.ps1` (Windows)
3. Instalar dependencias:
   `pip install -r requirements.txt`

## Ejecución del Pipeline

1. **Entrenar los modelos:** Ejecuta `python entrenar.py`. Esto descargará los datos, entrenará la línea base y las redes neuronales, y guardará el ganador en `modelos/`.
2. **Levantar la API:** Ejecuta `uvicorn src.api:app --reload`.
3. **Probar el Chatbot:** En una nueva terminal, ejecuta `python src/chatbot.py`.

## Pruebas

Para correr las pruebas automatizadas, ejecuta: `pytest tests/ -v`
