import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def cargar_datos(filepath='data/online_shoppers_intention.csv'):
    """
    Carga el dataset localmente o lo descarga desde la fuente oficial de UCI.
    """
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        print("Descargando dataset Online Shoppers Intention...")
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv"
        df = pd.read_csv(url)
        df.to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)
    return df

def preparar_y_dividir_datos(df, target_col='Revenue', random_state=42):
    """
    Divide los datos en Train (70%), Val (15%) y Test (15%) de forma estratificada.
    El preprocesador se ajusta EXCLUSIVAMENTE con el conjunto de entrenamiento.
    """
    # 1. Tratamiento de Fuga de Información (Rúbrica E2)
    # En el dataset UCI, 'PageValues' a veces se considera fuga porque representa 
    # el valor promedio de la página visitada antes de la compra, lo cual podría 
    # no conocerse hasta que el usuario finalice el recorrido.
    # Si decides justificar su eliminación en el informe, agrégala a la lista:
    columnas_fuga = [] # Ejemplo: ["PageValues"] 
    
    cols_a_eliminar = [col for col in columnas_fuga if col in df.columns]
    if cols_a_eliminar:
        df = df.drop(columns=cols_a_eliminar)

    # 2. Separar características (X) y variable objetivo (y)
    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)

    # 3. División 70% train, 30% temporal
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=random_state, stratify=y
    )

    # 4. División 50% val, 50% test (15% y 15% del total)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=random_state, stratify=y_temp
    )

    # 5. Definir preprocesador
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'bool']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
        ]
    )

    # 6. Transformar (Ajuste SOLO en entrenamiento)
    X_train_proc = preprocessor.fit_transform(X_train)
    X_val_proc = preprocessor.transform(X_val)
    X_test_proc = preprocessor.transform(X_test)

    return {
        'X_train': X_train_proc, 'y_train': y_train.values,
        'X_val': X_val_proc,     'y_val': y_val.values,
        'X_test': X_test_proc,   'y_test': y_test.values,
        'preprocessor': preprocessor
    }

if __name__ == "__main__":
    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    
    # Asegurar que la carpeta modelos existe
    os.makedirs('modelos', exist_ok=True)
    
    # Guardar el preprocesador físicamente para la Etapa E5 (API)
    ruta_preprocesador = 'modelos/preprocesador.joblib'
    joblib.dump(datos['preprocessor'], ruta_preprocesador)
    
    print("¡Datos cargados y procesados con éxito!")
    print(f"Entrenamiento: {datos['X_train'].shape}")
    print(f"Validación: {datos['X_val'].shape}")
    print(f"Prueba: {datos['X_test'].shape}")
    print(f"Preprocesador guardado en: {ruta_preprocesador}")