import config


class BaseConfig:
    """ Basic settings required by all classes """
    SECRET_KEY = config.SECRET_KEY
    # TESTING = True
    # Flask
    DEBUG = config.DEBUG

    # flask mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = config.SENDER_EMAIL
    MAIL_PASSWORD = config.SENDER_PASS
    MAIL_DEFAULT_SENDER = config.SENDER_EMAIL
    MAIL_DEBUG = config.DEBUG
    MAIL_SUPPRESS_SEND = config.DEBUG


class TestingConfig(BaseConfig):
    """ Testing settings  """
    TESTING = True


class EmailTestingConfig(BaseConfig):
    """Config settings to test email templates"""
    TESTING = True
    MAIL_SUPPRESS_SEND = False


class ProdConfig(BaseConfig):
    """Production settings"""
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
