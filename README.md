# Proyecto grupo 5: predicción de intención de compra online

Sistema de punta a punta para el dataset **Online Shoppers Purchasing Intention** (UCI, 12 330 sesiones). Predice si una sesión terminará en compra (`Revenue`) para apoyar un descuento en tiempo real.

Cita: Sakar, C. Okan; Kastro, Yomi (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. DOI: [10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q). ID 468.

## Requisitos

- Python 3.10 o superior

## Instalación desde cero

```powershell
git clone https://github.com/Angelo-Paucar-UNCP/proyecto_compras_v2.git
cd proyecto_compras_v2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

El CSV **no** va en GitHub. `python entrenar.py` lo descarga solo la primera vez a `data/online_shoppers_intention.csv`.

## Entrenar

Desde la raíz del proyecto:

```powershell
python entrenar.py
```

Eso parte los datos (70/15/15, estratificado), ajusta el preprocesador solo con entrenamiento, entrena la línea base y dos redes, elige umbral y ganador **solo en validación**, evalúa el ganador **una vez** en prueba y deja artefactos en `modelos/`.

## API

```powershell
uvicorn src.api:app --reload
```

- Salud: `GET http://127.0.0.1:8000/health`
- Predicción: `POST http://127.0.0.1:8000/predecir` con `{"datos": { ... 17 campos ... }}`
- Entrada inválida: código **400**

## Chatbot

Con la API encendida, en otra terminal:

```powershell
python src/chatbot.py
```

Escribe `ayuda` en cualquier momento para hablar con un humano.

## Pruebas

```powershell
pytest tests/ -v
```

## Estructura

```
proyecto_compras_v2/
├── README.md
├── requirements.txt
├── entrenar.py
├── src/
├── tests/
├── modelos/          # fichas JSON; los .pkl se generan al entrenar
├── docs/             # diagrama del chatbot y figuras
├── notebooks/        # exploración
└── informe.pdf
```
