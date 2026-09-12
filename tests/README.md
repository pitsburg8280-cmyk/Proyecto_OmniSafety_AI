# Pruebas automatizadas

Suite de pruebas unitarias y de integración del proyecto.

| Archivo | Cobertura |
| --- | --- |
| `test_api.py` | Endpoints de la API, validación de entrada y formato de respuestas |
| `test_vision.py` | Normalización, filtrado por confianza, supresión no máxima y resumen |
| `test_timeseries.py` | Estadísticas de ventana, entropía, tasas de cambio y combinación del ensemble |
| `test_nlp.py` | Fragmentación, similitud coseno, BM25 y métricas de recuperación |
| `test_config.py` | Rutas centralizadas y carga y escritura de la configuración |

## Ejecución

```bash
# Todas las pruebas
pytest -v

# Un archivo específico
pytest tests/test_vision.py -v

# Con medición de cobertura
pytest --cov=src --cov-report=term-missing
```

## Dependencias

```bash
pip install pytest pytest-cov
```
