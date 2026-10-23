import subprocess
import sys
import os

def ejecutar_script(ruta_script, descripcion):
    print(f"\n{'-'*60}\n🚀 Ejecutando: {descripcion} ({ruta_script})\n{'-'*60}")
    if not os.path.exists(ruta_script):
        print(f"❌ Error: No se encontró el archivo '{ruta_script}'.")
        sys.exit(1)
    
    resultado = subprocess.run([sys.executable, ruta_script])
    if resultado.returncode != 0:
        print(f"❌ Error crítico al ejecutar {ruta_script}. Abortando pipeline.")
        sys.exit(1)
    else:
        print(f"✅ {descripcion} completado con éxito.")

def main():
    print("\n" + "="*60 + "\n⚙️ INICIANDO PIPELINE DE ENTRENAMIENTO COMPLETO (B2B)\n" + "="*60)
    
    ejecutar_script("src/datos.py", "Fase 1: Preparación de datos y prevención de fuga")
    ejecutar_script("src/modelo.py", "Fase 2: Entrenamiento iterativo de modelos")
    ejecutar_script("src/evaluacion.py", "Fase 3: Evaluación y promoción del modelo ganador")
    
    print("\n" + "="*60 + "\n🎉 PIPELINE FINALIZADO CORRECTAMENTE.")
    print("Todos los artefactos están listos en la carpeta 'modelos/'.")
    print("👉 Ya puedes levantar la API con: uvicorn src.api:app --port 8001 --reload\n" + "="*60)

if __name__ == "__main__":
    main()