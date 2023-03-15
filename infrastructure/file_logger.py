from __future__ import annotations

import json
from datetime import datetime
from typing import Dict

from search.logger import SearchLogger


class FileSearchLogger(SearchLogger):
    def log(self, command: str, error: Dict):
        super().log(command, error)
        with open(
            f"{datetime.now().strftime('%Y%m%d')}_search_logger.log", "a+b"
        ) as logger:
            logger.write(bytes(f"{json.dumps(self.content)}\n", "utf-8"))
