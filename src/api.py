import os
import sys
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from typing import Any, Dict

# Agregar la raíz del proyecto al PATH para importar desde src
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.preprocesamiento_api import transformar_entrada

app = FastAPI(
    title="API REST - Intención de Compra en Línea",
    version="1.0.0"
)

def buscar_modelo():
    directorios = [os.path.join(BASE_DIR, "modelos"), "modelos", "."]
    extensiones = [".joblib", ".pkl"]
    for d in directorios:
        if os.path.exists(d):
            for f in os.listdir(d):
                if any(f.endswith(ext) for ext in extensiones) and "preprocesador" not in f and "scaler" not in f:
                    return os.path.join(d, f)
    return None

RUTA_MODELO = buscar_modelo()
modelo = joblib.load(RUTA_MODELO) if RUTA_MODELO and os.path.exists(RUTA_MODELO) else None

@app.get("/")
@app.get("/salud")
def verificar_salud():
    global modelo, RUTA_MODELO
    if modelo is None:
        RUTA_MODELO = buscar_modelo()
        if RUTA_MODELO and os.path.exists(RUTA_MODELO):
            modelo = joblib.load(RUTA_MODELO)

    return {
        "estado": "OK",
        "servicio": "API REST Intención de Compra",
        "modelo": f"Cargado ({os.path.basename(RUTA_MODELO)})" if modelo is not None else "No encontrado en modelos/"
    }

@app.post("/predict")
def predecir(payload: Dict[str, Any]):
    global modelo, RUTA_MODELO
    if modelo is None:
        RUTA_MODELO = buscar_modelo()
        if RUTA_MODELO and os.path.exists(RUTA_MODELO):
            modelo = joblib.load(RUTA_MODELO)

    if modelo is None:
        raise HTTPException(
            status_code=500, 
            detail="Modelo no encontrado en 'modelos/'. Ejecuta 'python src/modelo.py' para generarlo."
        )

    try:
        X_proc = transformar_entrada(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en preprocesamiento: {str(e)}")

    try:
        if hasattr(modelo, "predict_proba"):
            probs = modelo.predict_proba(X_proc)
            prob_compra = float(np.asarray(probs).ravel()[-1])
        else:
            pred = modelo.predict(X_proc)
            prob_compra = float(np.asarray(pred).ravel())

        prediccion = 1 if prob_compra >= 0.5 else 0

        return {
            "prediccion": prediccion,
            "probabilidad_compra": round(prob_compra, 4),
            "mensaje": "Intención de compra ALTA" if prediccion == 1 else "Intención de compra BAJA"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
