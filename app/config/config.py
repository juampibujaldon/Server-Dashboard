import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('MONGO_APP_USER', 'monitoreo_user')
PASSWORD = os.getenv('MONGO_APP_PASSWORD', 'monitoreo_pass')
DOCKER_HOST = os.getenv('MONGO_HOST', 'mongodb-servidor')
DB_DEV = os.getenv('MONGO_DB_DEV', 'DEV_MONITOREAR')
DB_TEST = os.getenv('MONGO_DB_TEST', 'TEST_MONITOREAR')

class Config:
    MONGO_URI = f"mongodb://{USER}:{PASSWORD}@{DOCKER_HOST}:27017/{DB_DEV}?authSource=admin"

class TestConfig(Config):
    TESTING = True
    MONGO_URI = f"mongodb://monitoreo_user:monitoreo_pass@localhost:27017/{DB_TEST}?authSource=admin"

config_by_name = {
    "development": Config,
    "testing": TestConfig,
}