from __future__ import annotations

from enum import Enum


_CLOCKWISE = ["N", "E", "S", "W"]

_DELTAS: dict[str, tuple[int, int]] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


class Direction(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_right(self) -> Direction:
        idx = _CLOCKWISE.index(self.value)
        return Direction(_CLOCKWISE[(idx + 1) % 4])

    def turn_left(self) -> Direction:
        idx = _CLOCKWISE.index(self.value)
        return Direction(_CLOCKWISE[(idx - 1) % 4])

    def opposite(self) -> Direction:
        idx = _CLOCKWISE.index(self.value)
        return Direction(_CLOCKWISE[(idx + 2) % 4])

    def delta(self) -> tuple[int, int]:
        return _DELTAS[self.value]
