from io import StringIO
from pytest import CaptureFixture, MonkeyPatch
from pathlib import Path

from src import main
from src.main import (
    MultiLevelFeedbackQueue,
    RRPriorityQueue,
    FCFSPriorityQueue,
    SJFPriorityQueue,
)
from src.main import Process

# note that pytest is called from the root directory, not from /tests
INPUTS_PATH: Path = Path.cwd() / 'tests' / 'input'
OUTPUTS_PATH: Path = Path.cwd() / 'tests' / 'output'


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


def test_main(monkeypatch: MonkeyPatch, capfd: CaptureFixture[str]) -> None:
    input_files: list[Path] = [f for f in INPUTS_PATH.iterdir() if f.is_file()]
    output_files: list[Path] = [f for f in OUTPUTS_PATH.iterdir() if f.is_file()]

    for input_file, output_file in zip(input_files, output_files):
        test_input: str = open(input_file, 'r').read()
        monkeypatch.setattr('sys.stdin', StringIO(test_input))

        # call main() from /src/main.py
        main.main()

        # capture stdout and stderr outputs from main.main()
        out: str
        err: str
        out, err = capfd.readouterr()
        assert out.strip() == open(output_file, 'r').read().strip()
        assert err == ''


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
