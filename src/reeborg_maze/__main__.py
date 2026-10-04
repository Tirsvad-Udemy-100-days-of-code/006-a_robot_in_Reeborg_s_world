"""!
@file __main__.py
@brief Command line entry point: python -m reeborg_maze WORLD.json
"""

import argparse

from .constants import DEFAULT_FRAME_DELAY
from .maze_solver import solve_maze
from .simulator import SimulatedRobot, load_world
from .visualizer import make_frame_printer, render


def main() -> None:
    """!
    @brief Solve a world file offline and report the final position.
    """
    parser = argparse.ArgumentParser(description="Solve a Reeborg maze offline.")
    parser.add_argument("world", help="path to a Reeborg world JSON file")
    parser.add_argument("--animate", action="store_true",
                        help="show the robot moving in the terminal")
    parser.add_argument("--delay", type=float, default=DEFAULT_FRAME_DELAY,
                        help="seconds between animation frames (default: %(default)s)")
    parser.add_argument("--start", nargs=3, type=int, metavar=("X", "Y", "HEADING"),
                        help="override start; heading 0=E 1=N 2=W 3=S")
    args = parser.parse_args()

    world = load_world(args.world)
    x, y, heading = args.start if args.start else (None, None, None)
    robot = SimulatedRobot(world, x, y, heading)
    if args.animate:
        robot.on_action = make_frame_printer(args.delay)
        robot.on_action(robot)
    solve_maze(robot)
    if not args.animate:
        print(render(robot))
    print(f"Goal reached at ({robot.x}, {robot.y}) in {robot.actions} actions.")


if __name__ == "__main__":
    main()
