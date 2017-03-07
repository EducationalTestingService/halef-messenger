from . import create_app
from .extensions import celery

app = create_app("production", False)

