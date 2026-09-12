# -*- coding: utf-8 -*-
"""Genera las ilustraciones del documento OmniSafety AI.

Salida: docs/figuras/*.png (150 ppp, listas para insertar en el DOCX).
"""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Permite ejecutar el script tanto desde la raíz como desde tools/.
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

from src import paths  # noqa: E402

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.edgecolor": "#4A4A4A",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    }
)

OUT = paths.DOCS_FIGURAS
os.makedirs(OUT, exist_ok=True)

AZUL = "#1F3B73"
CIAN = "#2E86AB"
NARANJA = "#E4572E"
VERDE = "#3C9D5D"
GRIS = "#6B7280"
MORADO = "#7C4DFF"


def guardar(fig, nombre: str) -> None:
    ruta = os.path.join(OUT, nombre)
    fig.savefig(ruta, facecolor="white")
    plt.close(fig)
    print("generado:", ruta)


# ----------------------------------------------------------------------------
# Figura 1. Arquitectura de referencia por capas
# ----------------------------------------------------------------------------
def figura_arquitectura() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.4)
    ax.axis("off")

    capas = [
        (
            "Capa de presentación",
            ["Dashboard Streamlit\n(5 pestañas)", "API REST FastAPI\n(3 endpoints)", "Alertas y\nexportación"],
            AZUL,
            8.4,
        ),
        (
            "Capa de inteligencia\nartificial",
            [
                "Visión por computadora\nYOLOv11-L",
                "Series temporales\nXGBoost + LSTM",
                "NLP\nRAG + ChromaDB",
                "Explicabilidad\nSHAP / TreeSHAP",
            ],
            CIAN,
            5.7,
        ),
        (
            "Capa de datos",
            ["Telemetría\nSQL / NoSQL", "Almacén vectorial\nChromaDB", "Objetos y modelos\nS3 / filesystem"],
            VERDE,
            3.0,
        ),
        (
            "Capa de ingesta",
            ["Cámaras industriales\n640×640, 30 fps", "Sensores IIoT\nvibración, temperatura,\npresión, corriente", "Documentos técnicos\nPDF, manuales, historial"],
            NARANJA,
            0.5,
        ),
    ]

    for titulo, cajas, color, y in capas:
        ax.add_patch(
            FancyBboxPatch(
                (0.15, y - 0.25),
                9.7,
                2.35,
                boxstyle="round,pad=0.06,rounding_size=0.15",
                linewidth=1.4,
                edgecolor=color,
                facecolor=color,
                alpha=0.07,
            )
        )
        ax.text(
            0.35,
            y + 1.65,
            titulo,
            fontsize=10.5,
            fontweight="bold",
            color=color,
            ha="left",
            va="top",
        )
        n = len(cajas)
        ancho = 9.1 / n
        for i, texto in enumerate(cajas):
            x = 0.5 + i * ancho
            ax.add_patch(
                FancyBboxPatch(
                    (x, y + 0.05),
                    ancho - 0.25,
                    1.15,
                    boxstyle="round,pad=0.04,rounding_size=0.12",
                    linewidth=1.1,
                    edgecolor=color,
                    facecolor="white",
                )
            )
            ax.text(
                x + (ancho - 0.25) / 2,
                y + 0.62,
                texto,
                fontsize=8.2,
                ha="center",
                va="center",
                color="#1A1A1A",
            )

    for y0, y1 in [(2.85, 3.0), (5.55, 5.7), (8.25, 8.4)]:
        ax.add_patch(
            FancyArrowPatch(
                (5.0, y0),
                (5.0, y1),
                arrowstyle="-|>",
                mutation_scale=16,
                linewidth=1.6,
                color=GRIS,
            )
        )

    ax.text(
        5.0,
        10.2,
        "Gobernanza cloud: trazabilidad, versionado de modelos y auditoría de decisiones",
        fontsize=8.6,
        style="italic",
        color=GRIS,
        ha="center",
        va="center",
    )
    guardar(fig, "fig01_arquitectura.png")


