from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol


class PriorityQueue(Protocol):
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    @property
    def num_processes(self) -> int: ...

    def on_tick(self): ...


class RRPriorityQueue:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    _time_quantum: int

    def __init__(self, time_allotment: int | None, time_quantum: int = 4) -> None:
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


class FCFSPriorityQueue:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    def __init__(self, time_allotment: int | None) -> None:
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


class SJFPriorityQueue:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    def __init__(self, time_allotment: int | None) -> None:
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


class MultiLevelFeedbackQueue:
    _processes: Sequence[Process]
    _priority_queues: Sequence[PriorityQueue]
    _context_switch_time: int

    def __init__(
        self,
        processes: Sequence[Process],
        priority_queues: Sequence[PriorityQueue],
        context_switch_time: int = 0,
    ) -> None:
        self._processes = processes
        self._priority_queues = priority_queues
        self._context_switch_time = context_switch_time

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"Processes: {self._processes}",
                f"PriorityQueues: {self._priority_queues}",
                f"Context Switch Time: {self._context_switch_time}",
            ]
        )

    def on_tick(self):
        pass

    def run(self):
        pass


# ---


def main() -> None:
    num_processes: int = int(input())
    time_allotment_q1: int = int(input())
    time_allotment_q2: int = int(input())
    context_switch_time: int = int(input())

    processes: list[Process] = []
    for _ in range(num_processes):
        [process_name, *process_details] = input().split()
        [arrival_time, *burst_times] = map(int, process_details)
        processes.append(Process(process_name, arrival_time, burst_times))

    priority_queues: list[PriorityQueue] = [
        RRPriorityQueue(time_allotment_q1),
        FCFSPriorityQueue(time_allotment_q2),
        SJFPriorityQueue(None),
    ]

    mlfq: MultiLevelFeedbackQueue = MultiLevelFeedbackQueue(
        processes, priority_queues, context_switch_time
    )

    print(mlfq)


if __name__ == "__main__":
    main()
