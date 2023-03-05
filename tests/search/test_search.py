from os.path import splitext
from pathlib import Path

from conftest import faker
from search.search_engine import SearchEngine, Movie
from tests.dummy_runner import DummyRunner
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


def test_should_escape_spaces_in_filename_or_dir_to_get_video_informations(mocker):
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

    first_video_path = first_video_file.replace(" ", "\ ")
    second_video_path = second_video_file.replace(" ", "\ ")
    assert runner.arguments == [
        f"-i /Videos/Dir\ with\ spaces/{first_video_path} -show_entries format=duration -v quiet -of csv='p=0' -sexagesimal",
        f"-i /Videos/Dir\ with\ spaces/{second_video_path} -show_entries format=duration -v quiet -of csv='p=0' -sexagesimal",
    ]
