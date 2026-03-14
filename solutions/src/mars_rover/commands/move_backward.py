from ..domain.grid import Grid
from ..entities.rover import Rover
from .base import Command


class MoveBackward(Command):
    def execute(self, rover: Rover, grid: Grid) -> None:
        opposite = rover.direction.opposite()
        new_position = rover.position.move(opposite)
        if grid.is_valid_position(new_position):
            rover.move_to(new_position)
