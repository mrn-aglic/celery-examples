from celery.utils.log import get_task_logger
from workflows.celeryapp import app
from workflows.worker.test_tasks import (
    insert_chain,
    print_task,
    simple_pipeline,
    split_group,
)

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        print_task.pipeline.apply_async(countdown=15)
        simple_pipeline.pipeline.apply_async(countdown=30)
        insert_chain.pipeline.apply_async(countdown=45)
        split_group.pipeline.apply_async(countdown=60)

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
