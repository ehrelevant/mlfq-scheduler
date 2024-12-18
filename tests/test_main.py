# from io import StringIO
from pytest import CaptureFixture  # , MonkeyPatch

# from src import main
from src.main import (
    MultiLevelFeedbackQueue,
    RRPriorityQueue,
    FCFSPriorityQueue,
    SJFPriorityQueue,
)
from src.main import Process


def generate_mlfq(
    time_allotment_q1: int,
    time_allotment_q2: int,
    context_switch_time: int,
    processes: list[Process],
) -> MultiLevelFeedbackQueue:
    return MultiLevelFeedbackQueue(
        processes,
        [
            RRPriorityQueue(time_allotment_q1),
            FCFSPriorityQueue(time_allotment_q2),
            SJFPriorityQueue(None),
        ],
        context_switch_time,
    )


"""
def test_sample_run(monkeypatch: MonkeyPatch, capfd: CaptureFixture[str]):
    # pass string value to stdin for main.main()
    test_input: str = '\n'.join(
        ['3', '8', '8', '0', 'B;0;5;2;5;2;5', 'A;2;2;2;6', 'C;0;30']
    )
    monkeypatch.setattr('sys.stdin', StringIO(test_input))

    # call main() from /src/main.py
    main.main()

    # capture stdout and stderr outputs from main.main()
    out: str; err: str
    out, err = capfd.readouterr()
    assert out == '\n'.join(
        [
            # todo 1: figure out the actual output for this test case
            # todo 2: maybe create a generic (stdin -> stdout, stderr) callback function
            # todo 3: maybe implement [todo 2] by reading stdin from a .txt file, and comparing outputs with stdout/stderr from other .txt files
            'Processes: [B, A, C]',
            'PriorityQueues: [[], [], []]',
            'Context Switch Time: 0',
            '',
        ]
    )
    assert err == ''
"""


def test_mlfq_instantiation(capfd: CaptureFixture[str]) -> None:
    time_allotment_q1: int = 8
    time_allotment_q2: int = 8
    context_switch_time: int = 0
    processes: list[Process] = [
        Process('B', 0, [5, 2, 5, 2, 5]),
        Process('A', 2, [2, 2, 6]),
        Process('C', 0, [30]),
    ]

    mlfq: MultiLevelFeedbackQueue = generate_mlfq(
        time_allotment_q1, time_allotment_q2, context_switch_time, processes
    )
    print(mlfq)

    # capture stdout and stderr outputs
    out: str
    err: str
    out, err = capfd.readouterr()
    assert out == '\n'.join(
        [
            'Processes: [B, A, C]',
            'PriorityQueues: [[], [], []]',
            'Context Switch Time: 0',
            '',
        ]
    )
    assert err == ''
