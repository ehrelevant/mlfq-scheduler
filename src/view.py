# todo: imports
from project_types import ( 
    MultiLevelFeedbackQueue
)

class MLFQView:
    # no need for any initial values (for now)
    def __init__(self):
        pass

    # Request the following in order: num_processes, time_allotment_q1, time_allotment_q2, context_switch_time
    def request_scheduler_details(self) -> tuple[int, int, int, int]:
        print("# Enter Scheduler Details #")
        return (int(input()), int(input()), int(input()), int(input()))

    # Request process details given the num_processes from previous input
    def request_process_details(self, num: int) -> list[str]: 
        print(f"# Enter {num} Process Details #")
        return [input() for _ in range(num)]

    # Do smth after every tick (i.e. after 1 second)
    '''
    def on_tick(self):
        ...
    '''

    #temporary
    def output(self, mlfq: MultiLevelFeedbackQueue):
        print(mlfq)