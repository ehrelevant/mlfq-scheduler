from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol, Tuple


class PriorityQueue(Protocol):
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    @property
    def num_processes(self) -> int: ...

    def on_tick(self): ...

    def push_process(self, process: Process): ...


class RRPriorityQueue:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    _time_quantum: int

    def __init__(
        self, time_allotment: int | None = None, time_quantum: int = 4
    ) -> None:
        self._time_allotment = time_allotment
        self._processes = []
        self._current_process_index = 0

        self._time_quantum = time_quantum

    def __repr__(self) -> str:
        return str(self._processes)

    def __str__(self) -> str:
        return str(self._processes)

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    def on_tick(self):
        pass

    def push_process(self, process: Process):
        self._processes.append(process)


class FCFSPriorityQueue:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    def __init__(self, time_allotment: int | None = None) -> None:
        self._time_allotment = time_allotment

        self._processes = []
        self._current_process_index = 0

    def __repr__(self) -> str:
        return str(self._processes)

    def __str__(self) -> str:
        return str(self._processes)

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    def on_tick(self):
        pass

    def push_process(self, process: Process):
        self._processes.append(process)


class SJFPriorityQueue:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    def __init__(self, time_allotment: int | None = None) -> None:
        self._time_allotment = time_allotment

        self._processes = []
        self._current_process_index = 0

    def __repr__(self) -> str:
        return str(self._processes)

    def __str__(self) -> str:
        return str(self._processes)

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    def on_tick(self):
        pass

    def push_process(self, process: Process):
        self._processes.append(process)


class Process:
    _process_name: str
    _arrival_time: int
    _burst_times: list[int]

    def __init__(
        self, process_name: str, arrival_time: int, burst_times: list[int]
    ) -> None:
        self._process_name = process_name
        self._arrival_time = arrival_time
        self._burst_times = burst_times

    def __repr__(self) -> str:
        return self._process_name

    def __str__(self) -> str:
        return self._process_name

    @property
    def process_name(self) -> str:
        return self._process_name

    @property
    def arrival_time(self) -> int:
        return self._arrival_time


class MultiLevelFeedbackQueue:
    _tick: int = 0
    _future_processes: Sequence[Process]
    _priority_queues: Sequence[PriorityQueue]
    _context_switch_time: int

    def __init__(
        self,
        future_processes: Sequence[Process],
        priority_queues: Sequence[PriorityQueue],
        context_switch_time: int = 0,
    ) -> None:
        self._future_processes = future_processes
        self._priority_queues = priority_queues
        self._context_switch_time = context_switch_time

    def __repr__(self) -> str:
        return '\n'.join(
            [
                f'Processes: {self._future_processes}',
                f'PriorityQueues: {self._priority_queues}',
                f'Context Switch Time: {self._context_switch_time}',
            ]
        )

    def on_tick(self):
        newly_arrived_processes = sorted(
            filter(lambda p: p.arrival_time == self._tick, self._future_processes),
            key=lambda p: p.process_name,
        )

        if newly_arrived_processes:
            print(f'New processes (t = {self._tick}): {newly_arrived_processes}')

            for process in newly_arrived_processes:
                self._priority_queues[0].push_process(process)

        self._tick += 1

    def run(self):
        for _ in range(10):
            self.on_tick()


# ---


def get_user_input() -> Tuple[int, int, int, list[Process]]:
    num_processes: int = int(input())
    time_allotment_q1: int = int(input())
    time_allotment_q2: int = int(input())
    context_switch_time: int = int(input())

    processes: list[Process] = []
    for _ in range(num_processes):
        [process_name, *process_details] = input().split(';')
        [arrival_time, *burst_times] = map(int, process_details)
        processes.append(Process(process_name, arrival_time, burst_times))

    return time_allotment_q1, time_allotment_q2, context_switch_time, processes


def get_fake_input() -> Tuple[int, int, int, list[Process]]:
    # I gave up on making tests
    time_allotment_q1: int = 8
    time_allotment_q2: int = 8
    context_switch_time: int = 0
    processes: list[Process] = [
        Process('B', 0, [5, 2, 5, 2, 5]),
        Process('A', 2, [2, 2, 6]),
        Process('C', 0, [30]),
    ]

    return time_allotment_q1, time_allotment_q2, context_switch_time, processes


def main() -> None:
    time_allotment_q1, time_allotment_q2, context_switch_time, processes = (
        get_fake_input()
    )

    priority_queues: list[PriorityQueue] = [
        RRPriorityQueue(time_allotment_q1),
        FCFSPriorityQueue(time_allotment_q2),
        SJFPriorityQueue(None),
    ]

    mlfq: MultiLevelFeedbackQueue = MultiLevelFeedbackQueue(
        processes, priority_queues, context_switch_time
    )

    print(mlfq)

    mlfq.run()


if __name__ == '__main__':
    main()
