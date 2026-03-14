import pytest

from mars_rover.domain.direction import Direction
from mars_rover.domain.grid import Grid
from mars_rover.domain.position import Position
from mars_rover.entities.rover import Rover
from mars_rover.services.mission_control import MissionControl


def _run_mission(
    grid_data: list[list[int]],
    start_pos: tuple[int, int],
    start_dir: str,
    commands: list[str],
):
    grid = Grid(grid_data)
    position = Position(start_pos[0], start_pos[1])
    direction = Direction(start_dir)
    rover = Rover(position, direction)
    mission = MissionControl(grid, rover)
    return mission.execute_from_codes(commands)


class TestScenario3:
    """Complex path with multiple obstacles -- the best-verified scenario."""

    def test_final_position(self):
        result = _run_mission(
            grid_data=[
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "R", "F", "F", "L", "F", "F", "R", "F", "S"],
        )
        assert result.position == Position(3, 2)

    def test_final_direction(self):
        result = _run_mission(
            grid_data=[
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "R", "F", "F", "L", "F", "F", "R", "F", "S"],
        )
        assert result.direction == Direction.S

    def test_data_collected(self):
        result = _run_mission(
            grid_data=[
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "R", "F", "F", "L", "F", "F", "R", "F", "S"],
        )
        assert result.data_collected == [Position(3, 2)]


class TestScenario1:
    """Simple path with no obstacles.

    Note: the challenge document states the expected output as (2, 1),
    which corresponds to (col, row) format. With (row, col) convention
    (validated by Scenario 3), the result is (1, 2).
    """

    def test_final_position(self):
        result = _run_mission(
            grid_data=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "F", "R", "F", "S"],
        )
        assert result.position == Position(1, 2)

    def test_final_direction_is_south(self):
        result = _run_mission(
            grid_data=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "F", "R", "F", "S"],
        )
        assert result.direction == Direction.S

    def test_data_collected(self):
        result = _run_mission(
            grid_data=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "F", "R", "F", "S"],
        )
        assert result.data_collected == [Position(1, 2)]


class TestScenario2:
    """Encountering and avoiding obstacles.

    The rover follows commands and skips moves that would hit obstacles.
    """

    def test_rover_skips_blocked_moves(self):
        result = _run_mission(
            grid_data=[
                [0, 0, 1, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [1, 0, 1, 0],
            ],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "F", "R", "F", "F", "L", "F", "S"],
        )
        assert result.position == Position(0, 1)
        assert result.direction == Direction.E
        assert result.data_collected == [Position(0, 1)]


class TestScenario4:
    """Hitting the boundary of the grid.

    The rover follows commands and skips moves at boundaries/obstacles.
    """

    def test_rover_handles_obstacles_and_boundary(self):
        result = _run_mission(
            grid_data=[[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            start_pos=(2, 0),
            start_dir="E",
            commands=["F", "L", "F", "F", "S"],
        )
        assert result.position == Position(2, 1)
        assert result.direction == Direction.N
        assert result.data_collected == [Position(2, 1)]


class TestEdgeCases:
    def test_no_commands(self):
        result = _run_mission(
            grid_data=[[0, 0], [0, 0]],
            start_pos=(0, 0),
            start_dir="N",
            commands=[],
        )
        assert result.position == Position(0, 0)
        assert result.direction == Direction.N
        assert result.data_collected == []

    def test_all_moves_blocked(self):
        result = _run_mission(
            grid_data=[[0, 1], [1, 1]],
            start_pos=(0, 0),
            start_dir="E",
            commands=["F", "R", "F", "R", "F", "R", "F"],
        )
        assert result.position == Position(0, 0)

    def test_multiple_data_collections(self):
        result = _run_mission(
            grid_data=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            start_pos=(0, 0),
            start_dir="E",
            commands=["S", "F", "S", "F", "S"],
        )
        assert result.data_collected == [
            Position(0, 0),
            Position(0, 1),
            Position(0, 2),
        ]

    def test_backward_movement(self):
        result = _run_mission(
            grid_data=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            start_pos=(1, 1),
            start_dir="N",
            commands=["B", "S"],
        )
        assert result.position == Position(2, 1)
        assert result.direction == Direction.N
        assert result.data_collected == [Position(2, 1)]

    def test_full_rotation_returns_to_same_direction(self):
        result = _run_mission(
            grid_data=[[0]],
            start_pos=(0, 0),
            start_dir="E",
            commands=["R", "R", "R", "R"],
        )
        assert result.direction == Direction.E

    def test_backward_blocked_by_boundary(self):
        result = _run_mission(
            grid_data=[[0, 0], [0, 0]],
            start_pos=(0, 0),
            start_dir="S",
            commands=["B"],
        )
        assert result.position == Position(0, 0)

    def test_single_cell_grid(self):
        result = _run_mission(
            grid_data=[[0]],
            start_pos=(0, 0),
            start_dir="N",
            commands=["F", "B", "L", "R", "S"],
        )
        assert result.position == Position(0, 0)
        assert result.direction == Direction.N
        assert result.data_collected == [Position(0, 0)]
