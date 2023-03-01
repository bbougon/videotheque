import getopt
import json
import re
import sys
from os import walk, rename, path
from pathlib import Path
from typing import Callable

from test_dummy_renamer import DummyRenamer

_USELESS_INFOS_REGEX = re.compile(
    r"(\[.*])|([0-9]{4}).*|([0-9]{3,4}p.*)|(x[0-9]{3}.*)|(bdrip).*|(brrip).*|(hdrip).*",
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


def _forge_new_name(file_name: str, ext: str = None) -> str:
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
    return [
        language
        for key, language in _LANGUAGES.items()
        if key in flatten_file_name or key.casefold() in flatten_file_name
    ]


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
