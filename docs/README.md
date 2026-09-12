# Documentación y entregables

## Entregable

El único entregable del proyecto es el documento académico en PDF.

| Ruta | Contenido |
| --- | --- |
| `entregables/OmniSafety_AI_Documento_APA.pdf` | Documento académico APA 7.ª edición, listo para entrega |

## Material de apoyo

Estos directorios complementan al documento, pero no forman parte del entregable.

| Ruta | Contenido |
| --- | --- |
| `figuras/` | Once ilustraciones generadas a 150 ppp |
| `respaldos/` | Versiones anteriores conservadas como referencia |

## Regenerar las ilustraciones

```bash
python tools/generate_figures.py
```

El documento contiene 24 tablas, 11 ilustraciones, referencias en formato APA 7.ª edición y cuatro apéndices orientados a la reproducibilidad.

## Notas

- El PDF es el artefacto final y no se regenera desde el repositorio.
- Para generar una versión editable en Word existe la herramienta opcional `tools/build_docx.py`, que requiere el archivo fuente `entregables/OmniSafety_AI_Documento_APA.txt`. Ese `.txt` no se distribuye en el repositorio; se conserva en `respaldos/`.
- El `.docx` se regenera por completo en cada ejecución: no hagas ediciones manuales sobre él, ya que se perderían.
- Al abrir el `.docx` en Word, pulsa `F9` sobre el índice para actualizar la tabla de contenido.
