import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '51f52814-0071-11e6-a247-000ec6c2372c')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
    SOCKETIO_MESSAGE_QUEUE = os.environ.get(
        'SOCKETIO_MESSAGE_QUEUE', 'redis://redis:6379/0')
    CELERY_CONFIG = {}
    APPLICATION_ROOT = os.environ.get('MESSENGER_ROOT', '/messenger')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SOCKETIO_MESSAGE_QUEUE = None


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
