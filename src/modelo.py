import joblib
import json
import os
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from datetime import datetime

def entrenar_modelos():
    print("Iniciando entrenamiento iterativo de modelos...")
    
    # 1. Cargar datos previamente procesados (sin fuga)
    ruta_datos = "modelos/datos_procesados.pkl"
    if not os.path.exists(ruta_datos):
        raise FileNotFoundError("Faltan los datos procesados. Ejecuta datos.py primero.")
        
    X_train, X_val, _, y_train, y_val, _ = joblib.load(ruta_datos)
    
    # 2. Definir los modelos exigidos por la rúbrica C3
    modelos = {
        "trivial": DummyClassifier(strategy="most_frequent"),
        "simple_logistic": LogisticRegression(max_iter=1000, random_state=42),
        "red_neuronal_v1": MLPClassifier(hidden_layer_sizes=(50,), max_iter=500, random_state=42),
        "red_neuronal_v2": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, early_stopping=True, random_state=42)
    }
    
    os.makedirs("modelos", exist_ok=True)
    
    # 3. Entrenar y evaluar SOLO en validación
    for nombre, modelo in modelos.items():
        print(f"Entrenando modelo: {nombre}...")
        modelo.fit(X_train, y_train)
        
        y_pred_val = modelo.predict(X_val)
        
        joblib.dump(modelo, f"modelos/{nombre}.pkl")
        
        ficha = {
            "modelo": nombre,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metricas_validacion": {
                "accuracy": accuracy_score(y_val, y_pred_val),
                "precision": precision_score(y_val, y_pred_val, zero_division=0),
                "recall": recall_score(y_val, y_pred_val, zero_division=0),
                "f1_score": f1_score(y_val, y_pred_val, zero_division=0)
            }
        }
        
        with open(f"modelos/ficha_{nombre}.json", "w") as f:
            json.dump(ficha, f, indent=4)
            
        print(f"✅ {nombre} guardado (F1-Score Validación: {ficha['metricas_validacion']['f1_score']:.4f})")

if __name__ == "__main__":
    entrenar_modelos()