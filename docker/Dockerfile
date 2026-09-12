# ============================================================
# OmniSafety AI - Imagen del ecosistema
# ============================================================
# Construcción desde la raíz del proyecto:
#
#     docker build -f docker/Dockerfile -t omnisafety-ai .
#
# O mediante Docker Compose:
#
#     docker compose up --build
# ============================================================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del sistema requeridas por OpenCV y las herramientas de compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python (capa cacheable)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Código fuente, configuración y activos necesarios en tiempo de ejecución
COPY src/ ./src/
COPY config/ ./config/

# Carpetas de datos y entregables
RUN mkdir -p data/raw data/processed data/models docs/figuras docs/entregables

EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto: API REST
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
