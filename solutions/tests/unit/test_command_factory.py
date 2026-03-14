import pytest

from mars_rover.commands import (
    CollectData,
    CommandFactory,
    MoveBackward,
    MoveForward,
    TurnLeft,
    TurnRight,
)


class TestCreateSingle:
    @pytest.mark.parametrize(
        "code,expected_type",
        [
            ("F", MoveForward),
            ("B", MoveBackward),
            ("L", TurnLeft),
            ("R", TurnRight),
            ("S", CollectData),
        ],
    )
    def test_creates_correct_command(self, code, expected_type):
        assert isinstance(CommandFactory.create(code), expected_type)

    def test_handles_lowercase(self):
        assert isinstance(CommandFactory.create("f"), MoveForward)

    def test_handles_whitespace(self):
        assert isinstance(CommandFactory.create(" R "), TurnRight)

    def test_raises_on_unknown_command(self):
        with pytest.raises(ValueError, match="Unknown command"):
            CommandFactory.create("X")


class TestCreateBatch:
    def test_creates_list_of_commands(self):
        commands = CommandFactory.create_batch(["F", "R", "S"])
        assert len(commands) == 3
        assert isinstance(commands[0], MoveForward)
        assert isinstance(commands[1], TurnRight)
        assert isinstance(commands[2], CollectData)

    def test_empty_list_returns_empty(self):
        assert CommandFactory.create_batch([]) == []
