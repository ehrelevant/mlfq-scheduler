from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol


class Process:
    _process_name: str
    _arrival_time: int
    _burst_times: list[int]
    _burst_index: int
    _queue_level: int
    _time_in_queue: int

    def __init__(
        self, process_name: str, arrival_time: int, burst_times: list[int]
    ) -> None:
        self._process_name = process_name
        self._arrival_time = arrival_time
        self._burst_times = burst_times

        self._burst_index = 0
        self._queue_level = 0
        self._time_in_queue = 0

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

    @property
    def queue_level(self) -> int:
        return self._queue_level

    @property
    def time_in_queue(self) -> int:
        return self._time_in_queue

    @property
    def remaining_current_burst(self):
        return self._burst_times[self._burst_index]

    @property
    def is_CPU_burst(self) -> bool:
        return bool(self._burst_index % 2 == 0)
    
    def on_tick(self) -> None:
        '''
        Updates the process burst time and time in queue
        '''
        self._time_in_queue += 1
        self._burst_times[self._burst_index] -= 1

    @property
    def next_burst(self) -> None:
        '''
        Updates the pointer to what burst (IO or CPU) should be running
        '''
        self._burst_index += 1

    @property
    def is_burst_complete(self) -> bool:
        return self._burst_times[self._burst_index] <= 0

    @property
    def is_process_complete(self) -> bool:
        return all(burst <= 0 for burst in self._burst_times)

    def is_within_allotment(self, time_allotment: int) -> bool:
        return self._time_in_queue < time_allotment

    def demote(self):
        '''
        Demotes the process to a lower queue
        '''
        self._queue_level += 1
        self._time_in_queue = 0


class PriorityQueue(Protocol):
    _time_allotment: int | None
    _processes: list[Process]

    @property
    def num_processes(self) -> int: ...

    @property
    def processes(self) -> list[Process]: ...

    @property
    def is_empty(self) -> bool: ...
    
    def on_tick(self):
        '''
        Reduce quantum count and run process
        '''
        ...

    def push_process(self, process: Process):
        ...

    # Only one process can be released (current)
    # We define expired processes as processes that have either completed a burst
    # or have used their entire time allocation for a priority queue
    def release_current_on_expiry(self) -> Process | None: 
        '''
        Release process when quantum is used up
        '''
        ...

    def select_new_process(self) -> Process | None: 
        '''
        Select new process to run
        '''
        ...

class RRPriorityQueue(PriorityQueue):
    _time_allotment: int | None
    _processes: list[Process] = []

    _time_quantum: int
    _time_quantum_counter: int = 0

    def __init__(
        self, time_allotment: int | None = None, time_quantum: int = 4
    ) -> None:
        self._time_allotment = time_allotment
        self._time_quantum = time_quantum
        self._time_quantum_counter = self._time_quantum

    def __repr__(self) -> str:
        return str(self._processes)

    def __str__(self) -> str:
        return str(self._processes)

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    @property
    def processes(self) -> list[Process]:
        return self._processes

    @property
    def is_empty(self) -> bool:
        return len(self._processes) == 0

    def on_tick(self):
        if self.is_empty:
            return

        self._time_quantum_counter -= 1
        self._processes[0].on_tick()

    def push_process(self, process: Process):
        self._processes.append(process)

    def release_current_on_expiry(self) -> Process | None:
        if self.is_empty:
            return

        current_process = self._processes[0]
        if current_process.is_burst_complete or (
            self._time_allotment
            and not current_process.is_within_allotment(self._time_allotment)
        ):
            self._time_quantum_counter = self._time_quantum
            return self._processes.pop(0)

    def select_new_process(self) -> Process | None:
        if self.is_empty:
            return

        if self._time_quantum_counter <= 0:
            old_process = self._processes.pop(0)
            self.push_process(old_process)
            self._time_quantum_counter = self._time_quantum

        return self._processes[0]

