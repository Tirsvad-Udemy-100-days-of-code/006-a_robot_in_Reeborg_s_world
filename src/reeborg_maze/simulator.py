"""!
@file simulator.py
@brief Minimal offline model of Reeborg's world, used to test the solver.
"""

import json
from collections.abc import Callable
from pathlib import Path

from .constants import (
    BLOCKING_TILES,
    HEADING_COUNT,
    HEADING_STEP,
    HEADING_WALL_NAME,
    MAX_ACTIONS,
)


class SimulationError(RuntimeError):
    """!
    @brief Raised when the robot hits a wall or exceeds the action limit.
    """


class SimulatedRobot:
    """!
    @brief A robot on a walled grid that mimics Reeborg's built-in API.
    """

    def __init__(self, world: dict, x: int | None = None, y: int | None = None,
                 heading: int | None = None,
                 on_action: Callable[["SimulatedRobot"], None] | None = None) -> None:
        """!
        @param world Parsed Reeborg world JSON.
        @param x Start column; defaults to the robot in the file.
        @param y Start row; defaults to the robot in the file.
        @param heading Start heading (0=E, 1=N, 2=W, 3=S); defaults to the file's.
        @param on_action Optional callback invoked after every turn or move.
        """
        start = world["robots"][0]
        self.cols: int = world["cols"]
        self.rows: int = world["rows"]
        self.x: int = start["x"] if x is None else x
        self.y: int = start["y"] if y is None else y
        self.heading: int = start["_orientation"] if heading is None else heading
        self.walls: dict[str, list[str]] = world.get("walls", {})
        self.tiles: dict[str, list[str]] = world.get("tiles", {})
        goal = world["goal"]["position"]
        self.goal: tuple[int, int] = (goal["x"], goal["y"])
        self.actions: int = 0
        self.on_action = on_action

    def _tick(self) -> None:
        self.actions += 1
        if self.actions > MAX_ACTIONS:
            raise SimulationError("Action limit exceeded: probable infinite loop")

    def _notify(self) -> None:
        if self.on_action is not None:
            self.on_action(self)

    def wall_between(self, x: int, y: int, heading: int) -> bool:
        """!
        @brief Whether a wall or the world edge blocks leaving (x, y) toward heading.
        """
        dx, dy = HEADING_STEP[heading]
        nx, ny = x + dx, y + dy
        if not (1 <= nx <= self.cols and 1 <= ny <= self.rows):
            return True
        name = HEADING_WALL_NAME[heading]
        opposite = HEADING_WALL_NAME[(heading + 2) % HEADING_COUNT]
        return (
            name in self.walls.get(f"{x},{y}", [])
            or opposite in self.walls.get(f"{nx},{ny}", [])
        )

    def _clear(self, heading: int) -> bool:
        if self.wall_between(self.x, self.y, heading):
            return False
        dx, dy = HEADING_STEP[heading]
        target = self.tiles.get(f"{self.x + dx},{self.y + dy}", [])
        return not BLOCKING_TILES.intersection(target)

    def front_is_clear(self) -> bool:
        """!@brief True if the robot can move forward."""
        return self._clear(self.heading)

    def right_is_clear(self) -> bool:
        """!@brief True if the robot could move after turning right."""
        return self._clear((self.heading - 1) % HEADING_COUNT)

    def at_goal(self) -> bool:
        """!@brief True if the robot stands on the goal."""
        return (self.x, self.y) == self.goal

    def turn_left(self) -> None:
        """!@brief Rotate 90 degrees counter-clockwise."""
        self._tick()
        self.heading = (self.heading + 1) % HEADING_COUNT
        self._notify()

    def move(self) -> None:
        """!
        @brief Move one cell forward.
        @throws SimulationError if blocked.
        """
        self._tick()
        if not self.front_is_clear():
            raise SimulationError(f"Blocked at ({self.x}, {self.y}) heading {self.heading}")
        dx, dy = HEADING_STEP[self.heading]
        self.x += dx
        self.y += dy
        self._notify()


def load_world(path: str | Path) -> dict:
    """!
    @brief Read a Reeborg world JSON file.
    @param path File to read.
    @return Parsed world dictionary.
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))
