import pytest

from mars_rover.commands import (
    CollectData,
    MoveBackward,
    MoveForward,
    TurnLeft,
    TurnRight,
)
from mars_rover.domain.direction import Direction
from mars_rover.domain.grid import Grid
from mars_rover.domain.position import Position
from mars_rover.entities.rover import Rover


class TestMoveForward:
    def test_moves_to_free_cell(self, open_3x3_grid):
        rover = Rover(Position(0, 0), Direction.E)
        MoveForward().execute(rover, open_3x3_grid)
        assert rover.position == Position(0, 1)

    def test_blocked_by_obstacle(self, grid_with_center_obstacle):
        rover = Rover(Position(0, 1), Direction.S)
        MoveForward().execute(rover, grid_with_center_obstacle)
        assert rover.position == Position(0, 1)

    def test_blocked_by_boundary(self, open_3x3_grid):
        rover = Rover(Position(0, 0), Direction.N)
        MoveForward().execute(rover, open_3x3_grid)
        assert rover.position == Position(0, 0)

    def test_does_not_change_direction(self, open_3x3_grid):
        rover = Rover(Position(0, 0), Direction.E)
        MoveForward().execute(rover, open_3x3_grid)
        assert rover.direction == Direction.E


class TestMoveBackward:
    def test_moves_opposite_of_facing(self, open_3x3_grid):
        rover = Rover(Position(1, 1), Direction.N)
        MoveBackward().execute(rover, open_3x3_grid)
        assert rover.position == Position(2, 1)

    def test_blocked_by_obstacle(self, grid_with_center_obstacle):
        rover = Rover(Position(2, 1), Direction.S)
        MoveBackward().execute(rover, grid_with_center_obstacle)
        assert rover.position == Position(2, 1)

    def test_blocked_by_boundary(self, open_3x3_grid):
        rover = Rover(Position(2, 2), Direction.N)
        MoveBackward().execute(rover, open_3x3_grid)
        assert rover.position == Position(2, 2)

    def test_preserves_direction(self, open_3x3_grid):
        rover = Rover(Position(1, 1), Direction.N)
        MoveBackward().execute(rover, open_3x3_grid)
        assert rover.direction == Direction.N


class TestTurnRight:
    def test_changes_direction_clockwise(self, open_3x3_grid):
        rover = Rover(Position(0, 0), Direction.N)
        TurnRight().execute(rover, open_3x3_grid)
        assert rover.direction == Direction.E

    def test_does_not_change_position(self, open_3x3_grid):
        rover = Rover(Position(1, 2), Direction.S)
        TurnRight().execute(rover, open_3x3_grid)
        assert rover.position == Position(1, 2)


class TestTurnLeft:
    def test_changes_direction_counter_clockwise(self, open_3x3_grid):
        rover = Rover(Position(0, 0), Direction.N)
        TurnLeft().execute(rover, open_3x3_grid)
        assert rover.direction == Direction.W

    def test_does_not_change_position(self, open_3x3_grid):
        rover = Rover(Position(1, 2), Direction.S)
        TurnLeft().execute(rover, open_3x3_grid)
        assert rover.position == Position(1, 2)


class TestCollectData:
    def test_records_current_position(self, open_3x3_grid):
        rover = Rover(Position(2, 1), Direction.E)
        CollectData().execute(rover, open_3x3_grid)
        assert rover.collected_data == [Position(2, 1)]
