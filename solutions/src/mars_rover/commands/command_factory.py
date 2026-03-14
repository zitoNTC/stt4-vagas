from .base import Command
from .move_forward import MoveForward
from .move_backward import MoveBackward
from .turn_left import TurnLeft
from .turn_right import TurnRight
from .collect_data import CollectData


_COMMAND_MAP: dict[str, type[Command]] = {
    "F": MoveForward,
    "B": MoveBackward,
    "L": TurnLeft,
    "R": TurnRight,
    "S": CollectData,
}


class CommandFactory:
    @staticmethod
    def create(code: str) -> Command:
        command_cls = _COMMAND_MAP.get(code.strip().upper())
        if command_cls is None:
            raise ValueError(f"Unknown command: '{code}'")
        return command_cls()

    @staticmethod
    def create_batch(codes: list[str]) -> list[Command]:
        return [CommandFactory.create(code) for code in codes]
