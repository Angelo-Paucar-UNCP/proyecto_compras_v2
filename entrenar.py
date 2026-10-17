import os

print("Iniciando pipeline de entrenamiento completo...")
# 1. Preparar datos
os.system("python src/datos.py")
# 2. Entrenar modelos
os.system("python src/modelo.py")
# 3. Evaluar y promover ganador
os.system("python src/evaluacion.py")
print("Pipeline finalizado. Revisa la carpeta 'modelos/'.")