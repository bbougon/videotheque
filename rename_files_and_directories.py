import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Callable, Tuple

from languages import extract_languages_from_name

_USELESS_INFOS_REGEX = re.compile(
    r"(\[.*])|([0-9]{4}).*|([0-9]{3,4}p.*)|(x[0-9]{3}.*)|(bdrip).*|(brrip).*|(hdrip).*",
    re.IGNORECASE,
)


def rename(root_path: Path, file_renamer: Callable[[str, str], None]):
    renamed_files_and_dirs: Dict[str, List[Dict[str, str]]] = {"files": [], "dirs": []}
    for root, _, files in os.walk(root_path):
        for name in files:
            new_file_name = _forge_new_name(*(os.path.splitext(Path(name))))
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
    for root, dirs, _ in os.walk(root_path):
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


def _forge_new_name(file_name: str, ext: Optional[str] = None) -> str:
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
) -> Tuple[str, str]:
    file_to_rename = os.path.join(root, to_rename)
    new_file_name_dest = os.path.join(root, new_name)
    renamer(
        file_to_rename,
        new_file_name_dest,
    )
    return file_to_rename, new_file_name_dest
