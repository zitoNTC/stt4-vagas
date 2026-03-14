from ..domain.grid import Grid
from ..entities.rover import Rover
from .base import Command


class TurnRight(Command):
    def execute(self, rover: Rover, grid: Grid) -> None:
        rover.turn_right()
