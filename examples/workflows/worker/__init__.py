from os import environ

from celery.utils.log import get_task_logger
from workflows.celeryapp import app
from workflows.worker.test_tasks import insert_chain, print_task, simple_pipeline

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        logger.info("Send some messages")
        # print_task.pipeline.s().apply_async()

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
