# -*- coding: utf-8 -*-
"""Características para el modelo de mantenimiento predictivo."""

from __future__ import annotations

from statistics import mean, pstdev
from typing import Iterable


def estadisticas_ventana(valores: Iterable[float]) -> dict[str, float]:
    """Calcula media, desviación estándar y rango de una ventana de señal."""
    serie = [float(v) for v in valores]
    if not serie:
        return {"media": 0.0, "desviacion": 0.0, "rango": 0.0}
    return {
        "media": round(mean(serie), 6),
        "desviacion": round(pstdev(serie) if len(serie) > 1 else 0.0, 6),
        "rango": round(max(serie) - min(serie), 6),
    }


def tasa_de_cambio(valores: Iterable[float]) -> float:
    """Calcula la tasa de cambio media entre muestras consecutivas."""
    serie = [float(v) for v in valores]
    if len(serie) < 2:
        return 0.0
    diferencias = [serie[i + 1] - serie[i] for i in range(len(serie) - 1)]
    return round(mean(diferencias), 6)


def entropia_senal(valores: Iterable[float], bins: int = 10) -> float:
    """Calcula la entropía de Shannon de la distribución de la señal."""
    from collections import Counter
    from math import log2

    serie = [float(v) for v in valores]
    if not serie:
        return 0.0
    minimo, maximo = min(serie), max(serie)
    if maximo == minimo:
        return 0.0
    ancho = (maximo - minimo) / bins
    indices = [min(bins - 1, int((valor - minimo) / ancho)) for valor in serie]
    conteos = Counter(indices)
    total = len(serie)
    return round(-sum((c / total) * log2(c / total) for c in conteos.values()), 6)


def construir_caracteristicas(ventana: dict[str, Iterable[float]]) -> dict[str, float]:
    """Genera el diccionario de características a partir de la telemetría."""
    caracteristicas: dict[str, float] = {}
    for nombre, valores in ventana.items():
        serie = list(valores)
        for clave, valor in estadisticas_ventana(serie).items():
            caracteristicas[f"{nombre}_{clave}"] = valor
        caracteristicas[f"{nombre}_tasa"] = tasa_de_cambio(serie)
        caracteristicas[f"{nombre}_entropia"] = entropia_senal(serie)
    return caracteristicas


def combinar_puntuaciones(puntuacion_xgboost: float, puntuacion_lstm: float,
                          peso_xgboost: float = 0.6) -> float:
    """Combina las puntuaciones de ambos modelos en una sola probabilidad."""
    peso = min(1.0, max(0.0, peso_xgboost))
    valor = peso * float(puntuacion_xgboost) + (1.0 - peso) * float(puntuacion_lstm)
    return round(min(1.0, max(0.0, valor)), 6)


def puntuacion_riesgo(vibracion: float, temperatura: float, presion: float, corriente: float) -> float:
    """Estimación heurística del riesgo usada por la API y el tablero."""
    ponderado = (vibracion * 0.4 + temperatura * 0.3 + presion * 0.2 + corriente * 0.1) / 100.0
    return round(min(1.0, max(0.0, ponderado)), 4)
