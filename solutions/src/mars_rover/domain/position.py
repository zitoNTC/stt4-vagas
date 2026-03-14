from __future__ import annotations

from dataclasses import dataclass

from .direction import Direction


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def move(self, direction: Direction) -> Position:
        d_row, d_col = direction.delta()
        return Position(self.row + d_row, self.col + d_col)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"
