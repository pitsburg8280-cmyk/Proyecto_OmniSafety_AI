# -*- coding: utf-8 -*-
"""Pruebas de la API REST de OmniSafety AI."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app

cliente = TestClient(app)


def test_raiz_responde() -> None:
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "message" in respuesta.json()


def test_health_reporta_estado_y_dispositivo() -> None:
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["status"] == "ok"
    assert datos["device"] in {"cpu", "cuda"}
    assert isinstance(datos["gpu_available"], bool)


def test_deteccion_de_defectos_devuelve_detecciones() -> None:
    respuesta = cliente.post(
        "/vision/defects/detect",
        json={"image_path": "demo", "confidence": 0.75},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["status"] == "ok"
    assert datos["confidence"] == 0.75
    assert len(datos["detections"]) > 0
    for deteccion in datos["detections"]:
        assert 0.0 <= deteccion["score"] <= 1.0
        assert len(deteccion["bbox"]) == 4


def test_prediccion_de_mantenimiento_normaliza_el_riesgo() -> None:
    respuesta = cliente.post(
        "/maintenance/predict",
        json={"vibration": 180, "temperature": 85, "pressure": 120, "current": 45},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert 0.0 <= datos["risk_score"] <= 1.0
    assert datos["label"] in {"normal", "alerta"}


def test_consulta_rag_devuelve_respuesta_y_fuentes() -> None:
    respuesta = cliente.post(
        "/rag/query",
        json={"query": "torque de apriete", "top_k": 2},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["top_k"] == 2
    assert datos["answer"]
    assert len(datos["source"]) > 0


def test_deteccion_rechaza_confianza_invalida() -> None:
    respuesta = cliente.post(
        "/vision/defects/detect",
        json={"image_path": "demo", "confidence": "alta"},
    )
    assert respuesta.status_code == 422
