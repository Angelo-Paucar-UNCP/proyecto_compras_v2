import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
import os

def preparar_datos():
    print("Iniciando pipeline de datos...")
    
    # 1. Carga de datos
    df = pd.read_csv("datos/online_shoppers_intention.csv")

    # 2. Limpieza de calidad (Requisito Rúbrica C2)
    # Detecta y elimina filas exactamente iguales que contaminarían la prueba
    duplicados_antes = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"✅ Se eliminaron {duplicados_antes} filas duplicadas para evitar fuga.")

    # 3. Separación de objetivo
    X = df.drop(columns=['Revenue'])
    y = df['Revenue'].astype(int)

    # 4. Partición Estratificada con Semilla (Requisito Rúbrica C2)
    # Separa 70% Entrenamiento, 15% Validación, 15% Prueba manteniendo la proporción de clases
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42, stratify=y_temp)

    # 5. Definición de Transformadores
    num_cols = ['Administrative', 'Administrative_Duration', 'Informational', 
                'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration', 
                'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
    
    cat_cols = ['Month', 'OperatingSystems', 'Browser', 'Region', 
                'TrafficType', 'VisitorType', 'Weekend']

    preprocesador = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
        ]
    )

    # 6. PREVENCIÓN DE FUGA DE INFORMACIÓN (Requisito Crítico C2 y Defensa D1)
    # El escalador aprende las medias/desviaciones ÚNICAMENTE con los datos de entrenamiento
    X_train_procesado = preprocesador.fit_transform(X_train)
    
    # Validación y Prueba SOLO se transforman, no se ajustan
    X_val_procesado = preprocesador.transform(X_val)
    X_test_procesado = preprocesador.transform(X_test)

    # 7. Guardar el transformador para la API
    os.makedirs("modelos", exist_ok=True)
    joblib.dump(preprocesador, "modelos/preprocesador.pkl")
    
    # Guardar los datos procesados para el script de entrenamiento (modelo.py)
    joblib.dump((X_train_procesado, X_val_procesado, X_test_procesado, y_train, y_val, y_test), "modelos/datos_procesados.pkl")
    
    print("✅ Preprocesamiento finalizado con éxito. Listo para entrenar.")

if __name__ == "__main__":
    preparar_datos()