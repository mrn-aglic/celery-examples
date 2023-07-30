from celery.utils.log import get_task_logger
from workflows.celeryapp import app
from workflows.worker.test_tasks import print_task, simple_pipeline

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        # print_task.pipeline.apply_async(countdown=15)
        simple_pipeline.pipeline.apply_async(countdown=15)

        # sender.add_periodic_task(2.0, print_pipeline.pipeline.s(), name="workflows_pipeline_a")
        # sender.add_periodic_task(5.0, simple_pipeline.pipeline_branch.s(), name="workflows_pipeline_b")

        # print_pipeline.s().apply_async()

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
