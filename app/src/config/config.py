import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://monitoreo_user:monitoreo_pass@localhost:27017/DEV_MONITOREAR?authSource=admin')

class TestConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI_TEST', 'mongodb://monitoreo_user:monitoreo_pass@localhost:27017/TEST_MONITOREAR?authSource=admin')

config_by_name = {
    "development": Config,
    "testing": TestConfig,
}