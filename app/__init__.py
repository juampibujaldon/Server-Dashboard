import os
from flask import Flask
from .config.config import config_by_name
from .db import db_manager

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("BACKEND_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db_manager.init_app(app)

    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
