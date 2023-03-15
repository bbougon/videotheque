from __future__ import annotations

import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from prettytable import PrettyTable
from progress.bar import IncrementalBar

from infrastructure.ffprobe.ffprobe import FFProbeRunner
from languages import extract_languages_from_name, map_languages
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
        all_movies = self.__search_all_movies(keywords, root_path)
        self.__retrieve_movies_informations(all_movies, result)
        return result

    def __retrieve_movies_informations(self, all_movies, result):
        bar = IncrementalBar(
            "Searching", max=len(all_movies), color="green", style="faint"
        )
        for movie, path in all_movies:
            details = self.search_for_video_details(path)
            languages = (
                [
                    language.capitalize()
                    for language in map_languages(details.languages)
                ]
                if details.languages
                else [
                    name.capitalize()
                    for name in extract_languages_from_name(movie)
                ]
            )
            result.add(
                Movie(
                    movie,
                    details.duration,
                    languages,
                )
            )
            bar.next()
        bar.finish()

    def __search_all_movies(self, keywords, root_path):
        all_movies = []
        for root, _, files in os.walk(root_path):
            type = lambda name: mimetypes.guess_type(name)[0]
            movie_name = lambda name: os.path.splitext(Path(name))[0]
            movies = [
                (movie_name(name), os.path.join(root, name))
                for name in files
                if not name.startswith(".")
                and type(name) in VIDEO_FILE_TYPES
                and self._has_all_keywords_in_name(keywords, name)
            ]
            all_movies.extend(movies)
        return all_movies

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
