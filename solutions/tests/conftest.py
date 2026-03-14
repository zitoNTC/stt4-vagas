import pytest

from mars_rover.domain.direction import Direction
from mars_rover.domain.grid import Grid
from mars_rover.domain.position import Position
from mars_rover.entities.rover import Rover


@pytest.fixture
def open_3x3_grid():
    return Grid([[0, 0, 0], [0, 0, 0], [0, 0, 0]])


@pytest.fixture
def grid_with_center_obstacle():
    return Grid([[0, 0, 0], [0, 1, 0], [0, 0, 0]])


@pytest.fixture
def origin():
    return Position(0, 0)


@pytest.fixture
def rover_at_origin_facing_east(origin):
    return Rover(origin, Direction.E)
