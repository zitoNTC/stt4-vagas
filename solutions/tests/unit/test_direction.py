import pytest

from mars_rover.domain.direction import Direction


class TestTurnRight:
    def test_north_turns_to_east(self):
        assert Direction.N.turn_right() == Direction.E

    def test_east_turns_to_south(self):
        assert Direction.E.turn_right() == Direction.S

    def test_south_turns_to_west(self):
        assert Direction.S.turn_right() == Direction.W

    def test_west_turns_to_north(self):
        assert Direction.W.turn_right() == Direction.N


class TestTurnLeft:
    def test_north_turns_to_west(self):
        assert Direction.N.turn_left() == Direction.W

    def test_west_turns_to_south(self):
        assert Direction.W.turn_left() == Direction.S

    def test_south_turns_to_east(self):
        assert Direction.S.turn_left() == Direction.E

    def test_east_turns_to_north(self):
        assert Direction.E.turn_left() == Direction.N


class TestOpposite:
    def test_north_opposite_is_south(self):
        assert Direction.N.opposite() == Direction.S

    def test_south_opposite_is_north(self):
        assert Direction.S.opposite() == Direction.N

    def test_east_opposite_is_west(self):
        assert Direction.E.opposite() == Direction.W

    def test_west_opposite_is_east(self):
        assert Direction.W.opposite() == Direction.E


class TestDelta:
    def test_north_moves_row_up(self):
        assert Direction.N.delta() == (-1, 0)

    def test_south_moves_row_down(self):
        assert Direction.S.delta() == (1, 0)

    def test_east_moves_col_right(self):
        assert Direction.E.delta() == (0, 1)

    def test_west_moves_col_left(self):
        assert Direction.W.delta() == (0, -1)


class TestFullRotation:
    def test_four_right_turns_return_to_original(self):
        d = Direction.N
        for _ in range(4):
            d = d.turn_right()
        assert d == Direction.N

    def test_four_left_turns_return_to_original(self):
        d = Direction.E
        for _ in range(4):
            d = d.turn_left()
        assert d == Direction.E

    def test_right_then_left_cancels_out(self):
        for d in Direction:
            assert d.turn_right().turn_left() == d
