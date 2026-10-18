import sys
import os
# Añade la carpeta actual (src) al path de Python para evitar errores de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocesamiento_api import transformar_entrada

import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

# Importar preprocesamiento con fallback para ejecuciones desde raíz o módulo src
try:
    from src.preprocesamiento_api import transformar_entrada
except ImportError:
    from preprocesamiento_api import transformar_entrada

app = FastAPI(
    title="API REST - Intención de Compra en Línea",
    description="Servicio web para predecir la probabilidad de compra de un usuario usando Redes Neuronales.",
    version="1.0.0"
)

# Cargar el modelo promovido al iniciar el servicio
RUTA_MODELO = "modelos/red_neuronal_v2.joblib"
if not os.path.exists(RUTA_MODELO):
    # Intentar con nombre alternativo si se usa modelo_promovido.joblib
    if os.path.exists("modelos/modelo_promovido.joblib"):
        RUTA_MODELO = "modelos/modelo_promovido.joblib"

modelo = None
if os.path.exists(RUTA_MODELO):
    modelo = joblib.load(RUTA_MODELO)

@app.get("/")
@app.get("/salud")
def verificar_salud():
    """
    Endpoint de verificación de estado de la API (Healthcheck - E5).
    """
    estado_modelo = "Cargado" if modelo is not None else "No encontrado en modelos/"
    return {
        "estado": "OK",
        "servicio": "API REST Intención de Compra",
        "modelo": estado_modelo
    }

@app.post("/predict")
def predecir(payload: Dict[str, Any]):
    """
    Endpoint para realizar predicciones de intención de compra (E5).
    Acepta solicitudes JSON parciales o completas y retorna la probabilidad calculada.
    """
    global modelo
    if modelo is None:
        if os.path.exists(RUTA_MODELO):
            modelo = joblib.load(RUTA_MODELO)
        else:
            raise HTTPException(
                status_code=500,
                detail="Modelo no disponible. Asegúrate de haber ejecutado src/modelo.py primero."
            )

    try:
        # Preprocesar entrada y validar con defensas
        X_proc = transformar_entrada(payload)

        # Calcular probabilidades e inferencia
        if hasattr(modelo, "predict_proba"):
            probabilidades = modelo.predict_proba(X_proc)[0]
            prob_compra = float(probabilidades[1]) if len(probabilidades) > 1 else float(probabilidades[0])
        else:
            # Fallback si el modelo solo tiene predict
            pred = modelo.predict(X_proc)[0]
            prob_compra = float(pred)

        prediccion = 1 if prob_compra >= 0.5 else 0

        return {
            "prediccion": prediccion,
            "probabilidad_compra": round(prob_compra, 4),
            "mensaje": "Intención de compra ALTA" if prediccion == 1 else "Intención de compra BAJA"
        }

    except ValueError as e:
        # Captura errores de validación (columnas inválidas, rangos incorrectos) y retorna 400
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Captura cualquier otro error interno y retorna 500
        raise HTTPException(status_code=500, detail=f"Error interno durante la inferencia: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
