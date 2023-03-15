from typing import List, Optional

from search.exceptions import RunnerException
from search.runner import VideoInformationRunner, VideoDetails
from search.logger import SearchLogger


class DummyRunner(VideoInformationRunner):
    arguments: List[str]

    def __init__(
        self,
        raise_exception: bool = False,
        video_details: Optional[VideoDetails] = None,
    ) -> None:
        super().__init__()
        self.arguments = []
        self.raise_exception = raise_exception
        self.video_details = video_details

    def run(self, *args) -> VideoDetails:
        if self.raise_exception:
            raise RunnerException(
                "Error occurred", -1, b"An error", args="no args"
            )
        self.arguments.append(*args)
        return (
            self.video_details
            if self.video_details is not None
            else VideoDetails(languages=[], duration="01:30:09.36")
        )


class MemoryLogger(SearchLogger):
    pass
