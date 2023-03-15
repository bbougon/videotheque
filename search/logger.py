from __future__ import annotations

from datetime import datetime
from typing import Dict


class SearchLogger:
    def __init__(self) -> None:
        super().__init__()
        self.content: Dict = {}

    def log(self, command: str, error: Dict):
        self.content = {
            "datetime": datetime.now().isoformat(),
            "command": command,
        }
        self.content.update(error)
