import os
from flask import Flask
from .config.config import config_by_name
from .db import db_manager 

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("BACKEND_ENV", "development")

    app = Flask(name)
    config = config_by_name[config_name]
    app.config.from_object(config)

    db_manager.init_app(app)

    from .routes import api as api_blueprint
    from .routes import auth_bp as auth_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    return app