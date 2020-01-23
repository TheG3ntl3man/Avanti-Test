""" API config File """
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Config(object):
    """ Parent configuration class """
    DEBUG = False
    TESTING = False
    Database_Url = os.getenv("DATABASE_URL") or os.getenv(f"{os.getenv('FLASK_ENV')}_Database")
    SECRET_KEY = os.getenv("SECRET")


class DevelopmentConfig(Config):
    """ Configuration for development environment """
    DEBUG = True


class TestingConfig(Config):
    """ Configuratio(env) zonecc@trevor:/var/codezonecc/My Diary$n for the testing environment """
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """ Configuration for the production environment """
    DEBUG = False
    TESTING = False


environments = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig
}
