from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODELOS_DIR = ROOT / "modelos"
DOCS_DIR = ROOT / "docs"

RUTA_CSV = DATA_DIR / "online_shoppers_intention.csv"
RUTA_PREPROCESADOR = MODELOS_DIR / "preprocesador.joblib"
RUTA_MODELO_PRODUCCION = MODELOS_DIR / "modelo_produccion.pkl"
RUTA_UMBRAL = MODELOS_DIR / "umbral.json"
RUTA_DEFAULTS = MODELOS_DIR / "valores_por_defecto.json"
