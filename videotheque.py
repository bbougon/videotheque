import argparse
import json
import re
from os import walk, rename, path
from pathlib import Path
from typing import Callable, List

from languages import extract_languages_from_name
from search_engine import SearchEngine, SearchResult
from test_dummy_renamer import DummyRenamer

_USELESS_INFOS_REGEX = re.compile(
    r"(\[.*])|([0-9]{4}).*|([0-9]{3,4}p.*)|(x[0-9]{3}.*)|(bdrip).*|(brrip).*|(hdrip).*",
    re.IGNORECASE,
)


def rename_files_and_directories(
    root_path: Path, file_renamer: Callable[[str, str], None] = rename
):
    renamed_files_and_dirs = {"files": [], "dirs": []}
    for root, _, files in walk(root_path):
        for name in files:
            new_file_name = _forge_new_name(*(path.splitext(Path(name))))
            if new_file_name != name:
                to_rename, new_name = _rename(
                    root,
                    name,
                    new_file_name,
                    file_renamer,
                )
                renamed_files_and_dirs["files"].append(
                    {"from": to_rename, "to": new_name}
                )

    for root, dirs, _ in walk(root_path):
        for dir in dirs:
            new_dir_name = _forge_new_name(dir)
            if new_dir_name != dir:
                to_rename, new_name = _rename(
                    root,
                    dir,
                    new_dir_name,
                    file_renamer,
                )
                renamed_files_and_dirs["dirs"].append(
                    {"from": to_rename, "to": new_name}
                )
    return renamed_files_and_dirs


def search(
    root_path: Path, keywords: List[str], search_engine: SearchEngine = SearchEngine()
) -> SearchResult:
    return search_engine.run(root_path, keywords)


def _forge_new_name(file_name: str, ext: str = None) -> str:
    if not file_name.startswith("."):
        languages = extract_languages_from_name(file_name)
        new_name = _USELESS_INFOS_REGEX.sub("", file_name)
        replacement = (
            new_name.replace(".", "_")
            .strip()
            .replace(" ", "_")
            .replace("__", "_")
            .replace("___", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .removesuffix("_")
        )
        replacement += f"_{'_'.join(languages)}" if languages else ""
        return f"{replacement}{ext}" if ext is not None else f"{replacement}"
    return file_name


def _rename(
    root: str,
    to_rename: str,
    new_name: str,
    renamer: Callable[[str, str], None],
):
    file_to_rename = path.join(root, to_rename)
    new_file_name_dest = path.join(root, new_name)
    renamer(
        file_to_rename,
        new_file_name_dest,
    )
    return file_to_rename, new_file_name_dest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="the path where to find your videos", type=Path)
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
        print(
            json.dumps(
                rename_files_and_directories(args.path, DummyRenamer().rename), indent=2
            )
        )
    else:
        search(Path(args.path), args.keyword.split(",")).print()
