"""!
@file constants.py
@brief Constants shared by the maze solver and the local world simulator.
"""

## Compass headings in Reeborg's world, counter-clockwise: east, north, west, south.
EAST: int = 0
NORTH: int = 1
WEST: int = 2
SOUTH: int = 3

## Number of headings; used for modular turning.
HEADING_COUNT: int = 4

## Unit step (dx, dy) for each heading. Reeborg's y axis grows northwards.
HEADING_STEP: dict[int, tuple[int, int]] = {
    EAST: (1, 0),
    NORTH: (0, 1),
    WEST: (-1, 0),
    SOUTH: (0, -1),
}

## Wall names used in Reeborg world JSON files, keyed by heading.
HEADING_WALL_NAME: dict[int, str] = {
    EAST: "east",
    NORTH: "north",
    WEST: "west",
    SOUTH: "south",
}

## Tiles the robot cannot enter.
BLOCKING_TILES: frozenset[str] = frozenset({"mud", "water"})

## Safety limit on simulator actions, so a bad algorithm cannot loop forever.
MAX_ACTIONS: int = 10_000

## Characters that show the robot's heading in the text visualisation.
HEADING_SYMBOL: dict[int, str] = {
    EAST: ">",
    NORTH: "^",
    WEST: "<",
    SOUTH: "v",
}

## Default pause between animation frames, in seconds.
DEFAULT_FRAME_DELAY: float = 0.15

## ANSI escape sequences: clear the screen, and move the cursor to the top left.
ANSI_CLEAR: str = "\x1b[2J"
ANSI_HOME: str = "\x1b[H"
