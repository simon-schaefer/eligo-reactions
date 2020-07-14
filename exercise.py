import functools
import operator
import random
import time
import typing

from geometry import Shape


class Exercise:

    operators = {"+": lambda x: functools.reduce(operator.__add__, x),
                 "-": lambda x: functools.reduce(operator.__sub__, x),
                 "x": lambda x: functools.reduce(operator.__mul__, x),
                 "/": lambda x: functools.reduce(operator.__truediv__, x)}

    def __init__(self, num_shapes: int = 2):
        self._num_shapes = num_shapes
        self._task = None
        self._solution = None
        self._timer = None

        self._counter = -1

    def new_task(self):
        shapes_dict = []
        kinds = []
        n = 0
        while n < 9:
            color = random.choice(Shape.colors)
            kind = random.choice(Shape.forms)
            if kind in kinds:
                continue
            shape = Shape(color=color, form=kind, data=n + 1)
            shapes_dict.append(shape)
            kinds.append(kind)
            n += 1

        shapes_task = []
        for _ in range(2):
            shapes_side = []
            for _ in range(self.num_shapes):
                shape_random = random.choice(shapes_dict)
                shapes_side.append(shape_random)
            shapes_task.append(shapes_side)

        decision = random.choice(["grösser", "kleiner"])
        operation = random.choice(list(self.operators.keys()))
        self._task = shapes_dict, shapes_task, decision, operation

        # Solve task (assuming addition).
        results = [self.operators[operation](shapes_side).data for shapes_side in shapes_task]
        if results[0] == results[1]:
            self._solution = "equal"
        elif (results[0] > results[1]) == (decision == "grösser"):
            self._solution = "left"
        else:
            self._solution = "right"

        # Increment task counter.
        self._counter += 1

        # Start task timer.
        self._timer_start()

    def reset_task(self):
        self._task = None
        self._timer_reset()

    ################################################################################
    # Timer ########################################################################
    ################################################################################
    def _timer_start(self):
        self._timer = time.time()

    def _timer_reset(self):
        self._timer = None

    def time_needed(self) -> float:
        assert self.timer is not None
        return time.time() - self.timer

    ################################################################################
    # Description ##################################################################
    ################################################################################
    def __str__(self) -> str:
        if self.task is None:
            return "None"
        else:
            shapes_dict, shapes_task, dec, op = self.task
            return f"Exercise {self.counter}\n" \
                   f"legend => {shapes_dict}, \ntask => {shapes_task}, \ndescription => {dec}, {op}\n" \
                   f"solution => {self.solution}\n\n"

    ################################################################################
    # Exercise Properties ##########################################################
    ################################################################################
    @property
    def num_shapes(self) -> int:
        return self._num_shapes

    @property
    def task(self) -> typing.Tuple[typing.List[Shape], typing.List[typing.List[Shape]], str, str]:
        return self._task

    @property
    def counter(self) -> int:
        return self._counter

    @property
    def solution(self) -> str:
        return self._solution

    @property
    def timer(self) -> float:
        return self._timer
