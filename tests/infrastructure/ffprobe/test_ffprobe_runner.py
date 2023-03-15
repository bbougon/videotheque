from subprocess import CompletedProcess

import pytest

from search.exceptions import RunnerException
from search.runner import VideoDetails
from infrastructure.ffprobe.ffprobe import FFProbeRunner


def test_should_check_errors_on_process_run(mocker):
    with pytest.raises(RunnerException) as exception:
        subprocess = mocker.patch(
            "subprocess.run",
            return_value=CompletedProcess(
                args="args", returncode=1, stderr=b"error occurred"
            ),
        )

        FFProbeRunner().run("the command that will fail")

    subprocess.assert_called_once_with(
        "ffprobe -i the command that will fail -show_entries format=duration -v error -of json -sexagesimal -show_entries stream=index:stream_tags=language -select_streams a",
        stdout=-1,
        stderr=-1,
        shell=True,
    )
    assert exception.value.msg == "Impossible to run the command"
    assert exception.value.details == {
        "args": "args",
        "return_code": 1,
        "stderr": "error occurred",
    }


def test_should_run_ffprobe_and_retrieve_result(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=CompletedProcess(
            args="args",
            returncode=0,
            stdout=b'{"programs": [],"streams": [{"index": 1,"tags": {"language": "fre"}},{"index": 2,"tags": {"language": "eng"}}],"format": {"duration": "1:41:55.136000"}}',
        ),
    )

    result: VideoDetails = FFProbeRunner().run(
        "the command returning meta from ffprobe"
    )

    assert result == VideoDetails(
        languages=["fre", "eng"], duration="1:41:55.136000"
    )


def test_should_run_ffprobe_and_retrieve_result_ignoring_language_case(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=CompletedProcess(
            args="args",
            returncode=0,
            stdout=b'{"programs": [],"streams": [{"index": 1,"tags": {"LANGUAGE": "fre"}},{"index": 2,"tags": {"LANGUAGE": "eng"}}],"format": {"duration": "1:41:55.136000"}}',
        ),
    )

    result: VideoDetails = FFProbeRunner().run(
        "the command returning meta from ffprobe"
    )

    assert result == VideoDetails(
        languages=["fre", "eng"], duration="1:41:55.136000"
    )


def test_should_run_ffprobe_and_retrieve_result_without_language(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=CompletedProcess(
            args="args",
            returncode=0,
            stdout=b'{"programs": [],"streams": [{"index": 1}], "format": {"duration": "1:41:55.136000"}}',
        ),
    )

    result: VideoDetails = FFProbeRunner().run(
        "the command returning meta from ffprobe"
    )

    assert result == VideoDetails(duration="1:41:55.136000")


def test_should_run_ffprobe_and_retrieve_result_without_language_at_all(
    mocker,
):
    mocker.patch(
        "subprocess.run",
        return_value=CompletedProcess(
            args="args",
            returncode=0,
            stdout=b'{"programs": [], "format": {"duration": "1:41:55.136000"}}',
        ),
    )

    result: VideoDetails = FFProbeRunner().run(
        "the command returning meta from ffprobe"
    )

    assert result == VideoDetails(duration="1:41:55.136000")