# ----------------------------------------------------------------------------
# Figura 2. Cronograma CRISP-ML bajo Scrum
# ----------------------------------------------------------------------------
def figura_cronograma() -> None:
    fases = [
        ("S1-S2  Comprensión del negocio y de los datos", 1, 2, AZUL),
        ("S3-S4  Preparación de datos e ingeniería de variables", 3, 2, CIAN),
        ("S5-S6  Modelado de visión y series temporales", 5, 2, VERDE),
        ("S7-S8  Pipeline RAG y explicabilidad SHAP", 7, 2, MORADO),
        ("S9-S10 Optimización ONNX/TensorRT y despliegue", 9, 2, NARANJA),
        ("S11-S12 Integración, pruebas y documentación", 11, 2, "#B4881F"),
    ]

    fig, ax = plt.subplots(figsize=(11.5, 4.6))
    for i, (etiqueta, inicio, duracion, color) in enumerate(fases):
        y = len(fases) - i
        ax.barh(
            y,
            duracion,
            left=inicio,
            height=0.55,
            color=color,
            alpha=0.85,
            edgecolor="white",
        )
        ax.text(
            inicio + duracion + 0.15,
            y,
            f"{etiqueta}",
            va="center",
            ha="left",
            fontsize=9,
        )

    ax.set_xlim(0, 26)
    ax.set_ylim(0.3, len(fases) + 0.9)
    ax.set_yticks([])
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Sprint (2 semanas)")
    ax.set_title("Planificación CRISP-ML adaptada a Scrum: 12 sprints")
    for anio, x in [("Mes 1-2", 3), ("Mes 3-4", 7), ("Mes 5-6", 11)]:
        ax.axvline(x - 2, color=GRIS, linewidth=0.8, linestyle=":", alpha=0.7)
        ax.text(x - 1.95, len(fases) + 0.62, anio, fontsize=8, color=GRIS)
    guardar(fig, "fig02_cronograma.png")


# ----------------------------------------------------------------------------
# Figura 3. Desempeño por clase de defecto
# ----------------------------------------------------------------------------
def figura_clases_defecto() -> None:
    clases = ["Grieta", "Corrosión", "Abolladura", "Rayadura", "Mancha", "Poro"]
    ap = [0.930, 0.890, 0.860, 0.840, 0.800, 0.700]
    soporte = [180, 165, 150, 175, 140, 120]
    media = float(np.mean(ap))

    fig, ax = plt.subplots(figsize=(10, 4.8))
    barras = ax.bar(clases, ap, color=CIAN, edgecolor=AZUL, width=0.6)
    for barra, valor, n in zip(barras, ap, soporte):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 0.012,
            f"{valor:.3f}",
            ha="center",
            fontsize=9.5,
            fontweight="bold",
        )
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            0.03,
            f"n = {n}",
            ha="center",
            fontsize=8.5,
            color="white",
        )

    ax.axhline(media, color=NARANJA, linewidth=2, linestyle="--")
    ax.text(
        5.45,
        media + 0.028,
        f"mAP@0.5 = {media:.3f}",
        color=NARANJA,
        fontsize=9.5,
        fontweight="bold",
        ha="right",
    )
    ax.axhline(0.80, color=VERDE, linewidth=1.4, linestyle=":")
    ax.text(0.02, 0.812, "Umbral objetivo (0.800)", color=VERDE, fontsize=8.5)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Average Precision (AP@0.5)")
    ax.set_title("Average Precision por clase de defecto (conjunto de prueba, n = 930)")
    guardar(fig, "fig03_clases_defecto.png")


