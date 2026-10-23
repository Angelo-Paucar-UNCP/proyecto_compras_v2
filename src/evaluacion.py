import joblib
import json
import os
import shutil
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

def evaluar_y_promover():
    print("Iniciando fase de evaluación y promoción...")
    
    # 1. Cargar el conjunto de PRUEBA
    _, _, X_test, _, _, y_test = joblib.load("modelos/datos_procesados.pkl")
    
    # 2. Leer las fichas de validación para elegir al mejor
    mejor_f1 = -1
    mejor_modelo_nombre = None
    
    for archivo in os.listdir("modelos"):
        if archivo.startswith("ficha_") and archivo.endswith(".json"):
            with open(f"modelos/{archivo}", "r") as f:
                ficha = json.load(f)
                f1_val = ficha["metricas_validacion"]["f1_score"]
                
                if f1_val > mejor_f1:
                    mejor_f1 = f1_val
                    mejor_modelo_nombre = ficha["modelo"]
                    
    print(f"🏆 Modelo ganador en Validación: {mejor_modelo_nombre} (F1: {mejor_f1:.4f})")
    
    # 3. Evaluar al ganador en el conjunto de Prueba (Solo una vez)
    modelo_ganador = joblib.load(f"modelos/{mejor_modelo_nombre}.pkl")
    y_pred_test = modelo_ganador.predict(X_test)
    
    print("\n--- MÉTRICAS FINALES EN PRUEBA (Criterio C4) ---")
    print(f"F1-Score:  {f1_score(y_test, y_pred_test, zero_division=0):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred_test, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred_test, zero_division=0):.4f}")
    
    # 4. Promover a Producción (Para que la API lo consuma)
    shutil.copy(f"modelos/{mejor_modelo_nombre}.pkl", "modelos/modelo_produccion.pkl")
    print("✅ Modelo promovido exitosamente a 'modelo_produccion.pkl'")

if __name__ == "__main__":
    evaluar_y_promover()