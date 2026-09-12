# -*- coding: utf-8 -*-
"""Carga y validación de la configuración del sistema."""

from __future__ import annotations

import os
from typing import Any

import yaml

from src import paths

CONFIGURACION_PREDETERMINADA: dict[str, Any] = {
    "sistema": {
        "nombre": "OmniSafety AI",
        "version": "1.0.0",
        "dispositivo": "auto",
    },
    "vision": {
        "modelo": "yolo11l.pt",
        "resolucion": 640,
        "confianza_minima": 0.5,
        "clases": ["grieta", "abolladura", "rayadura", "corrosion", "mancha", "poro"],
    },
    "series_temporales": {
        "ventana": 256,
        "peso_xgboost": 0.6,
        "peso_lstm": 0.4,
        "umbral_alerta": 0.6,
    },
    "rag": {
        "modelo_embeddings": "sentence-transformers/all-MiniLM-L6-v2",
        "dimensiones": 384,
        "tamano_fragmento": 512,
        "solapamiento": 50,
        "top_k": 5,
    },
    "api": {
        "host": "0.0.0.0",
        "puerto": 8000,
    },
    "dashboard": {
        "puerto": 8501,
        "intervalo_actualizacion": 5,
    },
}


def cargar_configuracion(ruta: str | None = None) -> dict[str, Any]:
    """Carga la configuración desde YAML y completa los valores faltantes."""
    ruta = ruta or paths.ARCHIVO_CONFIG
    configuracion: dict[str, Any] = {}
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as manejador:
            contenido = yaml.safe_load(manejador) or {}
            if isinstance(contenido, dict):
                configuracion = contenido

    resultado = dict(CONFIGURACION_PREDETERMINADA)
    for seccion, valores in configuracion.items():
        if isinstance(valores, dict) and isinstance(resultado.get(seccion), dict):
            resultado[seccion] = {**resultado[seccion], **valores}
        else:
            resultado[seccion] = valores
    return resultado


def guardar_configuracion(configuracion: dict[str, Any], ruta: str | None = None) -> str:
    """Escribe la configuración en disco y devuelve la ruta utilizada."""
    ruta = ruta or paths.ARCHIVO_CONFIG
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as manejador:
        yaml.safe_dump(configuracion, manejador, allow_unicode=True, sort_keys=False)
    return ruta


def dispositivo_objetivo() -> str:
    """Devuelve 'cuda' si hay GPU disponible y 'cpu' en caso contrario."""
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"
