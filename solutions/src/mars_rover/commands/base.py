from abc import ABC, abstractmethod

from ..domain.grid import Grid
from ..entities.rover import Rover


class Command(ABC):
    @abstractmethod
    def execute(self, rover: Rover, grid: Grid) -> None:
        ...
