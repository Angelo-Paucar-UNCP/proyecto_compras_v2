import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

def generar_matriz_y_errores():
    print("Cargando modelo y datos de prueba...")
    # Cargar los datos procesados y el modelo ganador
    _, _, X_test, _, _, y_test = joblib.load("modelos/datos_procesados.pkl")
    modelo = joblib.load("modelos/modelo_produccion.pkl")

    # Hacer predicciones
    y_pred = modelo.predict(X_test)

    # 1. GENERAR MATRIZ DE CONFUSIÓN
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, 
        display_labels=["Abandono (0)", "Compra (1)"]
    )
    
    # Configurar el gráfico con estilo profesional
    fig, ax = plt.subplots(figsize=(7, 5))
    disp.plot(cmap="Blues", ax=ax, values_format="d")
    plt.title("Matriz de Confusión - Conjunto de Prueba", fontsize=14)
    plt.tight_layout()
    
    # Guardar como imagen para el PowerPoint
    plt.savefig("matriz_confusion.png", dpi=300)
    print("✅ Matriz de confusión guardada exitosamente como 'matriz_confusion.png'")

    # 2. ANÁLISIS DE ERRORES (Falsos Positivos y Falsos Negativos)
    verdaderos_negativos, falsos_positivos, falsos_negativos, verdaderos_positivos = cm.ravel()
    
    print("\n" + "="*50)
    print("📊 INTERPRETACIÓN DE ERRORES PARA EL NEGOCIO (B2B)")
    print("="*50)
    
    print(f"✔️ Aciertos Totales: {verdaderos_negativos + verdaderos_positivos}")
    print(f"❌ Errores Totales: {falsos_positivos + falsos_negativos}\n")
    
    print(f"🔴 Falsos Positivos ({falsos_positivos} casos):")
    print("   El modelo predijo COMPRA (1), pero el cliente ABANDONÓ (0).")
    print("   Consecuencia B2B: El sistema no hizo nada y perdimos la venta.\n")
    
    print(f"🟡 Falsos Negativos ({falsos_negativos} casos):")
    print("   El modelo predijo ABANDONO (0), pero el cliente SÍ IBA A COMPRAR (1).")
    print("   Consecuencia B2B: El sistema le regaló un descuento del 15% a alguien")
    print("   que iba a comprar de todos modos (pérdida de margen).")
    print("="*50 + "\n")

if __name__ == "__main__":
    generar_matriz_y_errores()