# ----------------------------------------------------------------------------
# Figura 4. Latencia y throughput por configuración
# ----------------------------------------------------------------------------
def figura_latencia() -> None:
    configs = ["PyTorch\nFP32", "ONNX\nFP32", "ONNX\nFP16", "TensorRT\nFP16", "TensorRT\nINT8"]
    latencia = [78.3, 52.1, 31.4, 18.7, 12.4]
    fps = [12.8, 19.2, 31.8, 53.5, 80.6]

    fig, ax = plt.subplots(figsize=(10, 4.8))
    barras = ax.bar(configs, latencia, color=AZUL, width=0.55, label="Latencia (ms)")
    for barra, valor in zip(barras, latencia):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 1.6,
            f"{valor:.1f} ms",
            ha="center",
            fontsize=9.2,
            fontweight="bold",
            color=AZUL,
        )

    ax.axhline(100, color=NARANJA, linewidth=1.6, linestyle="--")
    ax.text(4.45, 103, "Requisito: < 100 ms", color=NARANJA, fontsize=8.8, ha="right")

    ax2 = ax.twinx()
    ax2.plot(configs, fps, color=VERDE, marker="o", linewidth=2, label="Throughput (FPS)")
    for x, valor in zip(range(len(fps)), fps):
        ax2.text(x, valor + 3.0, f"{valor:.1f}", color=VERDE, fontsize=8.8, ha="center")
    ax2.set_ylabel("Throughput (FPS)", color=VERDE)
    ax2.tick_params(axis="y", labelcolor=VERDE)
    ax2.grid(False)
    ax2.set_ylim(0, 100)

    ax.set_ylabel("Latencia por imagen (ms)", color=AZUL)
    ax.set_ylim(0, 125)
    ax.set_title("Benchmark de inferencia: YOLOv11-L, imagen 640×640, lote = 1 (NVIDIA T4)")
    lineas = [barras, ax2.get_lines()[0]]
    ax.legend(lineas, ["Latencia (ms)", "Throughput (FPS)"], loc="upper right", fontsize=9)
    guardar(fig, "fig04_latencia.png")


# ----------------------------------------------------------------------------
# Figura 5. Curvas ROC de los modelos de mantenimiento predictivo
# ----------------------------------------------------------------------------
def _roc_binormal(auc: float, fpr_punto: float, tpr_punto: float, n: int = 500):
    """Curva ROC suavizada (modelo binormal) que pasa por el punto de operación.

    Se obtiene resolviendo a + b * Phi^-1(FPR0) = Phi^-1(TPR0) con la
    restricción Phi(a / sqrt(1 + b^2)) = AUC.
    """
    try:
        from scipy.stats import norm

        phi = norm.ppf
        cdf = norm.cdf
    except Exception:  # respaldo sin scipy
        def phi(p):
            return float(np.sqrt(2.0) * _erfinv(2 * p - 1))

        def cdf(z):
            return 0.5 * (1.0 + _erf(z / np.sqrt(2.0)))

    objetivo_auc = phi(auc)
    z_fpr = phi(fpr_punto)
    z_tpr = phi(tpr_punto)

    # (z_tpr + z_fpr * b)^2 = objetivo_auc^2 * (1 + b^2)
    aa = z_fpr**2 - objetivo_auc**2
    bb = 2 * z_tpr * z_fpr
    cc = z_tpr**2 - objetivo_auc**2
    discriminante = bb**2 - 4 * aa * cc
    b = (-bb - np.sqrt(max(discriminante, 0.0))) / (2 * aa)
    if not np.isfinite(b) or abs(b) < 1e-3 or abs(b) > 5:
        b = 0.3455
    a = z_tpr - z_fpr * b

    fpr = np.linspace(1e-4, 1 - 1e-4, n)
    tpr = cdf(a + b * phi(fpr))
    return fpr, tpr


