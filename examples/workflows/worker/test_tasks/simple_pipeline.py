import typing

from workflows.celeryapp import app


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
def square_list(self, xs: typing.List[int]):
    print_info(self)

    return [a**2 for a in xs]


@app.task(bind=True)
def print_result(self, *arg):
    result = arg[0]
    print_info(self)

    print(f"print_result arg: {result}")


@app.task(bind=True)
def pipeline(self):
    print_info(self)
    return (return_list.s(n=5) | square_list.s() | print_result.s()).apply_async()
