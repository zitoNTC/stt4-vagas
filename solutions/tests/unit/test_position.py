import pytest

from mars_rover.domain.direction import Direction
from mars_rover.domain.position import Position


class TestPositionCreation:
    def test_stores_row_and_col(self):
        pos = Position(3, 5)
        assert pos.row == 3
        assert pos.col == 5

    def test_is_immutable(self):
        pos = Position(1, 2)
        with pytest.raises(AttributeError):
            pos.row = 10


class TestPositionMove:
    def test_move_north_decreases_row(self):
        pos = Position(2, 3)
        new = pos.move(Direction.N)
        assert new == Position(1, 3)

    def test_move_south_increases_row(self):
        pos = Position(2, 3)
        new = pos.move(Direction.S)
        assert new == Position(3, 3)

    def test_move_east_increases_col(self):
        pos = Position(2, 3)
        new = pos.move(Direction.E)
        assert new == Position(2, 4)

    def test_move_west_decreases_col(self):
        pos = Position(2, 3)
        new = pos.move(Direction.W)
        assert new == Position(2, 2)

    def test_move_returns_new_instance(self):
        original = Position(0, 0)
        moved = original.move(Direction.E)
        assert original == Position(0, 0)
        assert moved == Position(0, 1)


class TestPositionEquality:
    def test_same_coordinates_are_equal(self):
        assert Position(1, 2) == Position(1, 2)

    def test_different_coordinates_are_not_equal(self):
        assert Position(1, 2) != Position(2, 1)


class TestPositionStr:
    def test_string_representation(self):
        assert str(Position(3, 7)) == "(3, 7)"
