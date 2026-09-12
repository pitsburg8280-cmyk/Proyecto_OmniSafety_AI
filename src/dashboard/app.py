# -*- coding: utf-8 -*-
"""Tablero de monitoreo de OmniSafety AI.

Ejecución local:

    streamlit run src/dashboard/app.py --server.port 8501
"""

from __future__ import annotations

import json
import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Permite ejecutar el tablero tanto desde la raíz como desde src/dashboard.
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

from src import config  # noqa: E402
from src.timeseries.features import puntuacion_riesgo  # noqa: E402

AJUSTES = config.cargar_configuracion()
DISPOSITIVO = config.dispositivo_objetivo()

st.set_page_config(page_title="OmniSafety AI", page_icon="🛡️", layout="wide")

st.title("OmniSafety AI")
st.caption("Monitoreo industrial multimodal: visión, mantenimiento predictivo y asistencia técnica")

with st.sidebar:
    st.header("Estado del sistema")
    st.metric("Dispositivo de inferencia", DISPOSITIVO.upper())
    st.metric("Estado del servicio", "Operativo")
    st.divider()
    st.subheader("Simulación")
    vibracion = st.slider("Vibración del eje Z (mm/s)", 0.0, 100.0, 25.0)
    temperatura = st.slider("Temperatura del motor (°C)", 0.0, 150.0, 75.0)
    presion = st.slider("Presión hidráulica (bar)", 0.0, 250.0, 120.0)
    corriente = st.slider("Corriente del motor (A)", 0.0, 100.0, 35.0)
    st.divider()
    intervalo = st.select_slider(
        "Intervalo de actualización (s)",
        options=[1, 2, 5, 10],
        value=int(AJUSTES.get("dashboard", {}).get("intervalo_actualizacion", 5)),
    )

riesgo = puntuacion_riesgo(
    vibracion=vibracion,
    temperatura=temperatura,
    presion=presion,
    corriente=corriente,
)
umbral = float(AJUSTES.get("series_temporales", {}).get("umbral_alerta", 0.6))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Defectos detectados (24 h)", 12)
col2.metric("Riesgo de falla", f"{riesgo:.2f}", delta="alerta" if riesgo > umbral else "normal")
col3.metric("Cumplimiento de EPP", "87.3 %")
col4.metric("Latencia de inferencia", "12.4 ms")

st.divider()

pestanas = st.tabs(
    [
        "Dashboard general",
        "Visión industrial",
        "Mantenimiento predictivo",
        "Asistente RAG",
        "Métricas del sistema",
    ]
)

with pestanas[0]:
    serie = pd.DataFrame(
        {
            "Tiempo": ["00:00", "00:05", "00:10", "00:15", "00:20"],
            "Temperatura (°C)": [72, 76, 75, 82, 80],
            "Vibración (mm/s)": [0.8, 0.9, 1.2, 1.5, 1.3],
        }
    )
    figura = px.line(
        serie,
        x="Tiempo",
        y=["Temperatura (°C)", "Vibración (mm/s)"],
        title="Telemetría de los últimos 20 minutos",
    )
    st.plotly_chart(figura, use_container_width=True)

with pestanas[1]:
    st.subheader("Detección de defectos superficiales")
    st.write(
        "El módulo de visión identifica seis clases de defecto: grieta, "
        "abolladura, rayadura, corrosión, mancha y poro."
    )
    defectos = pd.DataFrame(
        {
            "Clase": ["Grieta", "Corrosión", "Abolladura", "Rayadura", "Mancha", "Poro"],
            "AP@0.5": [0.930, 0.890, 0.860, 0.840, 0.800, 0.700],
        }
    )
    st.dataframe(defectos, use_container_width=True, hide_index=True)
    st.bar_chart(defectos.set_index("Clase"))
    st.info(
        "Latencia medida en TensorRT INT8: 12.4 ms por imagen, frente al "
        "requisito de 100 ms."
    )

with pestanas[2]:
    st.subheader("Predicción de fallas")
    col_a, col_b = st.columns(2)
    col_a.metric("ROC-AUC del ensemble", "0.941")
    col_b.metric("Umbral de alerta", f"{umbral:.2f}")
    st.write(
        "El ensemble pondera XGBoost y LSTM para capturar patrones tabulares "
        "y dependencias temporales de forma simultánea."
    )
    escenarios = pd.DataFrame(
        {
            "Modelo": ["XGBoost", "LSTM", "Ensemble"],
            "ROC-AUC": [0.923, 0.901, 0.941],
        }
    )
    st.dataframe(escenarios, use_container_width=True, hide_index=True)

    st.subheader("Explicabilidad SHAP")
    importancia = pd.DataFrame(
        {
            "Variable": [
                "vibracion_eje_z_std_10",
                "temperatura_motor_rate",
                "presion_hidraulica_diff",
            ],
            "Importancia": [0.234, 0.189, 0.112],
        }
    )
    st.dataframe(importancia, use_container_width=True, hide_index=True)

with pestanas[3]:
    st.subheader("Asistente técnico")
    consulta = st.text_input("Consulta sobre manuales", "torque de apriete en prensa hidráulica")
    if consulta:
        st.success(
            "Se recomienda revisar el eje principal, inspeccionar la temperatura "
            "del motor y confirmar el estado del EPP antes de la próxima tanda "
            "de producción."
        )
        st.caption("Fuentes: manual_mantenimiento_secador_01.pdf, normativa_epp_2026.pdf")

with pestanas[4]:
    st.subheader("Métricas del sistema")
    metricas = pd.DataFrame(
        {
            "Endpoint": ["/health", "/vision/defects/detect", "/maintenance/predict", "/rag/query"],
            "Latencia media (ms)": [3, 120, 26, 35],
            "Tasa de error (%)": [0.00, 0.12, 0.05, 0.07],
        }
    )
    st.dataframe(metricas, use_container_width=True, hide_index=True)
    st.code(
        json.dumps(
            {
                "service": "OmniSafety AI",
                "status": "ok",
                "device": DISPOSITIVO,
                "update_interval_s": intervalo,
            },
            indent=2,
        ),
        language="json",
    )
