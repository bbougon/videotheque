from pathlib import Path

from search.search_engine import SearchEngine, Movie
from tests.fake import DummyRunner
from tests.test_dummy_renamer import DummyRenamer
from videotheque import rename, search


def test_should_rename_one_file_according_to_their_original_names(mocker):
    walk = mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [],
                ["Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4"],
            ),
        ],
    )
    renamer = DummyRenamer()

    rename(Path("/Videos"), renamer.rename)

    walk.assert_called()
    assert renamer.moves == [
        (
            "/Videos/Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
            "/Videos/Kung_Fu_Panda_2_PORTUGUESE.mp4",
        )
    ]


def test_should_search(mocker):
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [
                    "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME"
                ],
                ["Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4"],
            ),
            (
                "/Videos/[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
                [],
                [
                    "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi"
                ],
            ),
        ],
    )
    runner = DummyRunner()

    result = search(Path("/Videos"), [], SearchEngine(runner))

    assert result.movies == [
        Movie(
            "Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD",
            "01:30:09.36",
            ["Portuguese"],
        ),
        Movie(
            "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
            "01:30:09.36",
            ["French"],
        ),
    ]
    assert runner.arguments == [
        "/Videos/Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
        "/Videos/[nextorrent.org]\\ Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/[nextorrent.org]\\ Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi",
    ]


def test_should_search_with_keywords(mocker):
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [
                    "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME"
                ],
                ["Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4"],
            ),
            (
                "/Videos/[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
                [],
                [
                    "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi"
                ],
            ),
        ],
    )
    runner = DummyRunner()

    result = search(Path("/Videos"), ["Train"], SearchEngine(runner))

    assert result.movies == [
        Movie(
            "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
            "01:30:09.36",
            ["French"],
        ),
    ]
    assert runner.arguments == [
        "/Videos/[nextorrent.org]\\ Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/[nextorrent.org]\\ Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi",
    ]


def test_should_search_with_keywords_ignoring_case(mocker):
    mocker.patch(
        "os.walk",
        return_value=[
            (
                "/Videos",
                [
                    "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME"
                ],
                ["Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4"],
            ),
            (
                "/Videos/[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
                [],
                [
                    "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi"
                ],
            ),
        ],
    )
    runner = DummyRunner()

    result = search(Path("/Videos"), ["train"], SearchEngine(runner))

    assert result.movies == [
        Movie(
            "[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
            "01:30:09.36",
            ["French"],
        ),
    ]
    assert runner.arguments == [
        "/Videos/[nextorrent.org]\\ Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/[nextorrent.org]\\ Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi",
    ]
