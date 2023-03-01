from pathlib import Path

from test_dummy_renamer import DummyRenamer
from videotheque import rename_files_and_directories


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
    renamer = DummyRenamer()

    result = rename_files_and_directories(Path("/Videos"), renamer.rename)

    walk.assert_called()
    assert renamer.moves == [
        (
            "/Videos/Kung.Fu.Panda.2.2011.PORTUGUESE.720p.BDRiP.x264-nTHD.mp4",
            "/Videos/Kung_Fu_Panda_2_PORTUGUESE.mp4",
        ),
        (
            "/Videos/[nextorrent.org] "
            "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/[nextorrent.org] "
            "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME.avi",
            "/Videos/[nextorrent.org] "
            "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME/Train_to_Busan_FRENCH.avi",
        ),
        (
            "/Videos/[nextorrent.org] " "Train.to.Busan.2016.FRENCH.BDRip.XviD-EXTREME",
            "/Videos/Train_to_Busan_FRENCH",
        ),
    ]
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


def test_should_rename_files_containing_year_in_parentheses(mocker):
    walk = mocker.patch(
        "videotheque.walk",
        return_value=[
            (
                "/Videos",
                [],
                [
                    "Asterix E Il Regno Degli Dei (2014).ita.fre.sub.ita.eng.MIRCrew.mkv",
                    "Overlord (2018) [WEBRip] [720p] [YTS.AM].avi",
                ],
            ),
        ],
    )
    renamer = DummyRenamer()

    rename_files_and_directories(Path("/Videos"), renamer.rename)

    walk.assert_called()
    assert renamer.moves == [
        (
            "/Videos/Asterix E Il Regno Degli Dei (2014).ita.fre.sub.ita.eng.MIRCrew.mkv",
            "/Videos/Asterix_E_Il_Regno_Degli_Dei_FRENCH_ENGLISH.mkv",
        ),
        (
            "/Videos/Overlord (2018) [WEBRip] [720p] [YTS.AM].avi",
            "/Videos/Overlord.avi",
        ),
    ]


def test_should_not_rename_files_or_dir_if_already_well_formatted(mocker):
    walk = mocker.patch(
        "videotheque.walk",
        return_value=[
            (
                "/Videos",
                ["Asterix_E_Il_Regno_Degli_Dei_FRENCH_ENGLISH"],
                ["Asterix_E_Il_Regno_Degli_Dei_FRENCH_ENGLISH.mkv"],
            ),
        ],
    )
    renamer = DummyRenamer()

    rename_files_and_directories(Path("/Videos"), renamer.rename)

    assert renamer.moves == []


def test_should_not_rename_files_or_dirs_starting_with_a_dot(mocker):
    walk = mocker.patch(
        "videotheque.walk",
        return_value=[
            (
                "/Videos",
                [".hidden_dir"],
                [".hidden_file"],
            ),
        ],
    )
    renamer = DummyRenamer()

    rename_files_and_directories(Path("/Videos"), renamer.rename)

    assert renamer.moves == []
