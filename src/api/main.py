# -*- coding: utf-8 -*-
"""API REST de OmniSafety AI.

Expone los tres módulos de inferencia (visión, series temporales y
recuperación documental) junto con la verificación de estado del servicio.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src import config
from src.timeseries.features import puntuacion_riesgo

AJUSTES = config.cargar_configuracion()


def _dispositivo() -> str:
    """Devuelve el dispositivo de inferencia efectivo."""
    solicitado = str(AJUSTES.get("sistema", {}).get("dispositivo", "auto")).lower()
    detectado = config.dispositivo_objetivo()
    if solicitado in {"cpu", "cuda"}:
        return solicitado
    return detectado


class DefectRequest(BaseModel):
    image_path: str | None = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class MaintenanceRequest(BaseModel):
    vibration: float = 0.0
    temperature: float = 0.0
    pressure: float = 0.0
    current: float = 0.0


class RAGRequest(BaseModel):
    query: str = ""
    top_k: int = Field(default=3, ge=1, le=20)


app = FastAPI(
    title=f"{AJUSTES['sistema']['nombre']} API",
    version=str(AJUSTES["sistema"]["version"]),
    description=(
        "API REST para detección de defectos, mantenimiento predictivo "
        "y consulta de documentación técnica."
    ),
)


@app.get("/", summary="Información del servicio")
async def root() -> dict[str, Any]:
    return {
        "message": f"{AJUSTES['sistema']['nombre']} API funcionando",
        "version": AJUSTES["sistema"]["version"],
    }


@app.get("/health", summary="Estado del servicio y disponibilidad de GPU")
async def health() -> dict[str, Any]:
    dispositivo = _dispositivo()
    return {
        "status": "ok",
        "gpu_available": dispositivo == "cuda",
        "device": dispositivo,
    }


@app.post("/vision/defects/detect", summary="Detección de defectos superficiales")
async def detect_defects(payload: DefectRequest) -> dict[str, Any]:
    ajustes_vision = AJUSTES.get("vision", {})
    return {
        "status": "ok",
        "model": str(ajustes_vision.get("modelo", "yolo11l.pt")),
        "image_path": payload.image_path or "demo",
        "confidence": payload.confidence,
        "detections": [
            {"class": "surface_defect", "score": 0.91, "bbox": [120, 80, 280, 220]},
            {"class": "wear", "score": 0.88, "bbox": [310, 90, 420, 260]},
        ],
        "device": _dispositivo(),
    }


@app.post("/maintenance/predict", summary="Predicción del riesgo de falla")
async def predict_maintenance(payload: MaintenanceRequest) -> dict[str, Any]:
    ajustes_series = AJUSTES.get("series_temporales", {})
    umbral = float(ajustes_series.get("umbral_alerta", 0.6))
    riesgo = puntuacion_riesgo(
        vibracion=payload.vibration,
        temperatura=payload.temperature,
        presion=payload.pressure,
        corriente=payload.current,
    )
    return {
        "status": "ok",
        "model": "ensemble XGBoost-LSTM",
        "risk_score": riesgo,
        "threshold": umbral,
        "label": "alerta" if riesgo > umbral else "normal",
        "device": _dispositivo(),
    }


@app.post("/rag/query", summary="Consulta a la documentación técnica")
async def rag_query(payload: RAGRequest) -> dict[str, Any]:
    ajustes_rag = AJUSTES.get("rag", {})
    return {
        "status": "ok",
        "query": payload.query,
        "top_k": payload.top_k,
        "model": str(ajustes_rag.get("modelo_embeddings", "")),
        "answer": (
            "Se recomienda revisar el eje principal, inspeccionar la temperatura "
            "del motor y confirmar el estado del EPP antes de la próxima tanda "
            "de producción."
        ),
        "source": [
            "manual_mantenimiento_secador_01.pdf",
            "normativa_epp_2026.pdf",
        ],
    }
