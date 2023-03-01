import subprocess
from dataclasses import dataclass
from os import walk, path
from pathlib import Path
from subprocess import CompletedProcess
from typing import List

from prettytable import PrettyTable

from languages import extract_languages_from_name


@dataclass
class Movie:
    title: str
    duration: str
    languages: List[str]


class SearchResult:
    def __init__(self) -> None:
        super().__init__()
        self.movies: List[Movie] = []

    def print(self):
        pretty_table = PrettyTable()
        pretty_table.field_names = ["Film name", "Duration", "Language"]
        for movie in self.movies:
            pretty_table.add_row([movie.title, movie.duration, movie.languages])
        print(pretty_table)

    def add(self, movie: Movie):
        self.movies.append(movie)


class SearchEngine:
    def __init__(self, root_path: Path, keywords: List[str]) -> None:
        super().__init__()
        self.root_path = root_path
        self.keywords = keywords

    def run(self) -> SearchResult:
        result = SearchResult()
        for root, _, files in walk(self.root_path):
            for name in files:
                movie_name, _ = path.splitext(Path(name))
                result.add(
                    Movie(
                        movie_name,
                        self.search_for_duration(path.join(root, name)),
                        [
                            name.capitalize()
                            for name in extract_languages_from_name(name)
                        ],
                    )
                )
        return result

    def search_for_duration(self, path: str) -> str:
        completed_process: CompletedProcess = subprocess.run(
            [
                "ffprobe",
                "-i",
                path,
                "-show_entries",
                "format=duration",
                "-v",
                "quiet",
                "-of",
                'csv="p=0"',
                "-sexagesimal",
            ],
            capture_output=True,
        )
        return completed_process.stdout.decode("utf-8")
