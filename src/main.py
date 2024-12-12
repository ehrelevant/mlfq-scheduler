from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol


class Scheduler(Protocol):
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    @property
    def num_processes(self) -> int: ...

    def on_tick(self): ...


class RRScheduler:
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
        return f'[{', '.join(map(str, self._processes))}]'

    def __str__(self) -> str:
        return f'[{', '.join(map(str, self._processes))}]'

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    def on_tick(self) -> None:
        pass


class FCFSScheduler:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    def __init__(self, time_allotment: int | None) -> None:
        self._time_allotment = time_allotment

        self._processes = []
        self._current_process_index = 0

    def __repr__(self) -> str:
        return f'[{', '.join(map(str, self._processes))}]'

    def __str__(self) -> str:
        return f'[{', '.join(map(str, self._processes))}]'

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    def on_tick(self) -> None:
        pass


class SJFScheduler:
    _time_allotment: int | None
    _processes: list[Process]
    _current_process_index: int

    def __init__(self, time_allotment: int | None) -> None:
        self._time_allotment = time_allotment

        self._processes = []
        self._current_process_index = 0

    def __repr__(self) -> str:
        return f'[{', '.join(map(str, self._processes))}]'

    def __str__(self) -> str:
        return f'[{', '.join(map(str, self._processes))}]'

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    def on_tick(self) -> None:
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
    _schedulers: Sequence[Scheduler]
    _context_switch_time: int

    def __init__(
        self,
        processes: Sequence[Process],
        schedulers: Sequence[Scheduler],
        context_switch_time: int = 0,
    ) -> None:
        self._processes = processes
        self._schedulers = schedulers
        self._context_switch_time = context_switch_time

    def __repr__(self) -> str:
        # todo: find a better way to format this multiline f-string
        return f"""
Processes: {self._processes}
Schedulers: {self._schedulers}
Context Switch Time: {self._context_switch_time}
            """.strip()

    def on_tick(self) -> None:
        pass


# ---


def main() -> None:
    num_processes: int = int(input())
    time_allotment_q1: int = int(input())
    time_allotment_q2: int = int(input())
    context_switch_time: int = int(input())

    processes: list[Process] = []
    for _ in range(num_processes):
        process_raw: list[str] = input().split(";")
        processes.append(
            Process(
                process_raw[0], int(process_raw[1]), list(map(int, process_raw[2:]))
            )
        )

    schedulers: list[Scheduler] = [
        RRScheduler(time_allotment_q1),
        FCFSScheduler(time_allotment_q2),
        SJFScheduler(None),
    ]

    mlfq: MultiLevelFeedbackQueue = MultiLevelFeedbackQueue(
        processes, schedulers, context_switch_time
    )

    print(mlfq)


if __name__ == "__main__":
    main()
