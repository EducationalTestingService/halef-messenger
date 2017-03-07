import os

from flask import Flask

from .config import config
from .extensions import redis_store, socketio, celery
from .api import events  # noqa
from .tasks import send_message # noqa


def create_app(config_name=None, main=True, settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param: config_name: 'development', 'production', 'testing'
    :param: main: True if this runs as server, False if this runs as worker
    :param settings_override: Override settings
    :return: Flask app
    """

    # If MESSENGER_CONFIG is not set, run in development mode
    if config_name is None:
        config_name = os.environ.get('MESSENGER_CONFIG', 'development')

    # Initialize Flask application instance
    app = Flask(__name__)

    # Load config from ../config.py
    app.config.from_object(config[config_name])


    # Manually overwrite any settings
    if settings_override:
        app.config.update(settings_override)

    # Register blueprints
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix=app.config['APPLICATION_ROOT'])

    from .health_check import health_check as health_check_blueprint
    app.register_blueprint(health_check_blueprint, url_prefix=app.config['APPLICATION_ROOT'])

    # Initialize extensions
    extensions(app, main)

    return app


def extensions(app, main):
    """
    Register 0 or more extensions (Mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    redis_store.init_app(app)
    if main:
        # Initialize SocketIO as server and connect it to the message queue.
        socketio.init_app(app,
                          message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
                          async_mode='eventlet',
                          path=app.config['APPLICATION_ROOT'] + '/socketio')
    else:
        # Initialize SocketIO to emit events through the message queue.
        # Celery does not use eventlet. Therefore, we have to set async_mode
        # explicitly.
        socketio.init_app(None,
                          message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
                          async_mode='threading')
    celery.conf.update(app.config)

    return None
