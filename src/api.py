from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="API Lead Scoring B2B", version="1.0")

modelo = None
preprocesador = None

class DatosCliente(BaseModel):
    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: str
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: str
    Weekend: bool

class RequestPredict(BaseModel):
    datos: DatosCliente

@app.on_event("startup")
def cargar_modelo():
    global modelo, preprocesador
    try:
        modelo = joblib.load("modelos/modelo_produccion.pkl")
        preprocesador = joblib.load("modelos/preprocesador.joblib")
        print("✅ Modelo y preprocesador cargados en memoria.")
    except Exception as e:
        print(f"❌ Error al cargar los modelos: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "modelo_cargado": modelo is not None}

@app.post("/predecir")
def predecir(request: RequestPredict):
    """Endpoint principal de predicción con umbral comercial."""
    if modelo is None or preprocesador is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible en el servidor.")
    
    try:
        # 1. Convertir el JSON validado a DataFrame
        df = pd.DataFrame([request.datos.model_dump()]) # Usando model_dump() para evitar el warning de Pydantic
        
        # 2. Aplicar las transformaciones (sin fuga de datos)
        X_transformado = preprocesador.transform(df)
        
        # 3. Predecir SOLO las probabilidades (Ignoramos el .predict() por defecto)
        probabilidades = modelo.predict_proba(X_transformado)[0]
        prob_compra = probabilidades[1] if len(probabilidades) > 1 else 0.0

        # 4. APLICAR UMBRAL PERSONALIZADO (30%)
        UMBRAL = 0.30
        prediccion = 1 if prob_compra >= UMBRAL else 0

        return {
            "prediccion": int(prediccion),
            "probabilidad_compra": float(prob_compra),
            "version": "1.0-Produccion-Umbral30"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en los datos de entrada: {str(e)}")