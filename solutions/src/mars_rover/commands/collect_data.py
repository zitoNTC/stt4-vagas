from ..domain.grid import Grid
from ..entities.rover import Rover
from .base import Command


class CollectData(Command):
    def execute(self, rover: Rover, grid: Grid) -> None:
        rover.collect()
