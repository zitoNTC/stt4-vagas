import pytest

from mars_rover.domain.grid import Grid
from mars_rover.domain.position import Position


class TestGridCreation:
    def test_stores_dimensions(self):
        grid = Grid([[0, 0], [0, 0], [0, 0]])
        assert grid.rows == 3
        assert grid.cols == 2

    def test_rejects_empty_matrix(self):
        with pytest.raises(ValueError):
            Grid([])

    def test_rejects_empty_rows(self):
        with pytest.raises(ValueError):
            Grid([[]])


class TestWithinBounds:
    def test_origin_is_within_bounds(self, open_3x3_grid):
        assert open_3x3_grid.is_within_bounds(Position(0, 0)) is True

    def test_max_corner_is_within_bounds(self, open_3x3_grid):
        assert open_3x3_grid.is_within_bounds(Position(2, 2)) is True

    def test_negative_row_is_out_of_bounds(self, open_3x3_grid):
        assert open_3x3_grid.is_within_bounds(Position(-1, 0)) is False

    def test_negative_col_is_out_of_bounds(self, open_3x3_grid):
        assert open_3x3_grid.is_within_bounds(Position(0, -1)) is False

    def test_row_overflow_is_out_of_bounds(self, open_3x3_grid):
        assert open_3x3_grid.is_within_bounds(Position(3, 0)) is False

    def test_col_overflow_is_out_of_bounds(self, open_3x3_grid):
        assert open_3x3_grid.is_within_bounds(Position(0, 3)) is False


class TestHasObstacle:
    def test_free_cell_has_no_obstacle(self, grid_with_center_obstacle):
        assert grid_with_center_obstacle.has_obstacle(Position(0, 0)) is False

    def test_obstacle_cell_detected(self, grid_with_center_obstacle):
        assert grid_with_center_obstacle.has_obstacle(Position(1, 1)) is True


class TestIsValidPosition:
    def test_free_in_bounds_is_valid(self, open_3x3_grid):
        assert open_3x3_grid.is_valid_position(Position(1, 1)) is True

    def test_obstacle_is_invalid(self, grid_with_center_obstacle):
        assert grid_with_center_obstacle.is_valid_position(Position(1, 1)) is False

    def test_out_of_bounds_is_invalid(self, open_3x3_grid):
        assert open_3x3_grid.is_valid_position(Position(5, 5)) is False
