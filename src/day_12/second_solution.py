from pathlib import Path
from pprint import pprint as pp
from functools import reduce
from math import sin, cos, radians
from enum import Enum


current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

instruction_strs = [
    line.strip()
    for line
    in file_handler.readlines()
]

CARDINALITIES = ('E', 'S', 'W', 'N')

TRANSLATIONS = dict(
    zip(
        CARDINALITIES,
        ((1, 0), (0, -1), (-1, 0), (0, 1))
    )
)


def parse_instructions(instruction_strs):
    return [
        (instruction_str[:1], int(instruction_str[1:]))
        for instruction_str in instruction_strs
    ]


def translate_waypoint(state, instruction):
    position, waypoint = state
    v, w = waypoint

    operation, distance = instruction
    dv, dw = TRANSLATIONS[operation]

    new_waypoint = (
        v + dv * distance,
        w + dw * distance
    )

    return (
        position,
        new_waypoint
    )


def rotate_waypoint(state, instruction):
    position, waypoint = state
    x, y = position
    v, w = waypoint

    operation, angle = instruction
    turn_direction = 1 if operation == 'L' else -1
    signed_angle = turn_direction * angle

    new_r = x + (
        (v - x) * cos(radians(signed_angle)) -
        (w - y) * sin(radians(signed_angle))
    )
    new_w = y + (
        (v - x) * sin(radians(signed_angle)) +
        (w - y) * cos(radians(signed_angle))
    )

    new_waypoint = (int(new_r), int(new_w))

    return (
        position,
        new_waypoint
    )


def move_ship(state, instruction):
    position, waypoint = state
    x, y = position
    v, w = waypoint
    _, distance = instruction

    dx = (v - x) * distance
    dy = (w - y) * distance

    new_position = ((x + dx), (y + dy))
    new_waypoint = ((v + dx), (w + dy))

    return (
        new_position,
        new_waypoint
    )


def apply_instruction(state, instruction):
    operation, _ = instruction
    if operation in TRANSLATIONS.keys():
        new_state = translate_waypoint(state, instruction)
        return new_state
    elif operation in {'L', 'R'}:
        new_state = rotate_waypoint(state, instruction)
        return new_state
    else:
        new_state = move_ship(state, instruction)
        return new_state


def run(initial_state, instructions):
    return reduce(
        apply_instruction,
        instructions,
        initial_state
    )


def get_manhattan_distance(position):
    x, y = position
    return abs(x) + abs(y)


initial_state = (
    (0, 0),
    (10, 1)
)
instructions = parse_instructions(instruction_strs)
final_state = run(
    initial_state,
    instructions
)

final_position, _ = final_state

manhattan_distance = get_manhattan_distance(final_position)

pp(f"Puzzle 2: {manhattan_distance}")
