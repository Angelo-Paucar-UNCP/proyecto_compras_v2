import os
import json
import joblib
from datetime import datetime
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

from datos import cargar_datos, preparar_y_dividir_datos

def evaluar_modelo(modelo, X, y):
    """Calcula métricas robustas para problemas con desbalance de clases."""
    preds = modelo.predict(X)
    return {
        "f1_score": round(f1_score(y, preds, zero_division=0), 4),
        "precision": round(precision_score(y, preds, zero_division=0), 4),
        "recall": round(recall_score(y, preds, zero_division=0), 4),
        "accuracy": round(accuracy_score(y, preds), 4)
    }

def generar_ficha(nombre, modelo, metricas_val, metricas_test=None):
    """Genera la estructura de la ficha JSON para cumplir la Etapa E4."""
    # Extraemos los hiperparámetros si el modelo lo permite
    params = modelo.get_params() if hasattr(modelo, 'get_params') else "No disponible"
    
    ficha = {
        "modelo": nombre,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "datos_entrenamiento": "Online Shoppers Intention (70% train, 15% val, 15% test)",
        "parametros": params,
        "metricas_validacion": metricas_val
    }
    
    # Solo el modelo ganador tendrá métricas de prueba
    if metricas_test:
        ficha["metricas_prueba"] = metricas_test
        
    return ficha

if __name__ == "__main__":
    print("Cargando datos procesados...")
    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    X_val, y_val = datos['X_val'], datos['y_val']
    X_test, y_test = datos['X_test'], datos['y_test']
    
    nombres_modelos = ["trivial", "simple_logistic", "red_neuronal_v1", "red_neuronal_v2"]
    modelos_cargados = {}
    metricas_validacion_todas = {}
    
    # 1. Evaluar a todos SOLO en validación (Evitar fuga)
    print("\n--- EVALUACIÓN EN VALIDACIÓN ---")
    mejor_f1 = -1
    mejor_modelo_nombre = ""
    
    for nombre in nombres_modelos:
        ruta_modelo = f"modelos/{nombre}.pkl"
        if os.path.exists(ruta_modelo):
            modelo = joblib.load(ruta_modelo)
            modelos_cargados[nombre] = modelo
            
            metricas_val = evaluar_modelo(modelo, X_val, y_val)
            metricas_validacion_todas[nombre] = metricas_val
            
            print(f"[*] {nombre}: F1-Score = {metricas_val['f1_score']}")
            
            # Decidimos el ganador basados estrictamente en validación
            if metricas_val['f1_score'] > mejor_f1:
                mejor_f1 = metricas_val['f1_score']
                mejor_modelo_nombre = nombre

    print(f"\n>> ¡El modelo GANADOR en validación es: {mejor_modelo_nombre.upper()}! <<")
    
    # 2. Evaluación única en prueba y generación de fichas JSON
    for nombre, modelo in modelos_cargados.items():
        metricas_val = metricas_validacion_todas[nombre]
        
        if nombre == mejor_modelo_nombre:
            print(f"\n--- EVALUACIÓN FINAL EN PRUEBA ({nombre}) ---")
            # ¡Aquí y solo aquí tocamos los datos de prueba!
            metricas_test = evaluar_modelo(modelo, X_test, y_test)
            for met, val in metricas_test.items():
                print(f"- {met}: {val}")
            
            ficha = generar_ficha(nombre, modelo, metricas_val, metricas_test)
            
            # Promover el modelo elegido copiándolo como 'modelo_produccion.pkl'
            joblib.dump(modelo, "modelos/modelo_produccion.pkl")
            print("\n[+] Modelo promovido a 'modelos/modelo_produccion.pkl'")
        else:
            # Los modelos perdedores no tocan el conjunto de prueba
            ficha = generar_ficha(nombre, modelo, metricas_val)
            
        # Guardamos la ficha física en formato JSON
        ruta_json = f"modelos/ficha_{nombre}.json"
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(ficha, f, indent=4)
        
    print("\n¡Etapa E4 completada exitosamente! Revisa tu carpeta 'modelos/'.")