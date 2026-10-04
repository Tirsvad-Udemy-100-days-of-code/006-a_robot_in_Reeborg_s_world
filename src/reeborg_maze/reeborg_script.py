"""!
@file reeborg_script.py
@brief Self-contained script to paste into https://reeborg.ca (Python mode).

It uses only Reeborg's built-in functions, so it has no imports.
"""


def turn_right():
    """!
    @brief Turn clockwise by doing three left turns.
    """
    turn_left()
    turn_left()
    turn_left()


while front_is_clear():
    move()
turn_left()

while not at_goal():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()
