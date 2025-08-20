import os
from flask import Flask
from pymongo import MongoClient
from config.config import config_by_name

def create_app():
    env = os.getenv("BACKEND_ENV", "development")
    app = Flask(__name__)
    config = config_by_name[env]
    app.config.from_object(config)

    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_database()
    print(f"Conectado a la base de datos: {db.name} (Entorno: {env})")

    app.db = db
    
    with app.app_context():
        from routes import api as api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app