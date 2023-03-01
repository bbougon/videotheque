import getopt
import json
import os
from os import walk, rename, path
import re
import sys
from pathlib import Path
from typing import Callable

_USELESS_INFOS_REGEX = re.compile(
    r"(\[.*\])|([0-9]{4})|(\(.*\))|([0-9]{3,4}p.*)|(x[0-9]{3}.*)|(bdrip).*|(brrip).*|(hdrip).*",
    re.IGNORECASE,
)
_LANGUAGES = ["PORTUGUESE", "FRENCH", "FR", "ENG", "VOSTFR"]


def _rename(file_name: str, ext: str = None) -> str:
    new_name = _USELESS_INFOS_REGEX.sub("", file_name)
    replacement = (
        new_name.replace(".", "_")
        .strip()
        .replace(" ", "_")
        .replace("__", "_")
        .replace("___", "_")
        .removesuffix("_")
    )
    return f"{replacement}{ext}" if ext is not None else f"{replacement}"


def rename_files_and_directories(
    root_path: Path, file_renamer: Callable[[str, str], None] = rename
):
    renamed_files_and_dirs = {"files": [], "dirs": []}
    for root, _, files in walk(root_path):
        for name in files:
            file_to_rename = path.join(root, name)
            new_file_name = path.join(root, _rename(*(path.splitext(Path(name)))))
            renamed_files_and_dirs["files"].append(
                {"from": file_to_rename, "to": new_file_name}
            )
            file_renamer(
                file_to_rename,
                new_file_name,
            )

    for root, dirs, _ in walk(root_path):
        for dir in dirs:
            dir_to_rename = path.join(root, dir)
            new_dir_name = path.join(root, _rename(dir))
            renamed_files_and_dirs["dirs"].append(
                {"from": dir_to_rename, "to": new_dir_name}
            )
            file_renamer(dir_to_rename, new_dir_name)
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
    print(json.dumps(rename_files_and_directories(Path(file_path))))
