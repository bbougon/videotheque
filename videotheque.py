import argparse
import json
import os
from pathlib import Path
from typing import Callable, List

from infrastructure.file_logger import FileSearchLogger
from rename import rename_files_and_directories
from search.search_engine import SearchEngine, SearchResult
from infrastructure.ffprobe.ffprobe import FFProbeRunner
from tests.test_dummy_renamer import DummyRenamer


def rename(
    root_path: Path, file_renamer: Callable[[str, str], None] = os.rename
):
    return rename_files_and_directories.rename(root_path, file_renamer)


def search(
    root_path: Path,
    keywords: List[str],
    search_engine: SearchEngine = SearchEngine(),
) -> SearchResult:
    return search_engine.run(root_path, keywords)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", help="the path where to find your videos", type=Path
    )
    parser.add_argument(
        "command",
        help="the name of the command to execute (<rename> | <search>)",
        type=str,
    )
    parser.add_argument(
        "-k",
        "--keyword",
        help="the search keyword argument (separated with commas)",
        default="",
    )
    args = parser.parse_args()
    if args.command == "rename":
        print(json.dumps(rename(args.path, DummyRenamer().rename), indent=2))
    else:
        search(
            Path(args.path),
            args.keyword.split(","),
            SearchEngine(FFProbeRunner(), FileSearchLogger()),
        ).print()
