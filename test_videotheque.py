from pathlib import Path
from typing import List, Tuple
from unittest.mock import call

from videotheque import rename_files_and_directories


class DummyRenamer:
    def __init__(self) -> None:
        self.moves: List[Tuple[str, str]] = []

    def rename(self, src: str, dest: str):
        self.moves.append((src, dest))


def test_should_rename_one_file_according_to_their_original_names(mocker):
    walk = mocker.patch(
        "videotheque.walk",
        return_value=[
            (
                "/Videos",
                [],
                ["Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4"],
            ),
        ],
    )
    renamer = DummyRenamer()

    rename_files_and_directories(Path("/Videos"), renamer.rename)

    walk.assert_called()
    assert renamer.moves == [
        (
            "/Videos/Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
            "/Videos/Kung_Fu_Panda_2_PORTUGUESE.mp4",
        )
    ]


def test_should_rename_files_and_directories_according_to_their_original_names(mocker):
    walk = mocker.patch(
        "videotheque.walk",
        return_value=[
            (
                "/Videos",
                ["[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME"],
                ["Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4"],
            ),
            (
                "/Videos/[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
                [],
                ["[nextorrent.org] Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi"],
            ),
        ],
    )
    os_rename = mocker.patch("videotheque.rename")

    result = rename_files_and_directories(Path("/Videos"), os_rename)

    walk.assert_called()
    os_rename.assert_called()
    assert result == {
        "dirs": [
            {
                "from": "/Videos/[nextorrent.org] "
                "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
                "to": "/Videos/Train_to_Busan_FRENCH",
            }
        ],
        "files": [
            {
                "from": "/Videos/Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
                "to": "/Videos/Kung_Fu_Panda_2_PORTUGUESE.mp4",
            },
            {
                "from": "/Videos/[nextorrent.org] "
                "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/[nextorrent.org] "
                "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi",
                "to": "/Videos/[nextorrent.org] "
                "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/Train_to_Busan_FRENCH.avi",
            },
        ],
    }
