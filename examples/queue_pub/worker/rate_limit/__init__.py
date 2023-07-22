import typing

import kombu
from celery import Celery, Task
from celery.app.routes import MapRoute
from celery.result import AsyncResult
from queue_pub.celeryapp import app, celeryconfig


def message_to_dict(message: kombu.Message) -> dict:
    return {"headers": {**message.headers}, "body": tuple(message.decode())}


def pick_from_queue(celeryapp: Celery, queue="rate_limited"):
    with celeryapp.connection_for_read() as conn:
        msg = conn.default_channel.basic_get(queue, no_ack=True)

    return msg


def _get_queue_name(task_name: str) -> str:
    if not hasattr(celeryconfig, "task_routes"):
        return celeryconfig.default_queue.routing_key

    route_map = MapRoute(celeryconfig.task_routes)

    for pattern, queue in route_map.patterns.items():
        result = pattern.findall(task_name)
        if any(result):
            return queue["queue"]

    return celeryconfig.default_queue.name


def get_routing_key_and_exchange(
    celeryapp: Celery, task_name: str
) -> typing.Tuple[str, str]:
    router = celeryapp.amqp.router

    queue_name = _get_queue_name(task_name)

    # queue = celeryapp.select_queues([queue_name])
    queue = router.queues[queue_name]

    return queue.routing_key, queue.exchange


def publish_task(
    celeryapp: Celery,
    message: kombu.Message,
    routing_key: str = celeryconfig.default_queue.routing_key,
    exchange_name: str = celeryconfig.default_queue.name,
):
    try:
        with celeryapp.connection_for_write() as conn:
            # get a producer from the connection
            producer = conn.Producer()

            msg = message_to_dict(message)

            print(
                f"Publishing task {msg['headers']['task']} to queue: {exchange_name} with routing key: {routing_key}"
            )

            producer.publish(
                body=msg["body"],
                headers=msg["headers"],
                exchange=exchange_name,
                routing_key=routing_key,
            )
    except Exception as ex:
        print(ex)


def send_task(celeryapp: Celery, message: kombu.Message):
    body = message.decode()
    args, kwargs, embed = body

    callbacks = embed["callbacks"]
    errbacks = embed["errbacks"]

    headers = {**message.headers}
    task_name = headers["task"]
    task_id = headers["id"]

    shadow = headers.get("shadow")

    headers.pop("task")
    headers.pop("id")
    headers.pop("shadow")

    properties = message.properties

    options = {**headers, **properties}

    celeryapp.send_task(
        name=task_name,
        args=args,
        kwargs=kwargs,
        # keep the task_id
        task_id=task_id,
        # shadow
        shadow=shadow,
        # callbacks
        link=callbacks,
        link_error=errbacks,
        # result class to use
        result_cls=AsyncResult,
        # task type to use
        task_type=Task,
        **options,
    )


@app.task(bind=True)
def rate_limiter(self):
    print("Checking queue...")
    celeryapp = self.app

    message = pick_from_queue(celeryapp)

    if message is not None:
        name = message.headers["task"]

        routing_key, exchange_name = get_routing_key_and_exchange(celeryapp, name)

        publish_task(
            celeryapp, message, routing_key=routing_key, exchange_name=exchange_name
        )
        # send_task(celeryapp, message)
