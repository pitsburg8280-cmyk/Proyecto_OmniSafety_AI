# Código fuente de OmniSafety AI

Organización de los módulos de la plataforma.

| Ruta | Contenido |
| --- | --- |
| `api/main.py` | API REST en FastAPI con verificación de estado y tres endpoints de inferencia |
| `dashboard/app.py` | Tablero de monitoreo en Streamlit con cinco pestañas |
| `vision/utils.py` | Utilidades de visión: normalización, filtrado, supresión no máxima y resumen |
| `timeseries/features.py` | Ingeniería de características y combinación del ensemble |
| `nlp/retrieval.py` | Fragmentación, similitud, BM25 y métricas de recuperación |
| `config.py` | Carga, validación y escritura de la configuración del sistema |
| `paths.py` | Rutas centralizadas del proyecto |

## Importaciones

Todos los módulos se importan de forma explícita desde la raíz del proyecto:

```python
from src import config, paths
from src.timeseries.features import puntuacion_riesgo
from src.nlp import retrieval
from src.vision import utils
```

## Ejecución

```bash
# API REST
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Tablero
streamlit run src/dashboard/app.py --server.port 8501
```

## Pruebas

```bash
pytest -v
```
