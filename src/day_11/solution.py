from pathlib import Path
from pprint import pprint as pp
from itertools import product
from functools import reduce, cache

current_dir = Path(__file__).parent
file_handler = open(current_dir/"test_0.txt", 'r')

EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'
FLOOR = '.'

TRANSLATIONS_VECTOR = (-1, 0, 1)
ADJACENCY_TRANSLATIONS = [
    translation for translation
    in product(TRANSLATIONS_VECTOR, TRANSLATIONS_VECTOR)
    if translation != (0, 0)
]

seat_map = tuple(
    tuple(line.strip())
    for line
    in file_handler.readlines()
)


def get_cell_state(pos, seat_map):
    x, y = pos
    if y in range(len(seat_map)) and x in range(len(seat_map[y])):
        return seat_map[y][x]
    else:
        return None


def is_of_state(states, pos, seat_map):
    return get_cell_state(pos, seat_map) in states


def get_num_adjacent_states(states, pos, seat_map):
    x, y = pos
    return sum(
        1 if is_of_state(states, (x + dx, y + dy), seat_map) else 0
        for dx, dy in ADJACENCY_TRANSLATIONS
    )


def get_visible_state(pos, direction, seat_map):
    x, y = pos
    dx, dy = direction
    max_distance = max(
        len(seat_map),
        len(seat_map[0])
    )
    return next(
        get_cell_state((x + dx * n, y + dy * n), seat_map)
        for n in range(1, max_distance)
        if get_cell_state((x + dx * n, y + dy * n), seat_map) not in {FLOOR}
    )


def get_num_visible_states(states, pos, seat_map):
    return sum(
        1 if get_visible_state(pos, direction, seat_map) in states else 0
        for direction in ADJACENCY_TRANSLATIONS
    )


def get_first_puzzle_next_cell_state(pos, seat_map):
    current_state = get_cell_state(pos, seat_map)
    if current_state == EMPTY_SEAT:
        return OCCUPIED_SEAT \
            if get_num_adjacent_states({OCCUPIED_SEAT}, pos, seat_map) == 0 else EMPTY_SEAT
    elif current_state == OCCUPIED_SEAT:
        return EMPTY_SEAT \
            if get_num_adjacent_states({OCCUPIED_SEAT}, pos, seat_map) >= 4 else OCCUPIED_SEAT
    else:
        return current_state


def get_second_puzzle_next_cell_state(pos, seat_map):
    current_state = get_cell_state(pos, seat_map)
    if current_state == EMPTY_SEAT:
        return OCCUPIED_SEAT \
            if get_num_visible_states({OCCUPIED_SEAT}, pos, seat_map) == 0 else EMPTY_SEAT
    elif current_state == OCCUPIED_SEAT:
        return EMPTY_SEAT \
            if get_num_visible_states({OCCUPIED_SEAT}, pos, seat_map) >= 5 else OCCUPIED_SEAT
    else:
        return current_state


def next_tick(get_next_cell_state, seat_map):
    return tuple(
        tuple(
            get_next_cell_state((x, y), seat_map)
            for x in range(len(seat_map[y]))
        ) for y in range(len(seat_map))
    )


def get_fixed_point(get_next_cell_state, seat_map):
    next_seat_map = next_tick(get_next_cell_state, seat_map)
    if seat_map == next_seat_map:
        return seat_map
    else:
        return get_fixed_point(get_next_cell_state, next_seat_map)


def render_string(seat_map):
    return "\n".join(
        (
            "".join(row)
            for row in seat_map
        )
    )


def count_seat_state_instances(state, seat_map):
    return sum(
        cell in state
        for row in seat_map
        for cell in row
    )


first_puzzle_fixed_point = get_fixed_point(
    get_first_puzzle_next_cell_state, seat_map
)
first_puzzle_num_occupied_seats = count_seat_state_instances(
    {OCCUPIED_SEAT}, first_puzzle_fixed_point
)

pp(f"Puzzle 1: {first_puzzle_num_occupied_seats}")

second_puzzle_fixed_point = get_fixed_point(
    get_second_puzzle_next_cell_state, seat_map
)
second_puzzle_num_occupied_seats = count_seat_state_instances(
    {OCCUPIED_SEAT}, second_puzzle_fixed_point
)

pp(f"Puzzle 2: {second_puzzle_num_occupied_seats}")
