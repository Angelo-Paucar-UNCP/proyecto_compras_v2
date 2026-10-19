# Proyecto grupo 5: predicción de intención de compra online

Sistema de punta a punta para el dataset **Online Shoppers Purchasing Intention** (UCI, 12 330 sesiones). Predice si una sesión terminará en compra (`Revenue`) para apoyar decisiones relacionadas con la conversión.

**Referencia del dataset:** Sakar, C. Okan; Kastro, Yomi (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. DOI: [10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q). ID 468.

## Requisitos

- Python 3.10 o superior.
- Git.
- Dependencias indicadas en `requirements.txt`.

## Instalación desde cero

Clona el repositorio y entra en la carpeta:

```powershell
git clone https://github.com/Angelo-Paucar-UNCP/proyecto_compras_v2.git
cd proyecto_compras_v2
```

Crea y activa un entorno virtual en Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

El archivo CSV del dataset no se incluye en GitHub. El programa de entrenamiento se encarga de descargarlo si no está disponible localmente.

## Entrenamiento

Desde la raíz del proyecto, ejecuta:

```powershell
python entrenar.py
```

El proceso utiliza una partición estratificada de los datos: 70 % para entrenamiento, 15 % para validación y 15 % para prueba. El preprocesador se ajusta con los datos de entrenamiento. La selección del modelo y del umbral se realiza con validación; la evaluación final se realiza sobre el conjunto de prueba.

Los artefactos generados se guardan en `modelos/`.

**Nota:** este comando vuelve a ejecutar el entrenamiento y puede modificar los artefactos existentes. No es necesario ejecutarlo para iniciar la API si los archivos de modelos requeridos ya están disponibles.

## API

Desde la raíz del proyecto, inicia el servidor:

```powershell
python -m uvicorn src.api:app --reload --port 8001
```

La API utiliza los siguientes endpoints:

- **Estado del servicio:** `GET http://127.0.0.1:8001/health`
- **Predicción:** `POST http://127.0.0.1:8001/predecir`

El endpoint de predicción recibe un objeto JSON con la clave `datos`, que contiene los 17 campos esperados por el modelo.

Ejemplo de estructura de solicitud:

```json
{
  "datos": {
    "Administrative": 1,
    "Administrative_Duration": 8,
    "Informational": 0,
    "Informational_Duration": 0,
    "ProductRelated": 18,
    "ProductRelated_Duration": 596.0833333,
    "BounceRates": 0.002898551,
    "ExitRates": 0.025012117,
    "PageValues": 0,
    "SpecialDay": 0,
    "Month": "May",
    "OperatingSystems": 2,
    "Browser": 2,
    "Region": 3,
    "TrafficType": 2,
    "VisitorType": "Returning_Visitor",
    "Weekend": false
  }
}
```

Los valores del ejemplo son ilustrativos y no representan una predicción garantizada.

Las entradas inválidas se gestionan mediante respuestas HTTP de error según la implementación de la API. El servicio también dispone de un endpoint de salud y contempla la ausencia de archivos de modelo.

## Chatbot

Con la API en funcionamiento, abre otra terminal, activa el entorno virtual y ejecuta:

```powershell
python src/chatbot.py
```

El chatbot permite interactuar con el usuario, gestionar entradas no válidas y ofrecer una derivación a atención humana. El comando `ayuda` permite solicitar asistencia; también se contemplan opciones de derivación y salida según el flujo implementado.

## Pruebas

Desde la raíz del proyecto y con el entorno virtual activo, ejecuta:

```powershell
python -m pytest tests -v
```

Las pruebas verifican componentes de la API, el sistema y el flujo del chatbot.

## Estructura del proyecto

```text
proyecto_compras_v2/
├── README.md
├── requirements.txt
├── entrenar.py
├── informe.md
├── informe.pdf
├── informe_tecnico_E5.docx
├── declaracion_uso_IA.docx
├── data/
├── docs/
│   ├── flujo_chatbot.png
│   └── generar_diagrama.py
├── modelos/
│   ├── modelo_produccion.pkl
│   ├── preprocesador.joblib
│   ├── umbral.json
│   └── fichas JSON y otros modelos
├── notebooks/
│   └── exploracion.ipynb
├── src/
│   ├── api.py
│   ├── chatbot.py
│   ├── datos.py
│   ├── evaluacion.py
│   ├── modelo.py
│   ├── preprocesamiento_api.py
│   └── rutas.py
└── tests/
    ├── test_api.py
    ├── test_chatbot.py
    └── test_sistema.py
```

## Consideraciones

- No se incluye el dataset CSV en el repositorio.
- Los archivos de modelos y el preprocesador deben corresponder al código y a la configuración utilizada por la API.
- Las métricas de evaluación deben interpretarse teniendo en cuenta el desequilibrio entre sesiones con compra y sin compra.
- `PageValues` puede influir fuertemente en la predicción; por ello, debe considerarse su disponibilidad real al momento de utilizar el sistema.
- El dataset corresponde a información histórica y sus resultados no garantizan el mismo rendimiento en otros periodos o poblaciones.
