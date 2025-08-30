from flask import current_app, g
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
import os
import time

class DBManager:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        mongo_uri = app.config.get('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI no está configurada en la aplicación Flask.")

        max_attempts = int(os.getenv("MONGO_CONNECT_MAX_ATTEMPTS", "10"))
        initial_delay_seconds = float(os.getenv("MONGO_CONNECT_INITIAL_DELAY", "0.5"))
        attempt = 0
        delay = initial_delay_seconds

        while attempt < max_attempts:
            attempt += 1
            try:
                self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
                self.client.admin.command('ping')
                print(f"Conexión a MongoDB OK en intento {attempt}")
                break
            except (ServerSelectionTimeoutError, ConfigurationError) as exc:
                print(f"Intento {attempt}/{max_attempts} de conectar a MongoDB falló: {exc}")
                if attempt >= max_attempts:
                    raise
                time.sleep(delay)
                delay = min(delay * 2, 5.0)

        @app.teardown_appcontext
        def close_db(exception):
            pass

    def get_db(self):
        if not self.client:
            raise RuntimeError("La base de datos no ha sido inicializada. Llama a init_app primero.")

        db_name = self.client.get_default_database().name
        return self.client[db_name]

db_manager = DBManager()