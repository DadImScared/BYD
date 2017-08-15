import config


class BaseConfig:
    """ Basic settings required by all classes """
    SECRET_KEY = config.SECRET_KEY
    # TESTING = True
    # Flask
    DEBUG = config.DEBUG


class TestingConfig(BaseConfig):
    """ Testing settings  """
    TESTING = True
