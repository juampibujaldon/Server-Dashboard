
# Backend para Sistema de Monitoreo de Servidores

Este repositorio contiene el código fuente del **Backend Central**, un componente clave del sistema de monitoreo de servidores. Desarrollado en Python con Flask, su función principal es recibir, almacenar y procesar las métricas enviadas por los agentes de monitoreo.

## 📖 Descripción General

El backend expone una API REST para centralizar toda la información de los servidores monitoreados. Actúa como el cerebro del sistema, gestionando los datos históricos, la configuración de alertas y proveyendo los endpoints necesarios para que el dashboard visualice la información.

## ✨ Características Principales

  * **API REST Robusta**: Recibe métricas (CPU, RAM, disco, temperatura) de múltiples agentes de forma segura.
  * **Almacenamiento Persistente**: Guarda el historial de métricas y la configuración del sistema en una base de datos **MongoDB**.
  * **Sistema de Alertas**: Ofrece endpoints para configurar umbrales y condiciones que disparan notificaciones automatizadas.
  * **Integración Sencilla**: Diseñado para conectarse fácilmente con un dashboard (como Grafana o uno personalizado) y servicios de notificación (Email, Slack, etc.).
  * **Contenerizado con Docker**: Se distribuye con un `Dockerfile` para un despliegue rápido, consistente y aislado.

## 🛠️ Prerrequisitos

Para ejecutar este proyecto, necesitarás:

  * [Docker](https://www.google.com/search?q=https-www.docker.com-get-started) y [Docker Compose](https://www.google.com/search?q=https-docs.docker.com-compose-install-)
  * [Python](https://www.google.com/search?q=https-www.python.org-downloads-) 3.11+
  * [uv](https://www.google.com/search?q=https-github.com-astral-sh-uv) (Recomendado para gestionar el entorno virtual)

## 🚀 Puesta en Marcha con Docker (Recomendado)

La forma más sencilla de levantar todo el entorno (backend y base de datos) es con Docker Compose.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/juampibujaldon/Server-Dashboard-
    cd Server-Dashboard-/app
    ```
2.  **Configura las variables de entorno:**
    Crea un archivo `.env` a partir del ejemplo y ajústalo con tus credenciales para la base de datos.
    ```bash
    cp .env.example .env
    # Abre y edita el archivo .env
    ```
3.  **Levanta los servicios:**
    Este comando construirá las imágenes y levantará los contenedores del backend y de MongoDB en segundo plano.
    ```bash
    docker-compose up --build -d
    ```
4.  **Verifica que todo funcione:**
    La API debería estar disponible en `http://localhost:8000`. Puedes probar el endpoint de status:
    ```bash
    curl http://localhost:8000/api/status
    ```
    Deberías recibir una respuesta como: `{"status": "ok"}`.

## ⚙️ Desarrollo Local (Sin Docker)

Sigue estos pasos para configurar y correr el proyecto en tu máquina local.

1.  **Clona el repositorio (si aún no lo has hecho):**

    ```bash
    git clone https://github.com/juampibujaldon/Server-Dashboard-
    cd Server-Dashboard-/app
    ```

2.  **Crea y activa el entorno virtual:**
    Usaremos `uv` para crear un entorno virtual llamado `.venv`.

    ```bash
    uv venv
    source .venv/bin/activate
    ```

    *En Windows, el comando de activación es `.venv\Scripts\activate`*.

3.  **Instala todas las dependencias:**
    Este comando lee el archivo `pyproject.toml` e instala las dependencias del proyecto y las de desarrollo (como `pytest` y `uvicorn`).

    ```bash
    uv pip install ".[dev]"
    ```

4.  **Instala el proyecto en modo editable:**
    Este es un paso crucial. Hace que tu aplicación sea "instalable" en el entorno, solucionando problemas de importación.

    ```bash
    uv pip install -e .
    ```

5.  **Configura las variables de entorno:**
    Copia el archivo de ejemplo y configúralo para el entorno de desarrollo.

    ```bash
    cp .env.example .env
    # Edita el .env si es necesario para que coincida con tu base de datos local
    ```

6.  **Ejecuta la aplicación:**
    Ahora puedes iniciar el servidor con Uvicorn. La bandera `--reload` hará que el servidor se reinicie automáticamente cuando detecte cambios en el código.

    ```bash
    uv run uvicorn src.main:app --reload
    ```

    La API estará disponible en `http://12-7.0.0.1:8000`.

## 🧪 Ejecución de Tests

Para asegurar la calidad y el correcto funcionamiento de la API, puedes ejecutar la suite de pruebas.

1.  **Asegúrate de tener un MongoDB para tests:**
    Puedes usar la instancia de Docker para esto.
    ```bash
    docker-compose up -d mongo
    ```
2.  **Ejecuta los tests con `pytest`:**
    Asegúrate de que tu entorno virtual esté activado.
    ```bash
    uv run pytest -v
    ```

## 📁 Estructura del Proyecto

```
/
├── src/                  # Código fuente de la aplicación
│   ├── config/           # Módulos de configuración
│   ├── models/           # Modelos de datos
│   ├── routes/           # Lógica de los endpoints (en routes.py)
│   ├── services/         # Lógica de negocio
│   ├── app.py            # Fábrica de la aplicación Flask
│   └── db.py             # Configuración de la conexión a la BD
├── tests/                # Pruebas unitarias y de integración
├── .env.example          # Ejemplo de variables de entorno
├── docker-compose.yml    # Orquestación de contenedores
├── Dockerfile            # Definición del contenedor del backend
└── pyproject.toml        # Dependencias y configuración del proyecto
```