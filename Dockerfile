# Dockerfile para Producción
# --------------------------
# Este archivo crea una imagen optimizada, ligera y segura para el despliegue final.
# - Instala únicamente las dependencias estrictamente necesarias para ejecutar la aplicación.
# - Utiliza Gunicorn como servidor WSGI robusto.
# - No incluye herramientas de testing o depuración.

FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN groupadd -r appuser && useradd --no-create-home -r -g appuser appuser

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential
RUN apt-get install -y curl htop iputils-ping 
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && 
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /home/appuser

USER appuser

COPY app/pyproject.toml ./

RUN pip install uv && \
    uv sync && \
    pip install --no-cache-dir gunicorn==22.0.0

COPY app/src ./src

EXPOSE 5000

CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]