import json
import sys

from .domain.direction import Direction
from .domain.grid import Grid
from .domain.position import Position
from .entities.rover import Rover
from .services.mission_control import MissionControl


def run(input_data: dict) -> dict:
    grid = Grid(input_data["grid"])

    pos = input_data["position"]
    position = Position(row=pos[0], col=pos[1])
    direction = Direction(input_data["direction"])

    rover = Rover(position, direction)
    mission = MissionControl(grid, rover)

    result = mission.execute_from_codes(input_data["commands"])

    return {
        "position": [result.position.row, result.position.col],
        "direction": result.direction.value,
        "data_collected": [
            [p.row, p.col] for p in result.data_collected
        ],
    }


def main() -> None:
    input_data = json.load(sys.stdin)
    output = run(input_data)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
