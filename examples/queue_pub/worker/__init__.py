from celery.utils.log import get_task_logger
from queue_pub.celeryapp import app

from .other_queue_tasks.other_queue_task import other_queue_task_manager
from .rate_limit import rate_limiter
from .test_tasks.test_task import test_task_manager

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    app.control.purge()

    try:
        logger.info("Send some messages")

        test_task_manager.apply_async(countdown=3)
        other_queue_task_manager.apply_async(countdown=3)

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
