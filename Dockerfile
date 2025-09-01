FROM python:3.13-slim

ENV BACKEND_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    htop \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd --no-create-home -r -g appuser appuser

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

WORKDIR /home/appuser

COPY ./pyproject.toml ./uv.lock ./ 
RUN uv sync --locked

COPY ./app ./app

RUN chown -R appuser:appuser /home/appuser

USER appuser

ENV PATH="/home/appuser/.venv/bin:$PATH"

EXPOSE 5000

CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--workers", "4", "--log-level", "INFO"]
