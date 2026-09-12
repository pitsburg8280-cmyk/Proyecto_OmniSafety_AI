# -*- coding: utf-8 -*-
"""Rutas centralizadas del proyecto OmniSafety AI.

Todos los módulos y herramientas deben resolver rutas a través de este archivo
para que la reorganización de carpetas no rompa ninguna referencia.
"""

from __future__ import annotations

import os

RAIZ = os.path.dirname(os.path.abspath(__file__))

CONFIG = os.path.join(RAIZ, "config")
DATA = os.path.join(RAIZ, "data")
DATA_RAW = os.path.join(DATA, "raw")
DATA_PROCESSED = os.path.join(DATA, "processed")
DATA_MODELS = os.path.join(DATA, "models")
DOCS = os.path.join(RAIZ, "docs")
DOCS_FIGURAS = os.path.join(DOCS, "figuras")
DOCS_ENTREGABLES = os.path.join(DOCS, "entregables")
DOCS_RESPALDOS = os.path.join(DOCS, "respaldos")
TOOLS = os.path.join(RAIZ, "tools")
TESTS = os.path.join(RAIZ, "tests")
SRC = os.path.join(RAIZ, "src")

ARCHIVO_CONFIG = os.path.join(CONFIG, "config.yaml")
FUENTE_DOCUMENTO = os.path.join(DOCS_ENTREGABLES, "OmniSafety_AI_Documento_APA.txt")
SALIDA_DOCUMENTO = os.path.join(DOCS_ENTREGABLES, "OmniSafety_AI_Documento_APA.docx")


def crear_directorios() -> None:
    """Crea los directorios de trabajo si no existen."""
    for ruta in (
        CONFIG,
        DATA_RAW,
        DATA_PROCESSED,
        DATA_MODELS,
        DOCS_FIGURAS,
        DOCS_ENTREGABLES,
        DOCS_RESPALDOS,
        TOOLS,
        TESTS,
    ):
        os.makedirs(ruta, exist_ok=True)
