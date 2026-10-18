import pandas as pd
import joblib

# Lista de las 17 columnas que el preprocesador espera, con sus valores por defecto
COLUMNAS_ESPERADAS = {
    'Administrative': 0,
    'Administrative_Duration': 0.0,
    'Informational': 0,
    'Informational_Duration': 0.0,
    'ProductRelated': 0,
    'ProductRelated_Duration': 0.0,
    'BounceRates': 0.0,
    'ExitRates': 0.02,
    'PageValues': 0.0,
    'SpecialDay': 0.0,
    'Month': 'May',
    'OperatingSystems': 1,
    'Browser': 1,
    'Region': 1,
    'TrafficType': 1,
    'VisitorType': 'Returning_Visitor',
    'Weekend': False
}

def preparar_datos_entrada(datos_json):
    """
    Toma un diccionario con los datos enviados por el chatbot o cliente de la API
    y garantiza que contenga las 17 columnas necesarias para el preprocesador.
    
    Si faltan columnas (como Administrative, Administrative_Duration, Informational,
    o Informational_Duration), se agregan automáticamente con valor 0 para evitar el error HTTP 400.
    """
    if isinstance(datos_json, dict):
        datos_dict = datos_json.copy()
    else:
        datos_dict = dict(datos_json)

    # Rellenar cualquier columna faltante con su valor por defecto (0 para las administrativas/informativas)
    for col, default_val in COLUMNAS_ESPERADAS.items():
        if col not in datos_dict or datos_dict[col] is None:
            datos_dict[col] = default_val

    # Crear DataFrame garantizando el orden exacto de columnas que espera scikit-learn
    df = pd.DataFrame([datos_dict])
    df = df[list(COLUMNAS_ESPERADAS.keys())]
    return df

def transformar_entrada(datos_json, preprocessor_path='modelos/preprocesador.joblib'):
    """
    Carga el preprocesador guardado en la Etapa E2 y aplica la transformación sobre
    el DataFrame con las 17 columnas completas.
    """
    df = preparar_datos_entrada(datos_json)
    preprocessor = joblib.load(preprocessor_path)
    X_proc = preprocessor.transform(df)
    return X_proc
