from workflows.celeryapp import app


@app.task
def printer(task_arg):
    print(task_arg)


@app.task
def some_task(*arg, a=None, b=None, c=None):
    print("some_task called with:")
    print(f"arg: {arg}")
    print(f"a: {a}, b: {b}, c: {c}")


@app.task
def pipeline():
    return printer.s(some_task.s([1, 2, 3], a=15)).apply_async()
