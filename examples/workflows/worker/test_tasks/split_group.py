import typing

import celery
from celery import shared_task, subtask, group, chain
from workflows.celeryapp import app


@app.task
def log_error(request, exc, traceback):
    print("--\n\nLOG ERROR: ")
    print(f"request.id: {request.id}")
    print(f"exc: {exc}")
    print(f"traceback: {traceback}")


def print_info(self):
    print(f"{self.name} has parent with task id {self.request.parent_id}")
    print(f"chain of {self.name}: {self.request.chain}")
    print(f"self.request.id: {self.request.id}")

    if self.request.chain is not None:
        print("tasks in chain:")
        print([t["task"] for t in self.request.chain])


@app.task(bind=True)
def return_list(self, n: int):
    print_info(self)

    return list(range(n))


@app.task(bind=True)
def square(self, a: int):
    print_info(self)

    # raise ValueError("MY VALUE ERROR")
    # return [b**2 for b in a]
    return a**2


@app.task(bind=True)
def tsum(self, result: typing.List[int]):
    print_info(self)

    return sum(result)


@app.task(bind=True)
def print_result(self, *arg):
    result = arg[0]
    print_info(self)

    print(f"print_result arg: {result}")



class mychain(celery.canvas._chain):
    def __call__(self, *args, **kwargs):
        print("CHAIN ARGS:")
        print(args)
        if self.tasks:
            return self.apply_async(args, kwargs)


def mycall(self, *args, **kwargs):
    print("CHAIN ARGS:")
    print(args)
    if self.tasks:
        return self.apply_async(args, kwargs)


app_async = celery.canvas._chain.apply_async
gapp_async = celery.canvas.group.apply_async

def myapply_async(self, args=None, kwargs=None, **options):
    print("CHAIN ARGS:")
    print(args)
    print(kwargs)
    print(options)
    return app_async(self, args, kwargs, **options)



def mygapply_async(self, args=None, kwargs=None, **options):
    print("CHAIN ARGS FRO GROUP:")
    print(args)
    print(kwargs)
    print(options)
    return gapp_async(self, args, kwargs, **options)



celery.canvas._chain.__call__ = mycall
celery.canvas._chain.apply_async = myapply_async
celery.canvas.group.apply_async = mygapply_async
celery.canvas.group.__call__ = mycall


@shared_task(bind=True)
def split_group(self, result=None, branch=None):
    print_info(self)

    branches = []

    subtask_type = branch["subtask_type"]
    tasks = branch["kwargs"].get("tasks", [])

    for val in result:

        if subtask_type == "chain" and any(tasks):
            rest_tasks = [subtask(task).clone() for task in tasks[1:]]
            first_task = subtask(tasks[0]).clone(args=(val,))
            chain_tasks = [first_task, *rest_tasks]
            sig = chain(*chain_tasks)
        else:
            s = subtask(branch)
            sig = s.clone(args=(val,))


        branches.append(sig)

    g = group(branches)

    return self.replace(g)


@shared_task(bind=True)
def split_group_simpler(self, result=None, branch=None):
    print_info(self)

    branches = []

    s = subtask(branch)

    for val in result:

        sig = s.clone(args=(val,))

        if isinstance(s, celery.canvas._chain):
            first_task = sig.tasks[0]
            first_task.args = (val,)

        branches.append(sig)

    g = group(branches)

    return self.replace(g)

# .on_error(log_error.s())

@app.task
def pipeline():
    output = square.s() | print_result.s()

    return (
        return_list.s(n=5) | split_group.s(output)
    ).apply_async()

