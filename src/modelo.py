import os

import joblib
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

try:
    from .rutas import MODELOS_DIR
except ImportError:
    from rutas import MODELOS_DIR


def entrenar_lineas_base_y_redes(X_train, y_train):
    """
    1. Trivial (clase mayoritaria)
    2. Simple (regresión logística, con peso por clase)
    3. Red neuronal v1: una capa oculta
    4. Red neuronal v2: dos capas y regularización L2
    """
    print("Entrenando modelo trivial...")
    modelo_trivial = DummyClassifier(strategy="most_frequent", random_state=42)
    modelo_trivial.fit(X_train, y_train)

    print("Entrenando modelo simple (regresión logística)...")
    modelo_simple = LogisticRegression(
        max_iter=2000, class_weight="balanced", random_state=42
    )
    modelo_simple.fit(X_train, y_train)

    print("Entrenando red neuronal v1 (32 neuronas)...")
    nn_v1 = MLPClassifier(
        hidden_layer_sizes=(32,),
        activation="relu",
        max_iter=400,
        random_state=42,
    )
    nn_v1.fit(X_train, y_train)

    print("Entrenando red neuronal v2 (64-32, L2)...")
    nn_v2 = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        alpha=0.01,
        max_iter=600,
        random_state=42,
    )
    nn_v2.fit(X_train, y_train)

    return {
        "trivial": modelo_trivial,
        "simple_logistic": modelo_simple,
        "red_neuronal_v1": nn_v1,
        "red_neuronal_v2": nn_v2,
    }


def guardar_modelos(modelos, directorio=None):
    directorio = directorio or str(MODELOS_DIR)
    os.makedirs(directorio, exist_ok=True)
    for nombre, modelo in modelos.items():
        joblib.dump(modelo, os.path.join(directorio, f"{nombre}.pkl"))
    print(f"Modelos guardados en '{directorio}'.")


if __name__ == "__main__":
    from datos import cargar_datos, preparar_y_dividir_datos

    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    modelos = entrenar_lineas_base_y_redes(datos["X_train"], datos["y_train"])
    guardar_modelos(modelos)
