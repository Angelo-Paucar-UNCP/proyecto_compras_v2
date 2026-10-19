
import json
import os
import sys
from typing import Any

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.preprocesamiento_api import transformar_entrada

RUTA_MODELO = os.path.join(
    BASE_DIR, "modelos", "modelo_produccion.pkl"
)
RUTA_PREPROCESADOR = os.path.join(
    BASE_DIR, "modelos", "preprocesador.joblib"
)
RUTA_UMBRAL = os.path.join(
    BASE_DIR, "modelos", "umbral.json"
)

app = FastAPI(
    title="API REST - Intención de Compra en Línea",
    version="1.1.0",
)

modelo = None
umbral = None


def cargar_artefactos():
    global modelo, umbral

    if modelo is not None and umbral is not None:
        return

    for ruta, nombre in (
        (RUTA_MODELO, "modelo de producción"),
        (RUTA_PREPROCESADOR, "preprocesador"),
        (RUTA_UMBRAL, "configuración del umbral"),
    ):
        if not os.path.isfile(ruta):
            raise HTTPException(
                status_code=503,
                detail=f"No se encontró el {nombre}.",
            )

    try:
        nuevo_modelo = joblib.load(RUTA_MODELO)

        with open(RUTA_UMBRAL, encoding="utf-8") as archivo:
            configuracion = json.load(archivo)

        nuevo_umbral = float(configuracion["umbral"])

        if not 0 < nuevo_umbral < 1:
            raise ValueError("Umbral fuera del intervalo válido.")

        modelo = nuevo_modelo
        umbral = nuevo_umbral

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="No se pudieron cargar los artefactos de producción.",
        ) from error


@app.get("/")
@app.get("/salud")
@app.get("/health")
def verificar_salud():
    cargar_artefactos()

    return {
        "estado": "OK",
        "status": "activo",
        "servicio": "API REST Intención de Compra",
        "modelo": os.path.basename(RUTA_MODELO),
        "modelo_cargado": modelo is not None,
        "preprocesador_disponible": os.path.isfile(RUTA_PREPROCESADOR),
        "umbral": umbral,
    }


@app.post("/predict")
@app.post("/predecir")
def predecir(payload: dict[str, Any]):
    cargar_artefactos()

    if "datos" in payload:
        datos = payload["datos"]
        if not isinstance(datos, dict):
            raise HTTPException(
                status_code=400,
                detail="El campo 'datos' debe ser un objeto.",
            )
    else:
        datos = payload

    try:
        X_proc = transformar_entrada(
            datos,
            preprocessor_path=RUTA_PREPROCESADOR,
        )
    except (ValueError, TypeError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Error al preparar los datos de entrada.",
        ) from error

    try:
        if hasattr(modelo, "predict_proba"):
            probabilidades = np.asarray(
                modelo.predict_proba(X_proc)
            )
            clases = list(getattr(modelo, "classes_", []))

            indice = (
                clases.index(1)
                if 1 in clases
                else probabilidades.shape[1] - 1
            )

            probabilidad = float(probabilidades[0, indice])
            prediccion = int(probabilidad >= umbral)
        else:
            prediccion = int(
                np.asarray(modelo.predict(X_proc)).ravel()[0]
            )
            probabilidad = float(prediccion)

        return {
            "prediccion": prediccion,
            "probabilidad_compra": round(probabilidad, 4),
            "mensaje": (
                "Intención de compra ALTA"
                if prediccion == 1
                else "Intención de compra BAJA"
            ),
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Error durante la predicción.",
        ) from error


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
