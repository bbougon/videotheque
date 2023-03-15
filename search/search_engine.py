from __future__ import annotations

import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from prettytable import PrettyTable

from infrastructure.ffprobe.ffprobe import FFProbeRunner
from languages import extract_languages_from_name
from search.exceptions import RunnerException
from search.logger import SearchLogger
from search.runner import VideoInformationRunner, VideoDetails
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
            pretty_table.add_row(
                [movie.title, movie.duration, movie.languages]
            )
        print(pretty_table, f"\nTotal results: {len(self.movies)}")

    def add(self, movie: Movie):
        self.movies.append(movie)


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
                if (
                    not name.startswith(".")
                    and type in VIDEO_FILE_TYPES
                    and self._has_all_keywords_in_name(keywords, name)
                ):
                    movie_name, _ = os.path.splitext(Path(name))
                    details = self.search_for_video_details(
                        os.path.join(root, name)
                    )
                    result.add(
                        Movie(
                            movie_name,
                            details.duration,
                            [
                                name.capitalize()
                                for name in extract_languages_from_name(name)
                            ],
                        )
                    )
        return result

    def _has_all_keywords_in_name(
        self, keywords: List[str], name: str
    ) -> bool:
        return (
            len(
                list(
                    filter(
                        lambda has_occurence: has_occurence is True,
                        [
                            name.casefold().find(keyword.casefold()) >= 0
                            for keyword in keywords
                        ],
                    )
                )
            )
            == len(keywords)
            if keywords
            else True
        )

    def search_for_video_details(self, path: str) -> VideoDetails:
        try:
            final_path = (
                path.replace(" ", "\\ ")
                .replace("&", "\\&")
                .replace("(", "\\(")
                .replace(")", "\\)")
            )
            return self.runner.run(final_path)
        except RunnerException as e:
            if self.logger is not None:
                self.logger.log(config("VIDEO.RUNNER"), e.details)
            return VideoDetails(
                languages=[],
                duration="unable to get duration (see error log file)",
            )
