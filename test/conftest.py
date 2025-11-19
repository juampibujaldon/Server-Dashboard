import os

import pytest

os.environ["BACKEND_ENV"] = "testing"
os.environ.setdefault("MONGO_URI_TEST", "mongodb://monitoreo_user:monitoreo_pass@localhost:27017/TEST_MONITOREAR?authSource=admin")

from app import create_app
from app.db import db_manager


@pytest.fixture(scope="session")
def app_instance():
    return create_app()

@pytest.fixture(scope="session")
def client(app_instance):
    with app_instance.test_client() as c:
        with app_instance.app_context():
            yield c

@pytest.fixture(scope="session")
def db(app_instance):
    with app_instance.app_context():
        database = db_manager.get_db()
        for col in ("metrics", "servers", "alerts"):
            database[col].delete_many({})
        yield database
        for col in ("metrics", "servers", "alerts"):
            database[col].delete_many({})