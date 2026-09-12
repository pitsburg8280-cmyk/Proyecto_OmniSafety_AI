# Documentación y entregables

| Ruta | Contenido |
| --- | --- |
| `entregables/OmniSafety_AI_Documento_APA.docx` | Documento académico en Word, listo para entrega |
| `entregables/OmniSafety_AI_Documento_APA.txt` | Fuente editable del documento con marcadores de formato |
| `figuras/` | Once ilustraciones generadas a 150 ppp |
| `respaldos/` | Versiones anteriores conservadas como referencia |

## Regenerar los entregables

```bash
python tools/generate_figures.py
python tools/build_docx.py
```

El documento final contiene 24 tablas, 11 ilustraciones, referencias en formato APA 7.ª edición y cuatro apéndices orientados a la reproducibilidad.

## Notas

- El archivo `.docx` se regenera por completo en cada ejecución. No deben hacerse ediciones manuales sobre él, ya que se perderían.
- Para modificar el contenido, edita el archivo `.txt` y vuelve a ejecutar `build_docx.py`.
- Al abrir el `.docx` en Word, pulsa `F9` sobre el índice para actualizar la tabla de contenido.
