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
        print("Descargando dataset Online Shoppers Intention desde UCI...")
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv"
        df = pd.read_csv(url)
        df.to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)
    return df

def preparar_y_dividir_datos(df, target_col='Revenue', random_state=42):
    """
    Divide los datos en Train (70%), Val (15%) y Test (15%) de forma estratificada.
    Ajusta el preprocesador EXCLUSIVAMENTE sobre el conjunto de entrenamiento.
    """
    # Tratamiento de Fuga de Información (si deciden remover PageValues)
    columnas_fuga = []
    cols_a_eliminar = [col for col in columnas_fuga if col in df.columns]
    if cols_a_eliminar:
        df = df.drop(columns=cols_a_eliminar)

    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)

    # Partición estratificada (70% train, 30% temp)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=random_state, stratify=y
    )

    # Partición estratificada (15% val, 15% test)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=random_state, stratify=y_temp
    )

    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'bool']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
        ]
    )

    # Fit solo en entrenamiento para evitar fuga de información
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
    
    os.makedirs('modelos', exist_ok=True)
    
    ruta_preprocesador = 'modelos/preprocesador.joblib'
    joblib.dump(datos['preprocessor'], ruta_preprocesador)
    
    print("\n¡Preprocesamiento completado con éxito!")
    print(f"Dimensiones Train: {datos['X_train'].shape}")
    print(f"Dimensiones Val:   {datos['X_val'].shape}")
    print(f"Dimensiones Test:  {datos['X_test'].shape}")
    print(f"Preprocesador guardado en: {ruta_preprocesador}")
