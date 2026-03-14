# Mars Rover Control System

A Python implementation of the Mars Rover challenge — a control system that navigates a rover through a 2D grid, avoiding obstacles and collecting data.

## Quick Start

### With Docker

```bash
# Build the image
docker compose build

# Run the test suite
docker compose run test

# Run the application (reads JSON from stdin)
echo '{"grid":[[0,0,0],[0,0,0],[0,0,0]],"position":[0,0],"direction":"E","commands":["F","F","R","F","S"]}' | docker compose run -T app
```

### Without Docker

```bash
pip install -r requirements.txt

# Run tests
PYTHONPATH=src pytest -v

# Run tests with coverage
PYTHONPATH=src pytest --cov=mars_rover --cov-report=term-missing -v

# Run the application
echo '{"grid":[[0,0,0],[0,0,0],[0,0,0]],"position":[0,0],"direction":"E","commands":["F","F","R","F","S"]}' | PYTHONPATH=src python -m mars_rover.main
```

## Input / Output Format

### Input (JSON via stdin)

```json
{
  "grid": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
  "position": [0, 0],
  "direction": "E",
  "commands": ["F", "F", "R", "F", "S"]
}
```

- **grid**: 2D array where `0` = free cell, `1` = obstacle. Indexed as `grid[row][col]`.
- **position**: `[row, col]` starting position of the rover.
- **direction**: Initial orientation — `"N"`, `"S"`, `"E"`, or `"W"`.
- **commands**: List of command codes: `"F"` (forward), `"B"` (backward), `"L"` (turn left), `"R"` (turn right), `"S"` (collect data).

### Output (JSON to stdout)

```json
{
  "position": [1, 2],
  "direction": "S",
  "data_collected": [[1, 2]]
}
```

## Architecture

```
src/mars_rover/
├── domain/          # Value objects and domain rules
│   ├── direction.py   Direction enum with turn/delta logic
│   ├── position.py    Immutable (row, col) coordinate
│   └── grid.py        Grid terrain with obstacle detection
├── entities/        # Stateful domain entities
│   └── rover.py       Rover with position, direction, collected data
├── commands/        # Command pattern implementations
│   ├── base.py        Abstract Command interface
│   ├── move_forward.py
│   ├── move_backward.py
│   ├── turn_left.py
│   ├── turn_right.py
│   ├── collect_data.py
│   └── command_factory.py  String-to-Command mapping
├── services/        # Application orchestration
│   └── mission_control.py  Runs a full mission
└── main.py          # CLI entry point
```

## Design Decisions

### SOLID Principles

| Principle | How it is applied |
|---|---|
| **Single Responsibility** | Each class has one concern: `Direction` handles rotation, `Position` is a coordinate, `Grid` knows terrain, `Rover` holds state, each `Command` knows how to execute itself, `MissionControl` orchestrates. |
| **Open/Closed** | New commands can be added by creating a new `Command` subclass and registering it in `CommandFactory`, without modifying existing command classes. |
| **Liskov Substitution** | All five command classes (`MoveForward`, `TurnLeft`, etc.) are interchangeable through the `Command` abstract base class. |
| **Interface Segregation** | The `Command` interface exposes a single `execute(rover, grid)` method. No class implements unused methods. |
| **Dependency Inversion** | `MissionControl` depends on the `Command` abstraction, not concrete implementations. Only `CommandFactory` knows about concrete classes. |

### Key Patterns

- **Command Pattern**: Each rover instruction is an object that encapsulates the action, enabling easy extension and testing.
- **Value Object**: `Position` is a frozen dataclass — immutable, compared by value. Moving returns a new instance.
- **Factory**: `CommandFactory` translates string codes into `Command` objects, isolating construction from usage.

### Coordinate System

- Position is represented as `(row, col)`.
- The grid is accessed as `grid[row][col]`.
- Compass directions map to grid deltas:
  - **N** = row - 1 (up)
  - **S** = row + 1 (down)
  - **E** = col + 1 (right)
  - **W** = col - 1 (left)
- When a move would land on an obstacle or outside the grid, the command is ignored and the rover stays in place.

### Notes on Challenge Examples

Scenario 3 from the challenge document was used as the primary reference for validating the coordinate system, as it involves the most complex obstacle navigation and produces a result fully consistent with the `(row, col)` convention. The implementation follows this single, consistent convention for all scenarios.

**Scenario 1** — The expected output is `(2, 1)` facing `S`, but tracing the commands `F, F, R, F, S` from `(0, 0)` facing `E` on a 3x3 grid: the rover moves to `(0, 1)`, then `(0, 2)` (two steps east increasing the column), turns right to face `S`, moves to `(1, 2)` (one step south increasing the row), and collects. The correct result is `(1, 2)` facing `S`. The expected `(2, 1)` appears to have the row and column values swapped.

**Scenario 2** — The expected output is `(3, 1)` facing `N`, but tracing the commands `F, F, R, F, F, L, F, S` on the given grid yields `(0, 1)` facing `E`. The rover reaches `(0, 1)` on the first `F`, then every subsequent forward move is blocked by obstacles at `grid[0][2]` and `grid[1][1]`. The orientation after one `R` and one `L` returns to `E`, not `N`. The expected result would require additional movements or turns not present in the command sequence.

**Scenario 4** — The expected output is `(1, 1)` facing `W`, but position `(1, 1)` contains an obstacle (`grid[1][1] = 1`). The rover cannot occupy an obstacle cell. Tracing the commands `F, L, F, F, S` from `(2, 0)` facing `E`: the rover moves to `(2, 1)`, turns left to face `N`, then both forward moves toward `(1, 1)` are blocked by the obstacle. The correct result is `(2, 1)` facing `N`.

## Testing

The project has **90 tests** organized into:

- **Unit tests** (`tests/unit/`): test each class in isolation — directions, positions, grid bounds, rover state, all command types, and the command factory.
- **Integration tests** (`tests/integration/`): full end-to-end scenario tests including all four challenge scenarios plus edge cases (empty commands, surrounded by obstacles, backward movement, single-cell grid, multiple data collections).
