from pathlib import Path

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
