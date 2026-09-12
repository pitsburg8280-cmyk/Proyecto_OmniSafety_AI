# -*- coding: utf-8 -*-
"""Pruebas de las utilidades de visión por computadora."""

from __future__ import annotations

import numpy as np
import pytest

from src.vision import utils


def test_normalizar_imagen_escala_al_rango_unitario() -> None:
    imagen = np.array([[0, 5], [10, 20]], dtype="float32")
    normalizada = utils.normalizar_imagen(imagen)
    assert normalizada.max() == pytest.approx(1.0)
    assert normalizada.min() == pytest.approx(0.0)


def test_normalizar_imagen_vacia_no_falla() -> None:
    resultado = utils.normalizar_imagen(np.zeros((2, 2), dtype="float32"))
    assert resultado.shape == (2, 2)
    assert float(resultado.sum()) == 0.0


def test_filtrar_por_confianza_descarta_detecciones_debiles() -> None:
    detecciones = [
        {"class": "grieta", "score": 0.9, "bbox": [0, 0, 10, 10]},
        {"class": "poro", "score": 0.4, "bbox": [5, 5, 15, 15]},
    ]
    filtradas = utils.filtrar_por_confianza(detecciones, umbral=0.5)
    assert len(filtradas) == 1
    assert filtradas[0]["class"] == "grieta"


def test_supresion_no_maxima_elimina_cajas_solapadas() -> None:
    detecciones = [
        {"class": "grieta", "score": 0.95, "bbox": [0, 0, 100, 100]},
        {"class": "grieta", "score": 0.85, "bbox": [5, 5, 100, 100]},
        {"class": "poro", "score": 0.60, "bbox": [200, 200, 250, 250]},
    ]
    conservadas = utils.aplicar_supresion_no_maxima(detecciones, umbral_iou=0.5)
    assert len(conservadas) == 2
    assert conservadas[0]["score"] == 0.95


def test_supresion_no_maxima_sin_detecciones() -> None:
    assert utils.aplicar_supresion_no_maxima([]) == []


def test_resumen_detecciones_agrupa_por_clase() -> None:
    detecciones = [
        {"class": "grieta", "score": 0.9},
        {"class": "grieta", "score": 0.7},
        {"class": "poro", "score": 0.5},
    ]
    resumen = utils.resumen_detecciones(detecciones)
    assert resumen["total"] == 3
    assert resumen["por_clase"] == {"grieta": 2, "poro": 1}
    assert resumen["confianza_maxima"] == pytest.approx(0.9)


def test_resumen_detecciones_sin_datos() -> None:
    resumen = utils.resumen_detecciones([])
    assert resumen["total"] == 0
    assert resumen["confianza_promedio"] == 0.0
