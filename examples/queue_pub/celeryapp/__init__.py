from celery import Celery, bootsteps, signals
from kombu import Consumer, Exchange, Queue

from . import celeryconfig
from .celeryconfig import task_queues

app = Celery("queue_pub")
app.config_from_object(celeryconfig)

app.control.purge()
