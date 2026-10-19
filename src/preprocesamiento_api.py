import os
import json
import pandas as pd
import joblib

DEFAULTS_BASE = {
    'Administrative': 0, 'Administrative_Duration': 0.0,
    'Informational': 0, 'Informational_Duration': 0.0,
    'ProductRelated': 0, 'ProductRelated_Duration': 0.0,
    'BounceRates': 0.0, 'ExitRates': 0.02, 'PageValues': 0.0,
    'SpecialDay': 0.0, 'Month': 'May', 'OperatingSystems': 1,
    'Browser': 1, 'Region': 1, 'TrafficType': 1,
    'VisitorType': 'Returning_Visitor', 'Weekend': False,
}
try:
    from .rutas import RUTA_DEFAULTS
except ImportError:
    from rutas import RUTA_DEFAULTS


def cargar_defaults():
    if RUTA_DEFAULTS.is_file():
        with open(RUTA_DEFAULTS, encoding="utf-8") as archivo:
            return json.load(archivo)
    return DEFAULTS_BASE.copy()


DEFAULTS = cargar_defaults()

OBLIGATORIAS = ['ProductRelated', 'ProductRelated_Duration']
MESES = {'Feb','Mar','May','June','Jul','Aug','Sep','Oct','Nov','Dec'}
VISITANTES = {'Returning_Visitor','New_Visitor','Other'}
TASAS = ['BounceRates','ExitRates','SpecialDay']

def preparar_datos_entrada(datos):
    if not isinstance(datos, dict):
        raise ValueError("Los datos deben ser un diccionario.")
    desconocidas = set(datos) - set(DEFAULTS)
    if desconocidas:
        raise ValueError(f"Columnas no reconocidas: {sorted(desconocidas)}")
    faltan = [c for c in OBLIGATORIAS if datos.get(c) is None]
    if faltan:
        raise ValueError(f"Faltan columnas obligatorias: {faltan}")

    d = {**DEFAULTS, **{k: v for k, v in datos.items() if v is not None}}

    for col, defecto in DEFAULTS.items():
        if isinstance(defecto, (int, float)) and not isinstance(defecto, bool):
            try:
                d[col] = float(d[col])
            except (TypeError, ValueError):
                raise ValueError(f"'{col}' debe ser un número.")
            if d[col] < 0:
                raise ValueError(f"'{col}' no puede ser negativo.")
    for col in TASAS:
        if d[col] > 1:
            raise ValueError(f"'{col}' debe estar entre 0 y 1.")
    if d['Month'] not in MESES:
        raise ValueError(f"'Month' debe ser uno de {sorted(MESES)}.")
    if d['VisitorType'] not in VISITANTES:
        raise ValueError(f"'VisitorType' debe ser uno de {sorted(VISITANTES)}.")
    if not isinstance(d['Weekend'], bool):
        raise ValueError("'Weekend' debe ser true o false.")

    return pd.DataFrame([d])[list(DEFAULTS)]

def buscar_preprocesador():
    """Busca el archivo del preprocesador en la carpeta modelos/."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    candidatos = [
        "modelos/preprocesador.joblib",
        "modelos/preprocesador_scaler.joblib",
        "modelos/scaler.joblib"
    ]
    for rel_path in candidatos:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            return full_path
        if os.path.exists(rel_path):
            return rel_path
    
    modelos_dir = os.path.join(base_dir, "modelos")
    if os.path.exists(modelos_dir):
        for f in os.listdir(modelos_dir):
            if "preprocesador" in f and f.endswith(".joblib"):
                return os.path.join(modelos_dir, f)
    return "modelos/preprocesador.joblib"

def transformar_entrada(datos_json, preprocessor_path=None):
    df = preparar_datos_entrada(datos_json)
    if preprocessor_path is None or not os.path.exists(preprocessor_path):
        preprocessor_path = buscar_preprocesador()
    
    preprocessor = joblib.load(preprocessor_path)
    return preprocessor.transform(df)
