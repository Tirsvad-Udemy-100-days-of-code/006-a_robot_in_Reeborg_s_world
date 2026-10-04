"""!
@file test_maze_solver.py
@brief Runs the solver on every provided world from all four start headings.
"""

from pathlib import Path

import pytest

from reeborg_maze import SimulatedRobot, load_world, solve_maze
from reeborg_maze.constants import BLOCKING_TILES, HEADING_COUNT

WORLDS = sorted((Path(__file__).parent / "worlds").glob("*.json"))


def free_starts() -> list[tuple[str, int, int, int]]:
    """!
    @brief Every (world, x, y, heading) where the robot can start.
    """
    starts = []
    for path in WORLDS:
        world = load_world(path)
        for x in range(1, world["cols"] + 1):
            for y in range(1, world["rows"] + 1):
                if BLOCKING_TILES.intersection(world["tiles"].get(f"{x},{y}", [])):
                    continue
                for heading in range(HEADING_COUNT):
                    starts.append((path.name, x, y, heading))
    return starts


def test_worlds_exist() -> None:
    assert WORLDS


@pytest.mark.parametrize("path", WORLDS, ids=lambda p: p.name)
def test_reaches_goal_from_file_start(path: Path) -> None:
    robot = SimulatedRobot(load_world(path))
    solve_maze(robot)
    assert robot.at_goal()


@pytest.mark.parametrize(("name", "x", "y", "heading"), free_starts())
def test_reaches_goal_from_every_free_cell_and_heading(
    name: str, x: int, y: int, heading: int
) -> None:
    robot = SimulatedRobot(load_world(Path(__file__).parent / "worlds" / name), x, y, heading)
    solve_maze(robot)
    assert robot.at_goal()