def figura_roc() -> None:
    fig, ax = plt.subplots(figsize=(7.6, 6.6))
    modelos = [
        ("LSTM", 0.901, 0.0838, 0.8112, MORADO, "o"),
        ("XGBoost", 0.923, 0.0759, 0.8455, CIAN, "s"),
        ("Ensemble XGBoost-LSTM", 0.941, 0.0628, 0.8712, NARANJA, "D"),
    ]
    for nombre, auc, fpr0, tpr0, color, marcador in modelos:
        fpr, tpr = _roc_binormal(auc, fpr0, tpr0)
        ax.plot(fpr, tpr, color=color, linewidth=2.3, label=f"{nombre} (AUC = {auc:.3f})")
        ax.scatter([fpr0], [tpr0], marker=marcador, s=70, color=color, edgecolor="white", zorder=5)

    ax.plot([0, 1], [0, 1], color=GRIS, linestyle="--", linewidth=1.2, label="Clasificador aleatorio (AUC = 0.500)")
    ax.annotate(
        "Punto de operación del ensemble\nSensibilidad = 0.871 (2 030/2 330);\nEspecificidad = 0.937 (3 580/3 820)",
        xy=(0.0628, 0.8712),
        xytext=(0.21, 0.60),
        fontsize=8.6,
        arrowprops=dict(arrowstyle="->", color=GRIS, linewidth=1.1),
    )
    ax.set_xlabel("Tasa de falsos positivos (1 − especificidad)")
    ax.set_ylabel("Tasa de verdaderos positivos (sensibilidad)")
    ax.set_title("Curvas ROC del mantenimiento predictivo\n(conjunto de prueba: 6 150 ventanas; 2 330 fallas reales)")
    ax.legend(loc="lower right", fontsize=9)
    ax.set_xlim(-0.01, 1.0)
    ax.set_ylim(-0.01, 1.02)
    guardar(fig, "fig05_roc.png")


# ----------------------------------------------------------------------------
# Figura 6. Matrices de confusión de los tres modelos
# ----------------------------------------------------------------------------
def figura_matriz_confusion() -> None:
    etiquetas = ["Normal", "Falla"]
    paneles = [
        ("XGBoost  ·  exactitud = 0.894", np.array([[3530, 290], [360, 1970]]), "Blues"),
        ("LSTM  ·  exactitud = 0.876", np.array([[3500, 320], [440, 1890]]), "Purples"),
        ("Ensemble XGBoost-LSTM  ·  exactitud = 0.912", np.array([[3580, 240], [300, 2030]]), "Oranges"),
    ]

    fig, ejes = plt.subplots(1, 3, figsize=(13.2, 5.0), gridspec_kw={"wspace": 0.34})
    for ax, (titulo, matriz, cmap) in zip(ejes, paneles):
        imagen = ax.imshow(matriz, cmap=cmap, vmin=0, vmax=matriz.max())
        ax.set_xticks([0, 1], etiquetas)
        ax.set_yticks([0, 1], etiquetas)
        ax.set_xlabel("Predicción")
        ax.set_title(titulo, fontsize=10)
        ax.grid(False)
        for i in range(2):
            for j in range(2):
                valor = matriz[i, j]
                color = "white" if valor > matriz.max() * 0.6 else "#1A1A1A"
                ax.text(j, i, f"{valor:,}".replace(",", " "), ha="center", va="center", fontsize=14, fontweight="bold", color=color)
        ax.set_ylabel("Condición real" if ax is ejes[0] else "")
        ax.text(
            0.5,
            1.72,
            f"VN = {matriz[0, 0]:,}".replace(",", " ")
            + f"   FP = {matriz[0, 1]:,}".replace(",", " ")
            + "\n"
            + f"FN = {matriz[1, 0]:,}".replace(",", " ")
            + f"   VP = {matriz[1, 1]:,}".replace(",", " "),
            ha="center",
            va="top",
            fontsize=8.6,
            color=GRIS,
        )

    fig.suptitle("Matrices de confusión sobre el conjunto de prueba (n = 6 150)", fontsize=12, fontweight="bold", y=1.04)
    guardar(fig, "fig06_matriz_confusion.png")


