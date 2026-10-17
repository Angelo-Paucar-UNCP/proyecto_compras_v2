import os
import joblib
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

def entrenar_lineas_base_y_redes(X_train, y_train):
    """
    Entrena los modelos requeridos:
    1. Modelo trivial (línea base)
    2. Modelo simple (Regresión Logística)
    3. Red Neuronal Versión 1 (1 capa oculta)
    4. Red Neuronal Versión 2 (2 capas ocultas con regularización)
    """
    print("Entrenando Modelo Trivial...")
    modelo_trivial = DummyClassifier(strategy="most_frequent", random_state=42)
    modelo_trivial.fit(X_train, y_train)

    print("Entrenando Modelo Simple (Regresión Logística)...")
    modelo_simple = LogisticRegression(max_iter=1000, random_state=42)
    modelo_simple.fit(X_train, y_train)

    print("Entrenando Red Neuronal - Versión 1 (32 neuronas)...")
    nn_v1 = MLPClassifier(hidden_layer_sizes=(32,), activation='relu', max_iter=300, random_state=42)
    nn_v1.fit(X_train, y_train)

    print("Entrenando Red Neuronal - Versión 2 (64 y 32 neuronas)...")
    nn_v2 = MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', alpha=0.01, max_iter=500, random_state=42)
    nn_v2.fit(X_train, y_train)

    modelos = {
        "trivial": modelo_trivial,
        "simple_logistic": modelo_simple,
        "red_neuronal_v1": nn_v1,
        "red_neuronal_v2": nn_v2
    }

    return modelos

def guardar_modelos(modelos, directorio="modelos"):
    """
    Guarda los modelos entrenados en la carpeta 'modelos/'
    """
    os.makedirs(directorio, exist_ok=True)
    for nombre, modelo in modelos.items():
        ruta = os.path.join(directorio, f"{nombre}.pkl")
        joblib.dump(modelo, ruta)
    print(f"¡Modelos guardados exitosamente en la carpeta '{directorio}/'!")

if __name__ == "__main__":
    from datos import cargar_datos, preparar_y_dividir_datos
    
    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    
    modelos_entrenados = entrenar_lineas_base_y_redes(datos['X_train'], datos['y_train'])
    guardar_modelos(modelos_entrenados)