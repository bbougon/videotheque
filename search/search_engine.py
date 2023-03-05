from __future__ import annotations
import mimetypes
import os
import subprocess
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess
from typing import List, Optional, Dict

from prettytable import PrettyTable

from languages import extract_languages_from_name
from search.exceptions import RunnerException
from search.video_file_types import VIDEO_FILE_TYPES
from settings import config


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


class VideoInformationRunner:
    @abstractmethod
    def run(self, *args):
        pass


class FFProbeRunner(VideoInformationRunner):
    def __init__(self) -> None:
        self.runner = config("VIDEO.RUNNER")

    def run(self, *args):
        command = f"{self.runner} {''.join(args)}"
        completed_process: CompletedProcess = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        if completed_process.returncode != 0:
            raise RunnerException(
                "Impossible to run the command",
                completed_process.returncode,
                completed_process.stderr,
                completed_process.args,
            )
        return completed_process.stdout.decode("utf-8")


class SearchEngine:
    def __init__(
        self,
        runner: VideoInformationRunner = FFProbeRunner(),
        logger: Optional[SearchLogger] = None,
    ) -> None:
        super().__init__()
        self.runner = runner
        self.logger = logger

    def run(
        self,
        root_path: Path,
        keywords: List[str],
    ) -> SearchResult:
        result = SearchResult()
        for root, _, files in os.walk(root_path):
            for name in files:
                type, _ = mimetypes.guess_type(name)
                if not name.startswith(".") and type in VIDEO_FILE_TYPES:
                    movie_name, _ = os.path.splitext(Path(name))
                    result.add(
                        Movie(
                            movie_name,
                            self.search_for_duration(os.path.join(root, name)),
                            [
                                name.capitalize()
                                for name in extract_languages_from_name(name)
                            ],
                        )
                    )
        return result

    def search_for_duration(self, path: str) -> str:
        try:
            final_path = (
                path.replace(" ", "\\ ")
                .replace("&", "\\&")
                .replace("(", "\\(")
                .replace(")", "\\)")
            )
            return self.runner.run(
                f"-i {final_path} -show_entries format=duration -v quiet -of csv='p=0' -sexagesimal"
            )
        except RunnerException as e:
            self.logger.log(config("VIDEO.RUNNER"), e.details)
            return "unable to get duration (see error log file)"


class SearchLogger:
    def __init__(self) -> None:
        super().__init__()
        self.content: Dict = {}

    def log(self, command: str, error: Dict):
        self.content = {"datetime": datetime.now().isoformat(), "command": command}
        self.content.update(error)
