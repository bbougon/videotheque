from typing import List

from search.exceptions import RunnerException
from search.runner import VideoInformationRunner, VideoDetails
from search.logger import SearchLogger


class DummyRunner(VideoInformationRunner):
    arguments: List[str]

    def __init__(self, raise_exception: bool = False) -> None:
        super().__init__()
        self.arguments = []
        self.raise_exception = raise_exception

    def run(self, *args) -> VideoDetails:
        if self.raise_exception:
            raise RunnerException(
                "Error occurred", -1, b"An error", args="no args"
            )
        self.arguments.append(*args)
        return VideoDetails(languages=[], duration="01:30:09.36")


class MemoryLogger(SearchLogger):
    pass