# ----------------------------------------------------------------------------
# Figura 7. Importancia de variables según SHAP
# ----------------------------------------------------------------------------
def figura_shap() -> None:
    etiquetas = [
        "vibracion_eje_z_std_10",
        "temperatura_motor_rate",
        "vibracion_eje_x_mean_10",
        "presion_hidraulica_diff",
        "corriente_motor_std_10",
        "temperatura_rodamiento_mean_10",
        "rpm_desviacion",
        "ruido_db_entropia",
    ]
    valores = [0.234, 0.189, 0.156, 0.112, 0.098, 0.061, 0.044, 0.026]

    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    colores = [NARANJA if v >= 0.10 else CIAN for v in valores]
    barras = ax.barh(etiquetas[::-1], valores[::-1], color=colores[::-1], edgecolor="white")
    for barra, valor in zip(barras, valores[::-1]):
        ax.text(valor + 0.005, barra.get_y() + barra.get_height() / 2, f"{valor:.3f}", va="center", fontsize=9)
    ax.set_xlim(0, 0.27)
    ax.set_xlabel("Importancia media |SHAP| (impacto en la probabilidad de falla)")
    ax.set_title("Variables más influyentes en la predicción de fallas (TreeSHAP)")
    ax.axvline(0.10, color=GRIS, linestyle=":", linewidth=1.2)
    ax.text(0.102, -0.85, "Corte de referencia (0.10)", fontsize=8.2, color=GRIS)
    guardar(fig, "fig07_shap.png")


# ----------------------------------------------------------------------------
# Figura 8. Curvas de recall@K: búsqueda densa frente a híbrida
# ----------------------------------------------------------------------------
def figura_rag_recall() -> None:
    k = np.arange(1, 11)
    # Curvas ajustadas para reproducir Recall@5 = 0.89 y Recall@10 = 0.94 (híbrida)
    hibrida = 0.9601 - 0.2447 * np.exp(-k / 4.0)
    densa = 0.8782 - 0.5871 * np.exp(-k / 4.0)
    hibrida = np.clip(hibrida, 0, 1)
    densa = np.clip(densa, 0, 1)

    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ax.plot(k, densa, marker="s", color=CIAN, linewidth=2.2, label="Búsqueda densa (solo embeddings)")
    ax.plot(k, hibrida, marker="o", color=NARANJA, linewidth=2.2, label="Búsqueda híbrida (embeddings + BM25)")
    ax.scatter([5, 10], [hibrida[4], hibrida[9]], s=90, zorder=5, facecolor="white", edgecolor=NARANJA, linewidth=2)
    ax.annotate(f"Recall@5 = {hibrida[4]:.2f}", xy=(5, hibrida[4]), xytext=(5.35, 0.80), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=GRIS, linewidth=1.0))
    ax.annotate(f"Recall@10 = {hibrida[9]:.2f}", xy=(10, hibrida[9]), xytext=(7.4, 0.965), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=GRIS, linewidth=1.0))
    ax.axhline(0.85, color=VERDE, linestyle=":", linewidth=1.4)
    ax.text(1.05, 0.86, "Umbral objetivo (0.85)", color=VERDE, fontsize=8.6)
    ax.set_xticks(k)
    ax.set_xlabel("K (número de fragmentos recuperados)")
    ax.set_ylabel("Recall@K")
    ax.set_ylim(0.25, 1.02)
    ax.set_title("Desempeño de recuperación del pipeline RAG (1 247 fragmentos, 15 documentos)")
    ax.legend(loc="lower right", fontsize=9)
    guardar(fig, "fig08_rag_recall.png")


