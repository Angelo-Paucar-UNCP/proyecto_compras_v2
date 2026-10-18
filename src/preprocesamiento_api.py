import pandas as pd
import joblib

DEFAULTS = {
    'Administrative': 0, 'Administrative_Duration': 0.0,
    'Informational': 0, 'Informational_Duration': 0.0,
    'ProductRelated': 0, 'ProductRelated_Duration': 0.0,
    'BounceRates': 0.0, 'ExitRates': 0.02, 'PageValues': 0.0,
    'SpecialDay': 0.0, 'Month': 'May', 'OperatingSystems': 1,
    'Browser': 1, 'Region': 1, 'TrafficType': 1,
    'VisitorType': 'Returning_Visitor', 'Weekend': False,
}
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

def transformar_entrada(datos_json, preprocessor_path='modelos/preprocesador.joblib'):
    df = preparar_datos_entrada(datos_json)
    preprocessor = joblib.load(preprocessor_path)
    return preprocessor.transform(df)
