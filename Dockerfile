# Dockerfile para Producción
# --------------------------
# Este archivo crea una imagen optimizada, ligera y segura para el despliegue final.
# - Instala únicamente las dependencias estrictamente necesarias para ejecutar la aplicación.
# - Utiliza Gunicorn como servidor WSGI robusto.
# - No incluye herramientas de testing o depuración.

FROM python:3.13-slim

ENV BACKEND_ENV production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN groupadd -r appuser && useradd --no-create-home -r -g appuser appuser

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates

RUN apt-get install -y curl htop iputils-ping 
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false &&
RUN rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /home/appuser

USER appuser

COPY ./pyproject.toml ./

RUN uv sync --locked && \
    pip install --no-cache-dir gunicorn==22.0.0

COPY ./app ./

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--log-level", "INFO"]