import os
from flask import Flask
try:
    from .config.config import config_by_name
except ImportError:
    from config.config import config_by_name

from .db import db_manager
from .routes import api as api_blueprint

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("BACKEND_ENV", "development")

    app = Flask(name)
    config = config_by_name[config_name]
    app.config.from_object(config)

    db_manager.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

app = create_app()