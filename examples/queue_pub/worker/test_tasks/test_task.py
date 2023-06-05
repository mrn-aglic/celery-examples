from queue_pub.celeryapp import app


@app.task(bind=True)
def test_task(self, test_arg=None):
    print("Test task")
    print(f"ARG: {test_arg}")

    print(self.request.delivery_info)


@app.task()
def test_task_manager():
    print("Test_task_manager")

    async_result = None

    try:
        async_result = test_task.s(test_arg="MyTest").apply_async(queue="rate_limited")
    except Exception as ex:
        print(ex)

    print(f"async_result: {async_result}")