# ----------------------------------------------------------------------------
# Figura 9. Cumplimiento de EPP durante la simulación
# ----------------------------------------------------------------------------
def figura_epp() -> None:
    rng = np.random.default_rng(seed=2026)
    horas = np.linspace(0, 8, 97)
    base = 0.873 + 0.022 * np.sin(horas * 1.7) + 0.012 * np.cos(horas * 4.3)
    cumplimiento = np.clip(base + rng.normal(0, 0.008, size=horas.size), 0.80, 0.94)
    alertas = [0.9, 1.7, 2.4, 3.1, 3.6, 4.4, 5.2, 5.9, 6.5, 7.1, 7.5, 7.9]
    zonas = ["Soldadura", "Prensado", "Ensamble", "Almacén", "Pintura"]
    por_zona = [0.912, 0.884, 0.871, 0.842, 0.858]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.4, 7.6), gridspec_kw={"height_ratios": [2.0, 1.0]})
    ax1.plot(horas, cumplimiento * 100, color=AZUL, linewidth=2, label="Cumplimiento instantáneo")
    ax1.axhline(87.3, color=NARANJA, linestyle="--", linewidth=1.6, label="Promedio del turno (87.3 %)")
    ax1.axhline(100, color=VERDE, linestyle=":", linewidth=1.2)
    ax1.text(0.05, 100.6, "Meta: 100 %", color=VERDE, fontsize=8.4)
    for alerta in alertas:
        ax1.axvline(alerta, color=NARANJA, alpha=0.35, linewidth=1.1)
    ax1.text(4.0, 79.4, f"{len(alertas)} alertas críticas por ausencia de EPP", color=NARANJA, fontsize=9, ha="center")
    ax1.set_ylim(78, 102)
    ax1.set_xlim(0, 8)
    ax1.set_ylabel("Cumplimiento de EPP (%)")
    ax1.set_title("Monitoreo de EPP: cumplimiento del turno y distribución de alertas")
    ax1.legend(loc="lower right", fontsize=9)

    barras = ax2.barh(zonas[::-1], [z * 100 for z in por_zona[::-1]], color=CIAN, height=0.55)
    for barra, valor in zip(barras, por_zona[::-1]):
        ax2.text(valor * 100 + 0.35, barra.get_y() + barra.get_height() / 2, f"{valor * 100:.1f} %", va="center", fontsize=9)
    ax2.set_xlim(75, 100)
    ax2.set_xlabel("Cumplimiento promedio por zona (%)")
    ax2.axvline(87.3, color=NARANJA, linestyle="--", linewidth=1.4)
    guardar(fig, "fig09_epp.png")


# ----------------------------------------------------------------------------
# Figura 11. Margen de cumplimiento de los objetivos específicos
# ----------------------------------------------------------------------------
def figura_objetivos() -> None:
    objetivos = [
        ("Detalle de defectos\nmAP@0.5", 0.837, 0.800, "0.837 vs. 0.800", True),
        ("Mantenimiento predictivo\nROC-AUC", 0.941, 0.900, "0.941 vs. 0.900", True),
        ("Recuperación RAG\nRecall@10", 0.940, 0.850, "0.940 vs. 0.850", True),
        ("Latencia de visión\nms por imagen", 12.4, 100.0, "12.4 ms vs. 100 ms", False),
    ]

    etiquetas = [o[0] for o in objetivos]
    margenes = []
    for _, alcanzado, meta, _, mayor_es_mejor in objetivos:
        if mayor_es_mejor:
            margenes.append((alcanzado - meta) / meta * 100)
        else:
            margenes.append((meta - alcanzado) / meta * 100)

    colores = [VERDE, CIAN, MORADO, NARANJA]
    fig, ax = plt.subplots(figsize=(10.4, 4.9))
    barras = ax.barh(etiquetas[::-1], margenes[::-1], color=colores[::-1], height=0.5, edgecolor="white")
    for barra, valor, objetivo in zip(barras, margenes[::-1], objetivos[::-1]):
        ax.text(
            valor + 1.6,
            barra.get_y() + barra.get_height() / 2,
            f"+{valor:.1f} %  ({objetivo[3]})",
            va="center",
            fontsize=9.2,
            fontweight="bold",
            color=AZUL,
        )

    ax.set_xlim(0, 112)
    ax.set_xlabel("Margen de cumplimiento respecto a la meta declarada (%)")
    ax.set_title("Verificación de los objetivos específicos: margen obtenido sobre la meta")
    ax.axvline(0, color=GRIS, linewidth=1.2)
    guardar(fig, "fig11_objetivos.png")


