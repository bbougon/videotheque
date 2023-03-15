from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional


class VideoInformationRunner:
    @abstractmethod
    def run(self, *args) -> VideoDetails:
        pass


@dataclass
class VideoDetails:
    duration: str
    languages: Optional[List[str]] = None
