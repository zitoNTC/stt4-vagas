from ..domain.direction import Direction
from ..domain.position import Position


class Rover:
    def __init__(self, position: Position, direction: Direction) -> None:
        self._position = position
        self._direction = direction
        self._collected_data: list[Position] = []

    @property
    def position(self) -> Position:
        return self._position

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def collected_data(self) -> list[Position]:
        return list(self._collected_data)

    def move_to(self, position: Position) -> None:
        self._position = position

    def turn_right(self) -> None:
        self._direction = self._direction.turn_right()

    def turn_left(self) -> None:
        self._direction = self._direction.turn_left()

    def collect(self) -> None:
        self._collected_data.append(self._position)
