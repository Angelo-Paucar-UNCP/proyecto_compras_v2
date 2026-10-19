import json
import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from .rutas import DATA_DIR, MODELOS_DIR, RUTA_CSV, RUTA_DEFAULTS, RUTA_PREPROCESADOR
except ImportError:
    from rutas import DATA_DIR, MODELOS_DIR, RUTA_CSV, RUTA_DEFAULTS, RUTA_PREPROCESADOR

URL_DATASET = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "00468/online_shoppers_intention.csv"
)
TARGET_COL = "Revenue"

# PageValues se conoce durante la sesión (valor medio de páginas ya visitadas),
# no después del checkout. Se conserva. No usamos el resultado de la compra.
COLUMNAS_FUGA = []


def cargar_datos(filepath=None):
    filepath = str(filepath or RUTA_CSV)
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath) or str(DATA_DIR), exist_ok=True)
        print("Descargando dataset Online Shoppers Intention...")
        df = pd.read_csv(URL_DATASET)
        df.to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)
    return df


def _valores_por_defecto(X_train):
    defaults = {}
    for col in X_train.columns:
        if pd.api.types.is_numeric_dtype(X_train[col]):
            defaults[col] = float(X_train[col].median())
        else:
            valor = X_train[col].mode().iloc[0]
            defaults[col] = bool(valor) if pd.api.types.is_bool_dtype(X_train[col]) else valor
    return defaults


def preparar_y_dividir_datos(df, target_col=TARGET_COL, random_state=42):
    """
    Parte 70/15/15 de forma estratificada.
    El preprocesador se ajusta SOLO con entrenamiento.
    """
    df = df.copy()
    cols_fuga = [c for c in COLUMNAS_FUGA if c in df.columns]
    if cols_fuga:
        df = df.drop(columns=cols_fuga)

    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=random_state, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=random_state, stratify=y_temp
    )

    num_cols = X_train.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    cat_cols = X_train.select_dtypes(include=["object", "bool"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ]
    )

    X_train_proc = preprocessor.fit_transform(X_train)
    X_val_proc = preprocessor.transform(X_val)
    X_test_proc = preprocessor.transform(X_test)

    return {
        "X_train": X_train_proc,
        "y_train": y_train.values,
        "X_val": X_val_proc,
        "y_val": y_val.values,
        "X_test": X_test_proc,
        "y_test": y_test.values,
        "preprocessor": preprocessor,
        "defaults": _valores_por_defecto(X_train),
        "columnas": list(X_train.columns),
    }


def guardar_artefactos_datos(datos):
    MODELOS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(datos["preprocessor"], RUTA_PREPROCESADOR)
    with open(RUTA_DEFAULTS, "w", encoding="utf-8") as f:
        json.dump(datos["defaults"], f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    guardar_artefactos_datos(datos)
    print("Datos listos.")
    print(f"Entrenamiento: {datos['X_train'].shape}")
    print(f"Validación: {datos['X_val'].shape}")
    print(f"Prueba: {datos['X_test'].shape}")
