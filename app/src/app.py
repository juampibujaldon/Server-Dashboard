import os
from flask import Flask
from config.config import config_by_name
from db import db
from routes import api as api_blueprint

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("BACKEND_ENV", "development")

    app = Flask(__name__)
    config = config_by_name[config_name]
    app.config.from_object(config)
    
    with app.app_context():
        app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app