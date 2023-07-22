from celery.signals import after_task_publish
from celery.utils.log import get_task_logger
from queue_pub.celeryapp import app
from queue_pub.worker.rate_limit import rate_limiter

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        sender.add_periodic_task(2.0, rate_limiter.s(), name="google_rate_limiter")

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
