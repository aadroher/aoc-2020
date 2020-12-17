from pathlib import Path
from pprint import pprint as pp
from itertools import product
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"test_0.txt", 'r')

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
            if get_num_adjacent_states(OCCUPIED_SEAT, pos, seat_map) == 0 else EMPTY_SEAT
    elif current_state == OCCUPIED_SEAT:
        return EMPTY_SEAT \
            if get_num_adjacent_states(OCCUPIED_SEAT, pos, seat_map) >= 4 else OCCUPIED_SEAT
    else:
        return current_state


def next_tick(seat_map):
    return tuple(
        tuple(
            next_state((i, j), seat_map)
            for j in range(len(seat_map[i]))
        ) for i in range(len(seat_map))
    )


pp(seat_map)
pp(
    next_tick(seat_map)
)

translations_vector = (-1, 0, 1)
adjacency_translations = (*product(translations_vector, translations_vector), )
pp(adjacency_translations)
