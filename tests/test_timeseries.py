# -*- coding: utf-8 -*-
"""Pruebas de las características de mantenimiento predictivo."""

from __future__ import annotations

import pytest

from src.timeseries import features


def test_estadisticas_ventana_calcula_valores_basicos() -> None:
    resultado = features.estadisticas_ventana([1.0, 2.0, 3.0, 4.0])
    assert resultado["media"] == pytest.approx(2.5)
    assert resultado["rango"] == pytest.approx(3.0)
    assert resultado["desviacion"] > 0


def test_estadisticas_ventana_vacia() -> None:
    resultado = features.estadisticas_ventana([])
    assert resultado == {"media": 0.0, "desviacion": 0.0, "rango": 0.0}


def test_tasa_de_cambio_constante() -> None:
    assert features.tasa_de_cambio([1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_entropia_senal_constante_es_cero() -> None:
    assert features.entropia_senal([5.0, 5.0, 5.0]) == 0.0


def test_entropia_senal_distingue_variabilidad() -> None:
    uniforme = features.entropia_senal([0.0, 0.0, 0.0, 1.0])
    variable = features.entropia_senal([0.0, 0.3, 0.6, 1.0])
    assert variable > uniforme


def test_construir_caracteristicas_genera_claves_por_variable() -> None:
    ventana = {"vibracion_eje_z": [1.0, 2.0, 3.0, 4.0]}
    caracteristicas = features.construir_caracteristicas(ventana)
    assert "vibracion_eje_z_media" in caracteristicas
    assert "vibracion_eje_z_tasa" in caracteristicas
    assert "vibracion_eje_z_entropia" in caracteristicas


def test_combinar_puntuaciones_respeta_el_peso() -> None:
    assert features.combinar_puntuaciones(1.0, 0.0, peso_xgboost=0.6) == pytest.approx(0.6)
    assert features.combinar_puntuaciones(0.0, 1.0, peso_xgboost=0.6) == pytest.approx(0.4)


def test_combinar_puntuaciones_se_limita_al_rango() -> None:
    assert 0.0 <= features.combinar_puntuaciones(2.0, 3.0) <= 1.0
    assert 0.0 <= features.combinar_puntuaciones(-1.0, -5.0) <= 1.0


def test_puntuacion_riesgo_crece_con_la_vibracion() -> None:
    bajo = features.puntuacion_riesgo(vibracion=10, temperatura=50, presion=100, corriente=20)
    alto = features.puntuacion_riesgo(vibracion=90, temperatura=95, presion=180, corriente=60)
    assert alto > bajo
    assert 0.0 <= bajo <= 1.0
    assert 0.0 <= alto <= 1.0
