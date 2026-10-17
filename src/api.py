from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import joblib
import pandas as pd
import os

app = FastAPI(title="API de Predicción de Compras Online")

# Variables globales para cargar en memoria
modelo = None
preprocesador = None

@app.on_event("startup")
def cargar_recursos():
    global modelo, preprocesador
    ruta_modelo = "modelos/modelo_produccion.pkl"
    ruta_prep = "modelos/preprocesador.joblib"
    
    if not os.path.exists(ruta_modelo) or not os.path.exists(ruta_prep):
        raise RuntimeError("Faltan los archivos del modelo o preprocesador en la carpeta 'modelos/'.")
        
    modelo = joblib.load(ruta_modelo)
    preprocesador = joblib.load(ruta_prep)

# 1. Endpoint de salud (Requisito estricto de la Etapa E5)
@app.get("/health")
def health_check():
    return {"status": "activo", "modelo_cargado": modelo is not None}

# 2. Validación de entradas
class CompraInput(BaseModel):
    datos: Dict[str, Any]

# 3. Endpoint de predicción
@app.post("/predecir")
def predecir_compra(entrada: CompraInput):
    try:
        # Convertir el diccionario entrante a un DataFrame de Pandas (1 sola fila)
        df_entrada = pd.DataFrame([entrada.datos])
        
        # Transformar los datos crudos usando el mismo preprocesador del entrenamiento
        X_proc = preprocesador.transform(df_entrada)
        
        # Generar predicción y probabilidades
        prediccion = modelo.predict(X_proc)[0]
        probabilidades = modelo.predict_proba(X_proc)[0]
        
        return {
            "prediccion": int(prediccion),
            "probabilidad_compra": round(float(probabilidades[1]), 4),
            "alerta": "Alta probabilidad de abandono" if prediccion == 0 else "Compra segura"
        }
    except Exception as e:
        # 4. Errores claros con código 400 (Requisito estricto de la Etapa E5)
        raise HTTPException(
            status_code=400, 
            detail=f"Error validando la entrada. Verifica que enviaste todas las columnas correctas. Detalles: {str(e)}"
        )