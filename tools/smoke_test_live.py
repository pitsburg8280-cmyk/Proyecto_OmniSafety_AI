# -*- coding: utf-8 -*-
"""Prueba de humo funcional contra la API en vivo de OmniSafety AI.

Uso:

    python tools/smoke_test_live.py

Verifica cada endpoint real (visión, mantenimiento y RAG) con datos válidos,
comprueba los casos límite de validación y resume el resultado del flujo.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000"

VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
RESET = "\033[0m"

resultados: list[tuple[str, bool, str]] = []


def peticion(metodo: str, ruta: str, cuerpo: dict | None = None) -> tuple[int, object]:
    """Realiza una petición HTTP y devuelve el código y el cuerpo JSON."""
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    solicitud = urllib.request.Request(BASE + ruta, data=datos, method=metodo)
    if datos is not None:
        solicitud.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(solicitud, timeout=15) as respuesta:
            return respuesta.status, json.loads(respuesta.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def comprobar(nombre: str, condicion: bool, detalle: str) -> None:
    """Registra y muestra el resultado de una comprobación."""
    resultados.append((nombre, condicion, detalle))
    marca = f"{VERDE}OK{RESET}" if condicion else f"{ROJO}FALLO{RESET}"
    print(f"  [{marca}] {nombre}: {detalle}")


def main() -> int:
    print("=" * 70)
    print("COMPROBACIÓN FUNCIONAL EN VIVO - OmniSafety AI")
    print("=" * 70)

    # 1. Información del servicio
    print("\n[1] Información del servicio")
    codigo, datos = peticion("GET", "/")
    comprobar("GET /", codigo == 200, f"HTTP {codigo}")
    comprobar(
        "Respuesta de raíz",
        isinstance(datos, dict) and "message" in datos,
        f"message='{datos.get('message') if isinstance(datos, dict) else '?'}'",
    )

    # 2. Estado y dispositivo
    print("\n[2] Estado del servicio")
    codigo, datos = peticion("GET", "/health")
    comprobar("GET /health", codigo == 200, f"HTTP {codigo}")
    if isinstance(datos, dict):
        comprobar("Campo status", datos.get("status") == "ok", f"status={datos.get('status')}")
        comprobar(
            "Dispositivo válido",
            datos.get("device") in {"cpu", "cuda"},
            f"device={datos.get('device')} | gpu_available={datos.get('gpu_available')}",
        )

    # 3. Visión: detección de defectos
    print("\n[3] Visión industrial - detección de defectos")
    codigo, datos = peticion(
        "POST",
        "/vision/defects/detect",
        {"image_path": "data/raw/muestra_01.jpg", "confidence": 0.75},
    )
    comprobar("POST /vision/defects/detect", codigo == 200, f"HTTP {codigo}")
    if isinstance(datos, dict):
        comprobar("Campo status", datos.get("status") == "ok", f"status={datos.get('status')}")
        comprobar(
            "Eco de confianza",
            datos.get("confidence") == 0.75,
            f"confidence={datos.get('confidence')}",
        )
        detecciones = datos.get("detections", [])
        comprobar("Detecciones no vacías", len(detecciones) > 0, f"{len(detecciones)} detecciones")
        for deteccion in detecciones:
            print(f"       -> {deteccion['class']}: score={deteccion['score']} bbox={deteccion['bbox']}")

    # 4. Mantenimiento predictivo: escenario crítico
    print("\n[4] Mantenimiento predictivo - escenario crítico")
    codigo, datos = peticion(
        "POST",
        "/maintenance/predict",
        {"vibration": 85.0, "temperature": 95.0, "pressure": 180.0, "current": 60.0},
    )
    comprobar("POST /maintenance/predict", codigo == 200, f"HTTP {codigo}")
    if isinstance(datos, dict):
        riesgo = datos.get("risk_score", -1)
        comprobar("Riesgo en rango [0,1]", 0.0 <= riesgo <= 1.0, f"risk_score={riesgo}")
        comprobar(
            "Etiqueta coherente",
            datos.get("label") == ("alerta" if riesgo > datos.get("threshold", 1) else "normal"),
            f"label={datos.get('label')} threshold={datos.get('threshold')}",
        )

    # 5. Mantenimiento predictivo: escenario nominal
    print("\n[5] Mantenimiento predictivo - escenario nominal")
    codigo, datos = peticion(
        "POST",
        "/maintenance/predict",
        {"vibration": 5.0, "temperature": 30.0, "pressure": 20.0, "current": 10.0},
    )
    comprobar("POST /maintenance/predict (bajo)", codigo == 200, f"HTTP {codigo}")
    if isinstance(datos, dict):
        comprobar(
            "Etiqueta normal en escenario bajo",
            datos.get("label") == "normal",
            f"risk_score={datos.get('risk_score')} label={datos.get('label')}",
        )

    # 6. RAG: consulta documental
    print("\n[6] Asistente RAG - consulta documental")
    codigo, datos = peticion(
        "POST",
        "/rag/query",
        {"query": "torque de apriete en prensa hidráulica", "top_k": 2},
    )
    comprobar("POST /rag/query", codigo == 200, f"HTTP {codigo}")
    if isinstance(datos, dict):
        comprobar("Eco de top_k", datos.get("top_k") == 2, f"top_k={datos.get('top_k')}")
        comprobar("Respuesta no vacía", bool(datos.get("answer")), "answer presente")
        comprobar("Fuentes presentes", len(datos.get("source", [])) > 0, f"{len(datos.get('source', []))} fuentes")

    # 7. Validación de entrada (casos de error esperados)
    print("\n[7] Validación de entrada")
    codigo, _ = peticion(
        "POST",
        "/vision/defects/detect",
        {"image_path": "demo", "confidence": "alta"},
    )
    comprobar("Confianza inválida rechazada (422)", codigo == 422, f"HTTP {codigo}")

    codigo, _ = peticion("POST", "/rag/query", {"query": "prueba", "top_k": 999})
    comprobar("top_k fuera de rango rechazado (422)", codigo == 422, f"HTTP {codigo}")

    # Resumen
    print("\n" + "=" * 70)
    total = len(resultados)
    exitosas = sum(1 for _, ok, _ in resultados if ok)
    fallidas = total - exitosas
    color = VERDE if fallidas == 0 else ROJO
    print(f"RESUMEN: {color}{exitosas}/{total} comprobaciones superadas{RESET}")
    if fallidas:
        print(f"{AMARILLO}Comprobaciones fallidas:{RESET}")
        for nombre, ok, detalle in resultados:
            if not ok:
                print(f"  - {nombre}: {detalle}")
    print("=" * 70)
    return 0 if fallidas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
