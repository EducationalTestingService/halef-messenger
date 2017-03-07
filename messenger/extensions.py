import os

from flask_redis import FlaskRedis
from flask_socketio import SocketIO
from celery import Celery


redis_store = FlaskRedis()
socketio = SocketIO()
celery = Celery(__name__,
                broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
                backend=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'))