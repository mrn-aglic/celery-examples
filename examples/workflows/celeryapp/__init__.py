from celery import Celery

from . import celeryconfig
from .celeryconfig import task_queues

app = Celery("workflows")
app.config_from_object(celeryconfig)

app.control.purge()
