from os.path import splitext
from pathlib import Path

from immobilus import immobilus

from conftest import faker
from search.search_engine import SearchEngine, Movie
from tests.fake import DummyRunner, MemoryLogger
from videotheque import search


def test_should_search_avoiding_hidden_files(mocker):
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [],
                [
                    "Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
                    ".hidden_file",
                ],
            ),
        ],
    )

    result = search(Path("/Videos"), [], SearchEngine(DummyRunner()))

    assert result.movies == [
        Movie(
            "Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD",
            "01:30:09.36",
            ["Portuguese"],
        ),
    ]


def test_should_search_for_only_video_files(mocker):
    first_video_file = faker.custom_file_name()
    second_file = faker.custom_file_name(category="text")
    third_video_file = faker.custom_file_name()
    fourth_file = faker.custom_file_name(category="image")
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [],
                [first_video_file, second_file, third_video_file, fourth_file],
            ),
        ],
    )

    result = SearchEngine(DummyRunner()).run(Path("/Videos"), [])

    first_video_title, _ = splitext(first_video_file)
    third_video_title, _ = splitext(third_video_file)
    assert result.movies == [
        Movie(
            first_video_title,
            "01:30:09.36",
            [],
        ),
        Movie(
            third_video_title,
            "01:30:09.36",
            [],
        ),
    ]


def test_should_escape_spaces_in_filename_or_dir_to_get_video_informations(
    mocker,
):
    first_video_file: str = faker.custom_file_name()
    second_video_file: str = faker.custom_file_name()
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos/Dir with spaces",
                [],
                [first_video_file, second_video_file],
            ),
        ],
    )
    runner = DummyRunner()

    SearchEngine(runner).run(Path("/Videos"), [])

    first_video_path = first_video_file.replace(" ", "\\ ")
    second_video_path = second_video_file.replace(" ", "\\ ")
    assert runner.arguments == [
        f"/Videos/Dir\\ with\\ spaces/{first_video_path}",
        f"/Videos/Dir\\ with\\ spaces/{second_video_path}",
    ]


@immobilus("2020-04-03 10:24:15.230")
def test_should_explain_why_duration_was_not_found(mocker):
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos/Dir with spaces",
                [],
                ["my_video_for_which_duration_fails.avi"],
            ),
        ],
    )
    runner = DummyRunner(raise_exception=True)
    logger = MemoryLogger()

    result = SearchEngine(runner, logger).run(Path("/Videos"), [])

    assert result.movies[0] == Movie(
        "my_video_for_which_duration_fails",
        "unable to get duration (see error log file)",
        [],
    )
    assert logger.content == {
        "datetime": "2020-04-03T10:24:15.230000",
        "command": "ffprobe",
        "args": "no args",
        "return_code": -1,
        "stderr": "An error",
    }


def test_should_search_with_various_keywords(mocker):
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [],
                [
                    "Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
                    "Kung.Fu.Panda.3.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
                ],
            ),
        ],
    )

    result = search(
        Path("/Videos"), ["kung", "fu", "3"], SearchEngine(DummyRunner())
    )

    assert result.movies == [
        Movie(
            "Kung.Fu.Panda.3.2011.PORTUGUESE.720p.BDRiP.x264-nTHD",
            "01:30:09.36",
            ["Portuguese"],
        ),
    ]
