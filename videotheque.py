import getopt
import json
import os
from os import walk, rename, path
import re
import sys
from pathlib import Path
from typing import Callable, Tuple

from test_dummy_renamer import DummyRenamer

_USELESS_INFOS_REGEX = re.compile(
    r"(\[.*\])|([0-9]{4}).*|([0-9]{3,4}p.*)|(x[0-9]{3}.*)|(bdrip).*|(brrip).*|(hdrip).*",
    re.IGNORECASE,
)
_LANGUAGES = {
    "PORTUGUESE": "PORTUGUESE",
    "PT": "PORTUGUESE",
    "BR": "PORTUGUESE",
    "FRENCH": "FRENCH",
    "FR": "FRENCH",
    "FRE": "FRENCH",
    "ENG": "ENGLISH",
    "EN": "ENGLISH",
    "US": "ENGLISH",
    "VOSTFR": "VOSTFR",
}


def _rename(file_name: str, ext: str = None) -> str:
    languages = _extract_languages_from_name(file_name)
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


def _extract_languages_from_name(file_name):
    flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
    flatten_file_name = flat_map(
        lambda x: x, [el.split(" ") for el in file_name.split(".")]
    )
    languages = [
        language
        for key, language in _LANGUAGES.items()
        if key in flatten_file_name or key.casefold() in flatten_file_name
    ]
    return languages


def rename_files_and_directories(
    root_path: Path, file_renamer: Callable[[str, str], None] = rename
):
    renamed_files_and_dirs = {"files": [], "dirs": []}
    for root, _, files in walk(root_path):
        for name in files:
            new_file_name = _rename(*(path.splitext(Path(name))))
            if new_file_name != name:
                file_to_rename = path.join(root, name)
                new_file_name_dest = path.join(root, new_file_name)
                renamed_files_and_dirs["files"].append(
                    {"from": file_to_rename, "to": new_file_name_dest}
                )
                file_renamer(
                    file_to_rename,
                    new_file_name_dest,
                )

    for root, dirs, _ in walk(root_path):
        for dir in dirs:
            new_dir_name = _rename(dir)
            if new_dir_name != dir:
                dir_to_rename = path.join(root, dir)
                new_dir_name_dest = path.join(root, new_dir_name)
                renamed_files_and_dirs["dirs"].append(
                    {"from": dir_to_rename, "to": new_dir_name_dest}
                )
                file_renamer(dir_to_rename, new_dir_name_dest)
    return renamed_files_and_dirs


if __name__ == "__main__":
    file_path = ""
    opts, args = getopt.getopt(sys.argv[1:], "hf:", ["file-path="])
    for opt, arg in opts:
        if opt == "-h":
            print("videotheque.py -f <file_path>")
            sys.exit()
        elif opt in ("-f", "--file-path"):
            file_path = arg
    print(
        json.dumps(rename_files_and_directories(Path(file_path), DummyRenamer().rename))
    )