class FCFSPriorityQueue(PriorityQueue):
    _time_allotment: int | None
    _processes: list[Process] = []

    def __init__(self, time_allotment: int | None = None) -> None:
        self._time_allotment = time_allotment

    def __repr__(self) -> str:
        return str(self._processes)

    def __str__(self) -> str:
        return str(self._processes)

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    @property
    def processes(self) -> list[Process]:
        return self._processes
    
    @property
    def is_empty(self) -> bool:
        return len(self._processes) == 0

    def on_tick(self):
        if self.is_empty:
            return

        self._processes[0].on_tick()

    def push_process(self, process: Process):
        self._processes.append(process)

    def release_current_on_expiry(self) -> Process | None:
        if self.is_empty:
            return

        current_process = self._processes[0]
        if current_process.is_burst_complete or (
            self._time_allotment
            and not current_process.is_within_allotment(self._time_allotment)
        ):
            return self._processes.pop(0)

    def select_new_process(self) -> Process | None:
        if self.is_empty:
            return

        return self._processes[0]

class SJFPriorityQueue(PriorityQueue):
    _time_allotment: int | None
    _processes: list[Process] = []
    _current_process_index: int = 0

    def __init__(self, time_allotment: int | None = None) -> None:
        self._time_allotment = time_allotment

    def __repr__(self) -> str:
        return str(self._processes)

    def __str__(self) -> str:
        return str(self._processes)

    @property
    def num_processes(self) -> int:
        return len(self._processes)

    @property
    def processes(self) -> list[Process]:
        return self._processes
    
    @property
    def is_empty(self) -> bool:
        return len(self._processes) == 0

    def on_tick(self):
        if self.is_empty:
            return

        self._processes[self._current_process_index].on_tick()

    def push_process(self, process: Process):
        self._processes.append(process)

    def release_current_on_expiry(self) -> Process | None:
        if self.is_empty:
            return

        current_process = self._processes[self._current_process_index]
        if current_process.is_burst_complete or (
            self._time_allotment
            and not current_process.is_within_allotment(self._time_allotment)
        ):
            return self._processes.pop(self._current_process_index)

    def select_new_process(self) -> Process | None:
        if self.is_empty:
            return

        self._current_process_index = min(
            range(len(self._processes)),
            key=lambda i: self._processes[i].remaining_current_burst,
        )
        return self._processes[self._current_process_index]

class IO:
    _processes: list[Process]

    def __init__(self) -> None:
        self._processes = []

    def __repr__(self) -> str:
        return str(self._processes)
    
    def __str__(self) -> str:
        return str(self._processes)

    @property
    def is_empty(self) -> bool:
        return len(self._processes) == 0
    
    def on_tick(self):
        for process in self._processes:
            process.on_tick()

    def push_process(self, process: Process):
        self._processes.append(process)

    def release_expired_processes(self) -> list[Process]:
        '''
        Release processes from IO once burst time is used up
        '''
        expired_processes: list[Process] = [
            process for process in self._processes if process.is_burst_complete
        ]

        # Removes expired processes from IO
        for process in expired_processes:
            self._processes.remove(process)

        return expired_processes

