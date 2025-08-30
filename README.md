# Server Dashboard API

## Descripción

**Server Dashboard API** es un backend desarrollado en Flask diseñado para recibir, almacenar y gestionar métricas de rendimiento de servidores. Este sistema permite a agentes de monitoreo enviar datos como el uso de CPU, RAM, espacio en disco y temperatura, los cuales son almacenados en una base de datos MongoDB para su posterior análisis y visualización. La API cuenta con un sistema de autenticación basado en JWT para proteger sus endpoints.

## Características Principales

-   **Recepción de Métricas**: Endpoint para que los agentes de monitoreo envíen los datos de rendimiento del servidor.
    
-   **Almacenamiento en MongoDB**: Las métricas recibidas se almacenan en una base de datos MongoDB para su persistencia y consulta.
    
-   **Autenticación JWT**: Los endpoints están protegidos y requieren un token JWT para su acceso, con un endpoint de `/login` para obtener el token.
    
-   **Configuración por Entornos**: El sistema está configurado para ejecutarse en diferentes entornos (desarrollo, testing y producción) utilizando archivos de configuración específicos.
    
-   **Contenerización con Docker**: El proyecto incluye un `Dockerfile` y un archivo `docker-compose.yml` para facilitar el despliegue en contenedores.
    
-   **Testing**: Incluye una suite de tests unitarios y de integración para asegurar el correcto funcionamiento de la API.
    
## Tecnologías Utilizadas

-   **Backend**: Flask
    
-   **Base de Datos**: MongoDB (a través de PyMongo)
    
-   **Servidor WSGI**: Gunicorn
    
-   **Autenticación**: JSON Web Tokens (PyJWT)
    
-   **Gestión de Dependencias**: uv
    
-   **Contenerización**: Docker
    
-   **Testing**: Pytest
    

## Estructura del Proyecto

```
Server-Dashboard/
├── app/
│   ├── config/
│   │   └── config.py
│   ├── models/
│   │   ├── alert.py
│   │   ├── metric.py
│   │   └── server.py
│   ├── services/
│   │   └── metric_services.py
│   ├── __init__.py
│   ├── db.py
│   └── routes.py
├── docker/
│   ├── docker-compose.yml
│   └── .env
├── documents/
│   ├── caso de uso.png
│   └── diagrama de clase.png
├── test/
│   ├── test_app.py
│   └── test_metric.py
├── .env
├── app.py
├── Dockerfile
├── pyproject.toml
└── uv.lock

```

## Instalación y Configuración

### Prerrequisitos

-   Python 3.13
    
-   Docker y Docker Compose
    
-   `uv` (manejador de paquetes de Python)
    

### Instalación

1.  **Clona el repositorio**:
    
    Bash
    
    ```
    git clone "https://github.com/juampibujaldon/Server-Dashboard"
    cd Server-Dashboard
    
    ```
    
2.  Instala las dependencias:
    
    Utiliza uv para instalar las dependencias definidas en pyproject.toml y uv.lock.
    
    Bash
    
    ```
    uv sync
    
    ```
    


### Configuración

1.  **Crea un archivo `.env`**: Copia el archivo `.env.example` o crea un nuevo archivo `.env` en la raíz del proyecto. Este archivo contendrá las variables de entorno para la configuración de la base de datos y las credenciales de administrador.
    
    **.env.example:**
    
    ```
    # Se ejecuta de manera local.
    BACKEND_ENV=development
    
    # Clave secreta para la firma de JWT y otras funciones de seguridad.
    # Se recomienda generar una clave segura y única para producción.
    SECRET_KEY=
    
    # Cadenas de conexión a MongoDB para los diferentes entornos.
    # Reemplaza los valores con tus propias credenciales y configuración.
    MONGO_URI_PROD=mongodb://<usuario>:<contraseña>@<host>:<puerto>/<base_de_datos_prod>?authSource=admin
    MONGO_URI_DEV=mongodb://<usuario>:<contraseña>@<host>:<puerto>/<base_de_datos_dev>?authSource=admin
    MONGO_URI_TEST=mongodb://<usuario>:<contraseña>@<host>:<puerto>/<base_de_datos_test>?authSource=admin
    
    ```
    
2.  **Configuración para Docker**: Asegúrate de que el archivo `docker/.env.example` esté configurado con las variables necesarias para el entorno de Docker.
    

## Uso

### Ejecutar la Aplicación

#### Con Docker Compose

Para levantar el servicio de backend junto con la base de datos MongoDB, utiliza Docker Compose:

Bash

```
docker-compose up -d

```

La API estará disponible en `http://localhost:5000`.

#### De forma local

Si prefieres ejecutar la aplicación de forma local para desarrollo:

Bash

```
flask run

```

### Endpoints de la API

-   POST /api/auth/login:
    
    Autentica a un usuario y devuelve un token JWT.
    
    **Body**:
    
    JSON
    
    ```
    {
        "username": "admin",
        "password": "S3cr3t4dm1n"
    }
    
    ```
    
-   POST /api/metrics:
    
    Envía una nueva métrica del servidor. Requiere un token JWT en la cabecera Authorization.
    
    **Body**:
    
    JSON
    
    ```
    {
        "serverId": "server-01",
        "cpu_usage": 75.5,
        "ram_usage": 5.2
    }
    
    ```
    
-   GET /api/metrics/<server_id>:
    
    Obtiene todas las métricas de un servidor específico. Requiere un token JWT.
    

## Testing

Para ejecutar la suite de tests, utiliza Pytest:

Bash

```
pytest

```

Esto ejecutará todos los tests definidos en el directorio `test/`.