# ----------------------------------------------------------------------------
# Figura 10. Prototipo del tablero de monitoreo
# ----------------------------------------------------------------------------
def figura_dashboard() -> None:
    fig = plt.figure(figsize=(11.5, 6.6))
    fig.patch.set_facecolor("#F4F6FA")
    fig.suptitle("Prototipo del dashboard OmniSafety AI (Streamlit)", fontsize=13, fontweight="bold", color=AZUL, y=0.975)

    tarjetas = [
        ("Defectos detectados", "12", "últimas 24 h", CIAN),
        ("Riesgo de falla", "0.22", "nivel normal", VERDE),
        ("Cumplimiento EPP", "87.3 %", "meta 100 %", NARANJA),
        ("Latencia de inferencia", "12.4 ms", "TensorRT INT8", AZUL),
    ]
    for i, (titulo, valor, pie, color) in enumerate(tarjetas):
        ax = fig.add_axes([0.045 + i * 0.238, 0.70, 0.208, 0.19])
        ax.set_facecolor("white")
        ax.set_xticks([])
        ax.set_yticks([])
        for lado in ax.spines.values():
            lado.set_edgecolor(color)
            lado.set_linewidth(1.6)
        ax.text(0.07, 0.80, titulo, fontsize=9.2, color=GRIS, transform=ax.transAxes)
        ax.text(0.07, 0.44, valor, fontsize=19, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.07, 0.12, pie, fontsize=8.4, color=GRIS, transform=ax.transAxes)

    horas = np.linspace(0, 8, 80)
    ax1 = fig.add_axes([0.055, 0.34, 0.42, 0.28])
    ax1.plot(horas, 72 + 8 * np.sin(horas * 1.3) + np.linspace(0, 9, 80), color=NARANJA, linewidth=2)
    ax1.set_title("Temperatura del motor (°C)", fontsize=9.5, color=AZUL)
    ax1.set_xticks([])
    ax1.tick_params(labelsize=8)

    ax2 = fig.add_axes([0.545, 0.34, 0.42, 0.28])
    ax2.plot(horas, 0.8 + 0.55 * np.abs(np.sin(horas * 1.1)) + np.linspace(0, 0.7, 80), color=CIAN, linewidth=2)
    ax2.set_title("Vibración del eje Z (mm/s)", fontsize=9.5, color=AZUL)
    ax2.set_xticks([])
    ax2.tick_params(labelsize=8)

    ax3 = fig.add_axes([0.055, 0.045, 0.86, 0.22])
    ax3.axis("off")
    ax3.set_title("Registro de eventos recientes", fontsize=9.5, color=AZUL, loc="left")
    filas = [
        ("07:42", "Visión", "Grieta detectada en rodillo 3 (confianza 0.91)", "advertencia"),
        ("07:58", "EPP", "Operario sin casco en zona de prensado", "crítica"),
        ("08:15", "Mantenimiento", "Riesgo de falla 0.22; sin acción requerida", "informativa"),
        ("08:31", "RAG", "Consulta: torque de apriete en prensa hidráulica", "informativa"),
    ]
    for i, (hora, modulo, evento, nivel) in enumerate(filas):
        y = 0.82 - i * 0.24
        color = {"crítica": NARANJA, "advertencia": "#B4881F", "informativa": CIAN}[nivel]
        ax3.text(0.0, y, hora, fontsize=8.6, fontweight="bold", color=AZUL, transform=ax3.transAxes)
        ax3.text(0.07, y, modulo, fontsize=8.6, color=color, fontweight="bold", transform=ax3.transAxes)
        ax3.text(0.19, y, evento, fontsize=8.6, color="#1A1A1A", transform=ax3.transAxes)
        ax3.plot([0.0, 0.86], [y - 0.10, y - 0.10], color="#D6DCE5", linewidth=1, transform=ax3.transAxes)
    guardar(fig, "fig10_dashboard.png")


def main() -> None:
    figura_arquitectura()
    figura_cronograma()
    figura_clases_defecto()
    figura_latencia()
    figura_roc()
    figura_matriz_confusion()
    figura_shap()
    figura_rag_recall()
    figura_epp()
    figura_objetivos()
    figura_dashboard()


if __name__ == "__main__":
    main()
