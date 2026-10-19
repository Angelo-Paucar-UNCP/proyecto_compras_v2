import json
from datetime import datetime

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
)

try:
    from .rutas import MODELOS_DIR, RUTA_MODELO_PRODUCCION, RUTA_UMBRAL
except ImportError:
    from rutas import MODELOS_DIR, RUTA_MODELO_PRODUCCION, RUTA_UMBRAL


def _json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def _predicciones(modelo, X, umbral=None):
    if umbral is None or not hasattr(modelo, "predict_proba"):
        return modelo.predict(X)
    proba = modelo.predict_proba(X)[:, 1]
    return (proba >= umbral).astype(int)


def evaluar_modelo(modelo, X, y, umbral=None):
    preds = _predicciones(modelo, X, umbral)
    metricas = {
        "f1_score": round(float(f1_score(y, preds, zero_division=0)), 4),
        "precision": round(float(precision_score(y, preds, zero_division=0)), 4),
        "recall": round(float(recall_score(y, preds, zero_division=0)), 4),
        "accuracy": round(float(accuracy_score(y, preds)), 4),
    }
    if hasattr(modelo, "predict_proba"):
        proba = modelo.predict_proba(X)[:, 1]
        metricas["pr_auc"] = round(float(average_precision_score(y, proba)), 4)
    return metricas


def elegir_umbral(modelo, X_val, y_val):
    """Elige el umbral en validación maximizando F1 (desbalance)."""
    if not hasattr(modelo, "predict_proba"):
        return 0.5
    proba = modelo.predict_proba(X_val)[:, 1]
    mejor_t, mejor_f1 = 0.5, -1.0
    for t in np.linspace(0.10, 0.90, 81):
        preds = (proba >= t).astype(int)
        f1 = f1_score(y_val, preds, zero_division=0)
        if f1 > mejor_f1:
            mejor_f1 = f1
            mejor_t = float(t)
    return round(mejor_t, 4)


def generar_ficha(nombre, modelo, metricas_val, umbral, metricas_test=None):
    params = modelo.get_params() if hasattr(modelo, "get_params") else {}
    ficha = {
        "modelo": nombre,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "datos_entrenamiento": "Online Shoppers Intention (70% train, 15% val, 15% test)",
        "umbral_decision": umbral,
        "parametros": _json_safe(params),
        "metricas_validacion": metricas_val,
    }
    if metricas_test:
        ficha["metricas_prueba"] = metricas_test
    return ficha


def evaluar_y_promover(datos, modelos):
    X_val, y_val = datos["X_val"], datos["y_val"]
    X_test, y_test = datos["X_test"], datos["y_test"]
    MODELOS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n--- EVALUACIÓN EN VALIDACIÓN (elección de umbral y modelo) ---")
    mejor_nombre = None
    mejor_f1 = -1
    umbrales = {}
    metricas_val_todas = {}

    for nombre, modelo in modelos.items():
        umbral = elegir_umbral(modelo, X_val, y_val)
        umbrales[nombre] = umbral
        metricas_val = evaluar_modelo(modelo, X_val, y_val, umbral)
        metricas_val_todas[nombre] = metricas_val
        print(
            f"[*] {nombre}: umbral={umbral}  F1={metricas_val['f1_score']}  "
            f"recall={metricas_val['recall']}  accuracy={metricas_val['accuracy']}"
        )
        if metricas_val["f1_score"] > mejor_f1:
            mejor_f1 = metricas_val["f1_score"]
            mejor_nombre = nombre

    print(f"\n>> Ganador en validación: {mejor_nombre} (F1={mejor_f1}) <<")

    ganador = modelos[mejor_nombre]
    umbral_ganador = umbrales[mejor_nombre]

    print(f"\n--- EVALUACIÓN FINAL EN PRUEBA ({mejor_nombre}) ---")
    metricas_test = evaluar_modelo(ganador, X_test, y_test, umbral_ganador)
    for met, val in metricas_test.items():
        print(f"- {met}: {val}")

    for nombre, modelo in modelos.items():
        if nombre == mejor_nombre:
            ficha = generar_ficha(
                nombre, modelo, metricas_val_todas[nombre], umbrales[nombre], metricas_test
            )
        else:
            ficha = generar_ficha(
                nombre, modelo, metricas_val_todas[nombre], umbrales[nombre]
            )
        with open(MODELOS_DIR / f"ficha_{nombre}.json", "w", encoding="utf-8") as f:
            json.dump(ficha, f, indent=4, ensure_ascii=False)

    joblib.dump(ganador, RUTA_MODELO_PRODUCCION)
    with open(RUTA_UMBRAL, "w", encoding="utf-8") as f:
        json.dump(
            {
                "modelo": mejor_nombre,
                "umbral": umbral_ganador,
                "criterio": "F1 en validación (clase positiva = compra)",
            },
            f,
            indent=4,
            ensure_ascii=False,
        )
    print(f"\nModelo promovido: {RUTA_MODELO_PRODUCCION}")
    print(f"Umbral guardado: {RUTA_UMBRAL}")
    return mejor_nombre, umbral_ganador, metricas_test


if __name__ == "__main__":
    from datos import cargar_datos, preparar_y_dividir_datos

    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    nombres = ["trivial", "simple_logistic", "red_neuronal_v1", "red_neuronal_v2"]
    modelos = {}
    for nombre in nombres:
        ruta = MODELOS_DIR / f"{nombre}.pkl"
        if ruta.exists():
            modelos[nombre] = joblib.load(ruta)
    if not modelos:
        raise SystemExit("No hay modelos en modelos/. Ejecuta python entrenar.py")
    evaluar_y_promover(datos, modelos)
