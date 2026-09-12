# Herramientas de documentación

Scripts auxiliares para generar las ilustraciones y construir el documento académico. No forman parte del sistema en producción.

| Script | Función | Salida |
| --- | --- | --- |
| `generate_figures.py` | Genera las once ilustraciones del documento | `docs/figuras/*.png` |
| `build_docx.py` | Construye el documento DOCX a partir del texto fuente | `docs/entregables/OmniSafety_AI_Documento_APA.docx` |

## Ejecución

Ambos scripts resuelven las rutas a través de `src/paths.py`, por lo que pueden ejecutarse desde la raíz del proyecto o desde esta carpeta.

```bash
# Regenerar las ilustraciones
python tools/generate_figures.py

# Regenerar el documento DOCX
python tools/build_docx.py
```

## Marcadores del archivo fuente

El documento se escribe en `docs/entregables/OmniSafety_AI_Documento_APA.txt` usando marcadores que `build_docx.py` interpreta:

| Marcador | Efecto |
| --- | --- |
| `[CUBIERTA] ... [FIN_CUBIERTA]` | Portada con líneas centradas |
| `[PAGINA]` | Salto de página |
| `[INDICE]` | Índice automático de Word |
| `[H1]`, `[H2]`, `[H3]` | Títulos de nivel 1, 2 y 3 |
| `[TABLA] N \| Título` | Tabla; las filas comienzan con `\|` |
| `[FIGURA] archivo.png \| Título` | Ilustración desde `docs/figuras/` |
| `[NOTA] texto` | Nota al pie de tabla o figura |
| `[MONO] texto` | Bloque de código con fondo gris |
| `[REF] texto` | Referencia con sangría francesa |

## Dependencias

```bash
pip install python-docx matplotlib numpy
```
