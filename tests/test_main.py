from io import StringIO
from pytest import CaptureFixture, MonkeyPatch
from src import main


def test_sample_run(monkeypatch: MonkeyPatch, capfd: CaptureFixture[str]):
    # pass string value to stdin for main.main()
    test_input: str = '\n'.join(
        ['3', '8', '8', '0', 'B;0;5;2;5;2;5', 'A;2;2;2;6', 'C;0;30']
    )
    monkeypatch.setattr('sys.stdin', StringIO(test_input))

    # call main() from /src/main.py
    main.main()

    # capture stdout and stderr outputs from main.main()
    out, err = capfd.readouterr()
    assert out == '\n'.join(
        [
            # todo 1: figure out the actual output for this test case
            # todo 2: maybe create a generic (stdin -> stdout, stderr) callback function
            # todo 3: maybe implement [todo 2] by reading stdin from a .txt file, and comparing outputs with stdout/stderr from other .txt files
            # aside: added view checks for now to appease pytest
            '# Enter Scheduler Details #',
            '# Enter 3 Process Details #',
            'Processes: [B, A, C]',
            'PriorityQueues: [[], [], []]',
            'Context Switch Time: 0',
            '',
        ]
    )
    assert err == ''
