import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import numpy as np

# Configuración visual estilo Seaborn para que se vea profesional en la PPT
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

def generar_graficos_teoricos():
    print("Cargando datos y modelo...")
    _, _, X_test, _, _, y_test = joblib.load("modelos/datos_procesados.pkl")
    modelo = joblib.load("modelos/modelo_produccion.pkl")
    
    y_pred_probs = modelo.predict_proba(X_test)[:, 1]

    # ==========================================
    # GRÁFICO 1: Curva de Pérdida (Aplica Notebooks 2 y 5)
    # Demuestra que la red neuronal convergió y no tiene overfitting
    # ==========================================
    if hasattr(modelo, 'loss_curve_'):
        plt.figure()
        plt.plot(modelo.loss_curve_, color="#1F3864", linewidth=2.5)
        plt.title("Curva de Pérdida (Loss) durante el Entrenamiento (Notebook 5)", fontsize=14)
        plt.xlabel("Épocas (Iteraciones)")
        plt.ylabel("Pérdida (Log-Loss)")
        plt.tight_layout()
        plt.savefig("docs/curva_perdida.png", dpi=300)
        print("✅ Generado: docs/curva_perdida.png")
        plt.close()

    # ==========================================
    # GRÁFICO 2: Curva ROC y AUC (Aplica Notebook 6)
    # Demuestra la capacidad de separar compradores de abandonos
    # ==========================================
    fpr, tpr, umbrales = roc_curve(y_test, y_pred_probs)
    area = auc(fpr, tpr)
    
    plt.figure()
    plt.plot(fpr, tpr, color="crimson", linewidth=2.5, label=f"Modelo Producción (AUC = {area:.3f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--", label="Azar (AUC = 0.5)")
    plt.title("Curva ROC (Notebook 6)", fontsize=14)
    plt.xlabel("Tasa de Falsos Positivos")
    plt.ylabel("Tasa de Verdaderos Positivos")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("docs/curva_roc.png", dpi=300)
    print("✅ Generado: docs/curva_roc.png")
    plt.close()

    # ==========================================
    # GRÁFICO 3: Curva Precisión-Recall (Aplica Notebook 6)
    # Ideal para justificar datos desbalanceados
    # ==========================================
    precisiones, recalls, umbrales_pr = precision_recall_curve(y_test, y_pred_probs)
    
    plt.figure()
    plt.plot(recalls[:-1], precisiones[:-1], color="#2E7D32", linewidth=2.5)
    plt.title("Curva Precisión-Recall (Notebook 6)", fontsize=14)
    plt.xlabel("Recall (Sensibilidad)")
    plt.ylabel("Precisión")
    plt.tight_layout()
    plt.savefig("docs/curva_pr.png", dpi=300)
    print("✅ Generado: docs/curva_pr.png")
    plt.close()

if __name__ == "__main__":
    generar_graficos_teoricos()