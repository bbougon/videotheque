from subprocess import CompletedProcess

import pytest

from search.exceptions import RunnerException
from search.search_engine import FFProbeRunner


def test_should_check_errors_on_process_run(mocker):
    with pytest.raises(RunnerException) as exception:
        mocker.patch(
            "subprocess.run",
            return_value=CompletedProcess(
                args="args", returncode=1, stderr=b"error occurred"
            ),
        )

        FFProbeRunner().run("the command that will fail")

    assert exception.value.msg == "Impossible to run the command"
    assert exception.value.details == {
        "args": "args",
        "return_code": 1,
        "stderr": "error occurred",
    }
