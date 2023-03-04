from typing import List

from search.search_engine import VideoInformationRunner


class DummyRunner(VideoInformationRunner):
    arguments: List[str]

    def __init__(self) -> None:
        super().__init__()
        self.arguments = []

    def run(self, *args):
        self.arguments.append(*args)
        return "01:30:09.36"
