from mars_rover.domain.direction import Direction
from mars_rover.domain.position import Position
from mars_rover.entities.rover import Rover


class TestRoverInitialState:
    def test_has_initial_position(self):
        rover = Rover(Position(1, 2), Direction.N)
        assert rover.position == Position(1, 2)

    def test_has_initial_direction(self):
        rover = Rover(Position(0, 0), Direction.E)
        assert rover.direction == Direction.E

    def test_starts_with_no_collected_data(self):
        rover = Rover(Position(0, 0), Direction.N)
        assert rover.collected_data == []


class TestRoverMovement:
    def test_move_to_updates_position(self):
        rover = Rover(Position(0, 0), Direction.E)
        rover.move_to(Position(0, 1))
        assert rover.position == Position(0, 1)


class TestRoverTurning:
    def test_turn_right_updates_direction(self):
        rover = Rover(Position(0, 0), Direction.N)
        rover.turn_right()
        assert rover.direction == Direction.E

    def test_turn_left_updates_direction(self):
        rover = Rover(Position(0, 0), Direction.N)
        rover.turn_left()
        assert rover.direction == Direction.W


class TestRoverDataCollection:
    def test_collect_stores_current_position(self):
        rover = Rover(Position(2, 3), Direction.S)
        rover.collect()
        assert rover.collected_data == [Position(2, 3)]

    def test_multiple_collections_at_different_positions(self):
        rover = Rover(Position(0, 0), Direction.E)
        rover.collect()
        rover.move_to(Position(0, 1))
        rover.collect()
        assert rover.collected_data == [Position(0, 0), Position(0, 1)]

    def test_collected_data_returns_copy(self):
        rover = Rover(Position(0, 0), Direction.N)
        rover.collect()
        data = rover.collected_data
        data.clear()
        assert len(rover.collected_data) == 1
