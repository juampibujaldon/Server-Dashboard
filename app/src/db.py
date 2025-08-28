import os
from pymongo import MongoClient
from config.config import config_by_name 


config_name = os.getenv("BACKEND_ENV", "development")

config = config_by_name[config_name]

client = MongoClient(config.MONGO_URI)

db_name = client.get_default_database().name
db = client[db_name]

print(f"Conexión a MongoDB inicializada para la base de datos: {db.name} (Entorno: {config_name})")