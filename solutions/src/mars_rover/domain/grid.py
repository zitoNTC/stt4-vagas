from .position import Position


class Grid:
    OBSTACLE = 1

    def __init__(self, matrix: list[list[int]]) -> None:
        if not matrix or not matrix[0]:
            raise ValueError("Grid matrix must be non-empty")
        self._matrix = matrix
        self._rows = len(matrix)
        self._cols = len(matrix[0])

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self._rows and 0 <= position.col < self._cols

    def has_obstacle(self, position: Position) -> bool:
        return self._matrix[position.row][position.col] == self.OBSTACLE

    def is_valid_position(self, position: Position) -> bool:
        return self.is_within_bounds(position) and not self.has_obstacle(position)
