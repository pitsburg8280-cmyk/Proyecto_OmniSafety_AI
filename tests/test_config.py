# -*- coding: utf-8 -*-
"""Pruebas de la configuración y las rutas del proyecto."""

from __future__ import annotations

import os

from src import config, paths


def test_rutas_apuntan_a_la_raiz_del_proyecto() -> None:
    assert os.path.isdir(paths.RAIZ)
    assert paths.CONFIG.endswith("config")
    assert paths.DOCS_FIGURAS.endswith(os.path.join("docs", "figuras"))
    assert paths.DOCS_ENTREGABLES.endswith(os.path.join("docs", "entregables"))


def test_fuente_y_salida_del_documento_estan_en_entregables() -> None:
    assert os.path.dirname(paths.FUENTE_DOCUMENTO) == paths.DOCS_ENTREGABLES
    assert os.path.dirname(paths.SALIDA_DOCUMENTO) == paths.DOCS_ENTREGABLES
    assert paths.SALIDA_DOCUMENTO.endswith(".docx")


def test_crear_directorios_no_falla() -> None:
    paths.crear_directorios()
    for ruta in (paths.DATA_RAW, paths.DATA_PROCESSED, paths.DATA_MODELS, paths.DOCS_FIGURAS):
        assert os.path.isdir(ruta)


def test_cargar_configuracion_incluye_las_secciones_esperadas() -> None:
    ajustes = config.cargar_configuracion()
    for seccion in ("sistema", "vision", "series_temporales", "rag", "api", "dashboard"):
        assert seccion in ajustes


def test_cargar_configuracion_lee_el_archivo_yaml() -> None:
    ajustes = config.cargar_configuracion()
    assert ajustes["vision"]["modelo"] == "yolo11l.pt"
    assert ajustes["series_temporales"]["peso_xgboost"] == 0.6
    assert ajustes["rag"]["dimensiones"] == 384
    assert ajustes["api"]["puerto"] == 8000


def test_cargar_configuracion_usa_predeterminados_si_falta_el_archivo() -> None:
    ajustes = config.cargar_configuracion(ruta="ruta/que/no/existe.yaml")
    assert ajustes["sistema"]["nombre"] == "OmniSafety AI"
    assert ajustes["dashboard"]["intervalo_actualizacion"] == 5


def test_dispositivo_objetivo_es_valido() -> None:
    assert config.dispositivo_objetivo() in {"cpu", "cuda"}


def test_guardar_y_recargar_configuracion(tmp_path) -> None:
    destino = str(tmp_path / "config_temporal.yaml")
    config.guardar_configuracion({"sistema": {"version": "9.9.9"}}, ruta=destino)
    recargada = config.cargar_configuracion(ruta=destino)
    assert recargada["sistema"]["version"] == "9.9.9"
    assert recargada["sistema"]["nombre"] == "OmniSafety AI"
