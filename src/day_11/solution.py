from pathlib import Path
from pprint import pprint as pp
from itertools import product
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'
FLOOR = '.'

seat_map = tuple(
    tuple(line.strip())
    for line
    in file_handler.readlines()
)


def is_of_state(states, pos, seat_map):
    x, y = pos
    return x in range(len(seat_map)) \
        and y in range(len(seat_map[x])) \
        and seat_map[x][y] in states


def get_num_adjacent_states(states, pos, seat_map):
    x, y = pos
    translations_vector = (-1, 0, 1)
    adjacency_translations = (
        translation for translation
        in product(translations_vector, translations_vector)
        if translation != (0, 0)
    )
    return sum(
        1 if is_of_state(states, (x + dx, y + dy), seat_map) else 0
        for dx, dy in adjacency_translations
    )


def next_state(pos, seat_map):
    x, y = pos
    current_state = seat_map[x][y]
    if current_state == EMPTY_SEAT:
        return OCCUPIED_SEAT \
            if get_num_adjacent_states({OCCUPIED_SEAT}, pos, seat_map) == 0 else EMPTY_SEAT
    elif current_state == OCCUPIED_SEAT:
        return EMPTY_SEAT \
            if get_num_adjacent_states({OCCUPIED_SEAT}, pos, seat_map) >= 4 else OCCUPIED_SEAT
    else:
        return current_state


def next_tick(seat_map):
    return tuple(
        tuple(
            next_state((i, j), seat_map)
            for j in range(len(seat_map[i]))
        ) for i in range(len(seat_map))
    )


def get_fixed_point(seat_map):
    next_seat_map = next_tick(seat_map)
    if seat_map == next_seat_map:
        return seat_map
    else:
        return get_fixed_point(next_seat_map)


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

fixed_point = get_fixed_point(seat_map)
num_occupied_seats = count_seat_state_instances({OCCUPIED_SEAT}, fixed_point)

pp(f"Puzzle 1: {num_occupied_seats}")