class MultiLevelFeedbackQueue:
    _tick: int = 0
    _future_processes: list[Process]
    _priority_queues: Sequence[PriorityQueue]
    _io: IO
    _context_switch_time: int
    _context_switch_counter: int = 0
    _last_running_process: Process | None = None
    _current_process: Process | None = None

    def __init__(
        self,
        future_processes: Sequence[Process],
        priority_queues: Sequence[PriorityQueue],
        context_switch_time: int = 0,
    ) -> None:
        self._future_processes = list(future_processes)
        self._priority_queues = priority_queues
        self._context_switch_time = context_switch_time
        self._io = IO()

    def __repr__(self) -> str:
        return '\n'.join(
            [
                f'Processes: {self._future_processes}',
                f'PriorityQueues: {self._priority_queues}',
                f'Context Switch Time: {self._context_switch_time}',
            ]
        )

    @property
    def is_empty(self):
        return all(
            [queue.is_empty for queue in self._priority_queues]
            + [len(self._future_processes) == 0]
            + [self._io.is_empty]
        )

    def on_tick(self):
        '''
        Run both IO and CPU Ticks
        '''
        self._tick += 1

        # IO Tick
        self._io.on_tick()

        # CPU Tick (if not currently context switching)
        if self._context_switch_counter > 0:
            self._context_switch_counter -= 1
            return

        for queue in self._priority_queues:
            if not queue.is_empty:
                queue.on_tick()
                break

    def push_arriving_processes(self):
        '''
        Push all processes arriving during the tick
        '''
        newly_arrived_processes = sorted(
            [
                process
                for process in self._future_processes
                if process.arrival_time == self._tick
            ],
            key=lambda p: p.process_name,
        )

        # Removes newly arrived processes from future processes list
        for process in newly_arrived_processes:
            self._future_processes.remove(process)

        if newly_arrived_processes:
            print(f'Arriving : {newly_arrived_processes}')

            for process in newly_arrived_processes:
                self._priority_queues[0].push_process(process)

    def reschedule_expired_processes(self):
        '''
        Reassign complete, demoted and requeue processes on Queues (either IO, Q1, Q2, or Q3)
        '''
        completed_processes: list[Process] = []
        burst_completed_processes: list[Process] = []
        demoted_processes: list[Process] = []

        # Check all priority queues and sort into three separate lists
        for queue in self._priority_queues:
            process = queue.release_current_on_expiry()
            if process:
                if process.is_process_complete:
                    completed_processes.append(process)
                elif process.is_burst_complete:
                    burst_completed_processes.append(process)
                else:
                    demoted_processes.append(process)

        # Check IO and release finished IO processes
        io_completed_processes = self._io.release_expired_processes()
        for process in io_completed_processes:
            if not process.is_process_complete:
                burst_completed_processes.append(process)

        # Sorting alphabetically
        completed_processes.sort(key=lambda p: p.process_name)
        burst_completed_processes.sort(key=lambda p: p.process_name)
        demoted_processes.sort(key=lambda p: p.process_name)

        # Output all finished processes (i.e. all burst times are now 0)
        for process in completed_processes:
            print(f'{process.process_name} DONE')

        # Reassign demoted processes
        for process in demoted_processes:
            print(f'{process.process_name} DEMOTED')
            process.demote()
            self._priority_queues[process.queue_level].push_process(process)

        # Reassign based on IO or CPU burst completion
        for process in burst_completed_processes:
            process.next_burst

            if process.is_CPU_burst:
                self._priority_queues[process.queue_level].push_process(process)
            else:
                self._io.push_process(process)

    def context_switch(self):
        # ASSUMPTIONS:
        # - Context switch cannot be interrupted if already ongoing
        #   - If a higher priority process enters mid-switch, it will have to wait to do a context switch
        # - All priority queues are pre-emptive

        if self._context_switch_counter > 0:
            return

        next_process: Process | None = None

        for queue in self._priority_queues:
            if not queue.is_empty:
                next_process = queue.select_new_process()
                break

        if next_process and self._last_running_process != next_process:
            self._last_running_process = next_process
            self._current_process = None
            self._context_switch_counter = self._context_switch_time

        if self._context_switch_counter <= 0:
            self._current_process = next_process

    def run(self):
        '''
        Run the MLFQ simulation.
        Note that the context switch runs first *when the program is simulated*.
        '''
        self.context_switch()
        while not self.is_empty:
            print(f'At Time = {self._tick}')
            self.push_arriving_processes()
            self.reschedule_expired_processes()
            self.context_switch()
            self.on_tick()

            # Has to be done this way to remove the current process
            queue_processes_list = [queue.processes for queue in self._priority_queues]
            queues_waiting_processes = [
                list(filter(lambda p: p != self._current_process, processes))
                for processes in queue_processes_list
            ]
            print(f'Queues : { ";".join(map(str, queues_waiting_processes)) }')

            if self._current_process:
                print(f'CPU : {self._current_process}')
            else:
                print('CPU : []')

            if not self._io.is_empty:
                print(f'IO : {self._io}')

            print()


# ---


def get_user_input() -> tuple[int, int, int, list[Process]]:
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


def get_fake_input() -> tuple[int, int, int, list[Process]]:
    # I gave up on making tests
    time_allotment_q1: int = 8
    time_allotment_q2: int = 8
    context_switch_time: int = 0
    processes: list[Process] = [
        Process('B', 0, [5, 2, 5, 2, 5]),
        Process('A', 2, [2, 2]),
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
