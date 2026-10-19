import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from datos import cargar_datos, guardar_artefactos_datos, preparar_y_dividir_datos
from evaluacion import evaluar_y_promover
from modelo import entrenar_lineas_base_y_redes, guardar_modelos


def main():
    print("Iniciando pipeline de entrenamiento...")
    df = cargar_datos()
    datos = preparar_y_dividir_datos(df)
    guardar_artefactos_datos(datos)
    modelos = entrenar_lineas_base_y_redes(datos["X_train"], datos["y_train"])
    guardar_modelos(modelos)
    evaluar_y_promover(datos, modelos)
    print("Pipeline finalizado. Revisa la carpeta modelos/.")


if __name__ == "__main__":
    main()
