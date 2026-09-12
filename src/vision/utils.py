# -*- coding: utf-8 -*-
"""Funciones auxiliares para los módulos de visión por computadora."""

from __future__ import annotations

from typing import Any

import numpy as np


def normalizar_imagen(imagen: np.ndarray) -> np.ndarray:
    """Convierte una imagen al rango [0, 1] y evita la división por cero."""
    arreglo = np.asarray(imagen, dtype="float32")
    maximo = float(arreglo.max()) if arreglo.size else 0.0
    if maximo <= 0:
        return np.zeros_like(arreglo)
    return arreglo / maximo


def filtrar_por_confianza(detecciones: list[dict[str, Any]], umbral: float) -> list[dict[str, Any]]:
    """Descarta detecciones cuya puntuación sea inferior al umbral indicado."""
    return [d for d in detecciones if float(d.get("score", 0.0)) >= umbral]


def aplicar_supresion_no_maxima(detecciones: list[dict[str, Any]], umbral_iou: float = 0.5) -> list[dict[str, Any]]:
    """Aplica supresión no máxima simple sobre cajas en formato [x1, y1, x2, y2]."""
    if not detecciones:
        return []

    ordenadas = sorted(detecciones, key=lambda d: float(d.get("score", 0.0)), reverse=True)
    conservadas: list[dict[str, Any]] = []

    def iou(caja_a: list[float], caja_b: list[float]) -> float:
        x1 = max(caja_a[0], caja_b[0])
        y1 = max(caja_a[1], caja_b[1])
        x2 = min(caja_a[2], caja_b[2])
        y2 = min(caja_a[3], caja_b[3])
        interseccion = max(0.0, x2 - x1) * max(0.0, y2 - y1)
        area_a = max(0.0, caja_a[2] - caja_a[0]) * max(0.0, caja_a[3] - caja_a[1])
        area_b = max(0.0, caja_b[2] - caja_b[0]) * max(0.0, caja_b[3] - caja_b[1])
        union = area_a + area_b - interseccion
        return interseccion / union if union > 0 else 0.0

    for candidata in ordenadas:
        caja = candidata.get("bbox", [0, 0, 0, 0])
        if all(iou(list(caja), list(guardada.get("bbox", [0, 0, 0, 0]))) <= umbral_iou for guardada in conservadas):
            conservadas.append(candidata)
    return conservadas


def resumen_detecciones(detecciones: list[dict[str, Any]]) -> dict[str, Any]:
    """Resume las detecciones por clase para alimentar al tablero."""
    conteo: dict[str, int] = {}
    for deteccion in detecciones:
        clase = str(deteccion.get("class", "desconocida"))
        conteo[clase] = conteo.get(clase, 0) + 1
    puntuaciones = [float(d.get("score", 0.0)) for d in detecciones]
    return {
        "total": len(detecciones),
        "por_clase": conteo,
        "confianza_promedio": round(float(np.mean(puntuaciones)), 4) if puntuaciones else 0.0,
        "confianza_maxima": round(max(puntuaciones), 4) if puntuaciones else 0.0,
    }
