from ..domain.grid import Grid
from ..entities.rover import Rover
from .base import Command


class MoveForward(Command):
    def execute(self, rover: Rover, grid: Grid) -> None:
        new_position = rover.position.move(rover.direction)
        if grid.is_valid_position(new_position):
            rover.move_to(new_position)
