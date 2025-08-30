import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    MONGO_URI = os.getenv('MONGO_URI')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI_DEV', 'mongodb://localhost:27017/test_db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI_TEST', 'mongodb://localhost:27017/test_db')

class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.getenv('MONGO_URI_PROD')

config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
