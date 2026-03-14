from dataclasses import dataclass

from ..commands.base import Command
from ..commands.command_factory import CommandFactory
from ..domain.direction import Direction
from ..domain.grid import Grid
from ..domain.position import Position
from ..entities.rover import Rover


@dataclass(frozen=True)
class MissionResult:
    position: Position
    direction: Direction
    data_collected: list[Position]


class MissionControl:
    def __init__(self, grid: Grid, rover: Rover) -> None:
        self._grid = grid
        self._rover = rover

    def execute_commands(self, commands: list[Command]) -> MissionResult:
        for command in commands:
            command.execute(self._rover, self._grid)

        return MissionResult(
            position=self._rover.position,
            direction=self._rover.direction,
            data_collected=self._rover.collected_data,
        )

    def execute_from_codes(self, codes: list[str]) -> MissionResult:
        commands = CommandFactory.create_batch(codes)
        return self.execute_commands(commands)
