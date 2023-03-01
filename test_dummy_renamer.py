from typing import List, Tuple


class DummyRenamer:
    def __init__(self) -> None:
        self.moves: List[Tuple[str, str]] = []

    def rename(self, src: str, dest: str):
        self.moves.append((src, dest))
