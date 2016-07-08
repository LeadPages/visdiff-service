import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    configuration settings for all environments
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or\
        'a string that would be tough to guess'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    configuration settings for development
    """
    DEBUG = True


class TestingConfig(Config):
    """
    configuration settings for testing
    """
    TESTING = True


class ProductionConfig(Config):
    """
    configuration settings for production
    """
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
