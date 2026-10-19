# Informe técnico — Predicción de intención de compra online

**Asignatura:** Tecnologías Emergentes (ISO46B)  
**Grupo 5 — Dataset 3**  
**Entrega:** 19/10/2026

## 1. Planteamiento

El sistema predice si una sesión de comercio electrónico terminará en compra (`Revenue = True`). El usuario del sistema es el equipo de marketing o de conversión: necesita decidir, **durante** la visita, si vale la pena ofrecer un incentivo (cupón) antes de que la persona cierre la pestaña.

La predicción se hace con datos de la sesión en curso: páginas vistas, tiempos, tipo de visitante, mes, fin de semana, tasas de rebote/salida y valor de páginas ya visitadas. No se usa información posterior al checkout.

Error más costoso: **falso negativo** (iba a abandonar y no se detecta) implica una venta perdida; el **falso positivo** gasta un descuento en alguien que ya iba a pagar. En este negocio la venta perdida suele pesar más, por eso no nos guiamos por accuracy. La métrica principal es **F1 de la clase compra**, complementada con recall, precision y PR-AUC. El umbral se elige en validación maximizando F1.

## 2. Datos y exploración

Fuente: Sakar, C. Okan; Kastro, Yomi (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. DOI 10.24432/C5F88Q. 12 330 sesiones, 17 atributos + `Revenue`.

Calidad: no hay nulos. La clase positiva es ~15,5 % (desbalance). `Month` usa la etiqueta `June` (no `Jun`). Enteros como región o tipo de tráfico se tratan como numéricos.

**Fuga:** no se usa el resultado de la compra como entrada. `PageValues` es el valor medio de páginas **ya** visitadas en la sesión; se conoce en el momento de decidir y se conserva. El chatbot no pregunta esa variable: rellena la mediana de entrenamiento cuando el usuario no la aporta.

Partición estratificada 70 % / 15 % / 15 %. `StandardScaler` y `OneHotEncoder` se ajustan **solo** con entrenamiento (`src/datos.py`).

## 3. Modelado

| Modelo | Idea |
|---|---|
| Trivial | Clase mayoritaria (siempre “no compra”) |
| Simple | Regresión logística con `class_weight=balanced` |
| Red v1 | MLP, una capa oculta (32) |
| Red v2 | MLP, dos capas (64-32) y L2 (`alpha=0.01`) |

La línea trivial deja accuracy 0,845 y F1 0: demuestra que accuracy no sirve. En validación, con umbral propio, la **regresión logística ganó a las dos redes** (F1 0,631 vs 0,610 y 0,566). Se promueve la logística: un modelo más simple y mejor en la métrica acordada.

## 4. Evaluación y versionado

Para cada modelo se busca un umbral en `[0.10, 0.90]` que maximice F1 **en validación**. El ganador se elige solo con esas métricas. El conjunto de prueba se mira **una vez**, solo para el promovido.

Resultado de validación (F1): trivial 0,00 (umbral irrelevante); logística 0,631 (umbral 0,55); red v1 0,610 (0,21); red v2 0,566 (0,26).

Prueba única del ganador: F1 0,640; precision 0,578; recall 0,717; accuracy 0,875; PR-AUC 0,622.

Cada versión tiene ficha JSON en `modelos/`. El ganador se copia a `modelo_produccion.pkl` y el umbral a `umbral.json`.

## 5. API

FastAPI carga el modelo promovido, el preprocesador y el umbral. `GET /health` indica si el modelo está en memoria. `POST /predecir` valida los 17 campos (`src/preprocesamiento_api.py`): tipos, rangos, mes y tipo de visitante. Error de negocio → **400**. Si falta el modelo → 503. Responde clase, probabilidad de compra y umbral usado.

## 6. Chatbot

Flujo en `docs/flujo_chatbot.png`. Recolecta slots (visitante, páginas de producto, minutos, fin de semana, mes), completa el resto con medianas/modas de train, llama a la API y habla en lenguaje no técnico: cupón si predice abandono, o invitación a caja si predice compra. Fallback a los 3 intentos inválidos. Palabras `ayuda`, `humano`, `asesor` o `salir` derivan a una persona. Si la API no responde, también deriva.

## 7. Limitaciones y ética

### 7.1. Limitaciones del modelo

El modelo se ha desarrollado utilizando el conjunto de datos *Online Shoppers Purchasing Intention Dataset*, publicado en 2018. Por ello, sus resultados pueden no representar el comportamiento actual de todos los usuarios de comercio electrónico ni generalizarse a otras plataformas. Antes de utilizarlo en un entorno real, sería necesario evaluar su rendimiento con datos recientes del sitio web donde se implementaría.

Además, el modelo puede cometer falsos positivos y falsos negativos. Un falso positivo puede ocasionar que se ofrezca un cupón innecesario, mientras que un falso negativo puede impedir que se ofrezca un incentivo a un visitante que lo habría necesitado. La elección del umbral busca equilibrar estos errores mediante las métricas definidas para el proyecto, pero no los elimina por completo.

### 7.2. Equidad y posibles sesgos

Las variables relacionadas con la región, el sistema operativo y el tipo de tráfico pueden reflejar diferencias entre grupos de usuarios. Si el modelo presenta un rendimiento desigual entre visitantes nuevos y recurrentes, por ejemplo, algunas personas podrían recibir ofertas con menor frecuencia que otras.

Por esta razón, se recomienda evaluar las métricas de precisión y recall por tipo de visitante y condición de fin de semana. Estas comprobaciones permitirían identificar diferencias de rendimiento antes de considerar un despliegue real. No se afirma que exista un sesgo demostrado, ya que sería necesario realizar dicha evaluación.

### 7.3. Privacidad y uso responsable de los datos

La información de navegación debe utilizarse únicamente para la finalidad prevista y de acuerdo con las políticas de privacidad aplicables. En una implementación real, sería necesario revisar qué datos se recopilan, cuánto tiempo se conservan, quién puede acceder a ellos y qué medidas de seguridad se aplican.

Asimismo, se recomienda evitar la recopilación de información personal que no sea necesaria para la predicción y proteger los registros de las sesiones frente a accesos no autorizados.

### 7.4. Supervisión humana y uso de los resultados

Las predicciones deben considerarse estimaciones y no certezas sobre la intención de compra de una persona. El sistema puede servir como apoyo para las decisiones de marketing, pero no debería ser el único criterio para determinar qué usuarios reciben beneficios o descuentos.

Si se detectan errores recurrentes, diferencias importantes entre grupos o una disminución del rendimiento, será necesario revisar el modelo y valorar si corresponde actualizarlo. La atención humana debe mantenerse disponible para resolver consultas, reclamaciones y situaciones que el sistema no pueda gestionar adecuadamente.

En conclusión, el modelo constituye una herramienta de apoyo a la toma de decisiones. Su utilización responsable requiere verificar periódicamente su rendimiento, proteger los datos y reconocer sus limitaciones.

+
## Declaración de uso de herramientas de IA

Se usó Cursor (asistente de código) para estructurar el repositorio, validar entradas de la API, el pipeline de umbral y el diagrama del chatbot. Se verificó a mano: descarga UCI, columnas reales, que el test no se usa para elegir modelo, respuestas 400, y el flujo del chatbot con frases inválidas. Las métricas que se reportan son las que imprime `python entrenar.py`.
