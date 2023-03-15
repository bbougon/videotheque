from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import List


class VideoInformationRunner:
    @abstractmethod
    def run(self, *args) -> VideoDetails:
        pass


@dataclass
class VideoDetails:
    languages: List[str]
    duration: str
