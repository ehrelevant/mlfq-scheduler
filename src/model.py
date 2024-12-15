from project_types import ( 
    Process, 
    PriorityQueue, RRPriorityQueue, FCFSPriorityQueue, SJFPriorityQueue, 
    MultiLevelFeedbackQueue
)

class MLFQModel:
    # initialize variables (and lists are currently empty)
    _num_processes: int
    _time_allotment_q1: int
    _time_allotment_q2: int
    _context_switch_time: int
    _processes: list[Process]
    _priority_queues: list[PriorityQueue]
    _mlfq: MultiLevelFeedbackQueue

    def __init__(self):
        self._processes = []
        self._priority_queues = []

    # obtain scheduler details from view.py
    def implement_scheduler_details(self, sched_deets: tuple[int, int, int, int]):
        self._num_processes = sched_deets[0]
        self._time_allotment_q1 = sched_deets[1]
        self._time_allotment_q2 = sched_deets[2]
        self._context_switch_time = sched_deets[3]

    # obtain process details from view.py
    def implement_process_details(self, proc_deets: list[str]):
        for process in proc_deets:
            [process_name, *process_details] = process.split(';')
            [arrival_time, *burst_times] = map(int, process_details)
            self._processes.append(Process(process_name, arrival_time, burst_times))

    # self-explanatory
    def setup_priority_queues(self):
        self._priority_queues = [
            RRPriorityQueue(self._time_allotment_q1),
            FCFSPriorityQueue(self._time_allotment_q2),
            SJFPriorityQueue(None),
        ]
    
    # self-explanatory
    def setup_mlfq(self):
        self._mlfq: MultiLevelFeedbackQueue = MultiLevelFeedbackQueue(
            self._processes, self._priority_queues, self._context_switch_time
        )

    # PROPERTIES - for outside class usage
    @property
    def num_processes(self) -> int:
        return self._num_processes
    
    @property
    def mlfq(self) -> MultiLevelFeedbackQueue:
        return self._mlfq

    