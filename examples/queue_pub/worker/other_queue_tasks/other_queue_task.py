from queue_pub.celeryapp import app


@app.task(bind=True)
def my_other_queue_task(self):
    print("Called other queue_task")
    print(self.request.delivery_info)


@app.task
def other_queue_task_manager():
    print("Other_queue_task_manager")

    async_result = None

    try:
        async_result = my_other_queue_task.s().apply_async(queue="rate_limited")
    except Exception as ex:
        print(ex)

    print(f"async_result: {async_result}")
