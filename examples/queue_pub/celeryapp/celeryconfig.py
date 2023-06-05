from kombu import Exchange, Queue

broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/1"

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
enable_utc = True

task_create_missing_queues = True

task_soft_time_limit = 2 * 60 * 60 * 60
task_time_limit = task_soft_time_limit + 60
worker_prefetch_multiplier = 1
worker_concurrency = 1


default_exchange = Exchange("default", type="direct")
other_exchange = Exchange("other_queue", type="direct")
rate_limited_worker_exchange = Exchange("rate_limited", type="direct")

default_queue = Queue("default", default_exchange)
other_queue = Queue("other_queue", other_exchange)
rate_limited_queue = Queue("rate_limited", rate_limited_worker_exchange)

task_queues = (
    default_queue,
    other_queue,
    rate_limited_queue,
)

task_routes = {
    "queue_pub.worker.other_queue_tasks.*": {"queue": "other_queue"},
}

task_default_exchange = default_exchange
task_default_queue = "default"

# Enable events
worker_send_task_events = True
task_send_sent_event = True
