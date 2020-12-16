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


def get_num_adjacent_states(state, pos, seat_map):
  x, y = pos
  translations_vector = (-1, 0, 1)
  adjacency_translations = (
      *product(translations_vector, translations_vector),
  )
  return sum(

  )


def next_state(pos, seat_map):
  x, y = pos


def next_tick(seat_map):
  pass


pp(seat_map)

translations_vector = (-1, 0, 1)
adjacency_translations = (*product(translations_vector, translations_vector), )
pp(adjacency_translations)
