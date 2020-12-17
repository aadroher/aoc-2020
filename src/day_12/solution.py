from pathlib import Path
from pprint import pprint as pp
from functools import reduce
from enum import Enum


current_dir = Path(__file__).parent
file_handler = open(current_dir/"test_0.txt", 'r')

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


def direction_to_move_operation(direction):
    return next(
        operation
        for operation, degrees
        in zip(
            TRANSLATIONS.keys(),
            range(0, 360, 90)
        )
        if direction == degrees
    )


def move(state, instruction):
    direction, position = state
    x, y = position

    operation, argument = instruction
    dx, dy = TRANSLATIONS[operation]

    new_position = (
        x + dx * argument,
        y + dy * argument
    )

    return (
        direction,
        new_position
    )


def turn(state, instruction):
    direction, position = state
    operation, argument = instruction
    turn_direction = 1 if operation == 'R' else -1

    new_direction = (direction + turn_direction * argument) % 360

    return (
        new_direction,
        position
    )


def forward(state, instruction):
    direction, _ = state
    _, argument = instruction
    move_instruction = (
        direction_to_move_operation(direction),
        argument
    )
    return move(state, move_instruction)


def parse_instructions(instruction_strs):
    return [
        (instruction_str[:1], int(instruction_str[1:]))
        for instruction_str in instruction_strs
    ]


def apply_instruction(state, instruction):
    operation, _ = instruction
    if operation in TRANSLATIONS.keys():
        new_state = move(state, instruction)
        pp(new_state)
        return new_state
    elif operation in {'L', 'R'}:
        new_state = turn(state, instruction)
        pp(new_state)
        return new_state
    else:
        new_state = forward(state, instruction)
        pp(new_state)
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


pp(instruction_strs)
pp(parse_instructions(instruction_strs))

instructions = parse_instructions(instruction_strs)
final_state = run(
    (0, (0, 0)),
    instructions
)
_, final_position = final_state

manhattan_distance = get_manhattan_distance(final_position)

pp(f"Puzzle 1: {manhattan_distance}")
