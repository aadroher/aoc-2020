from pathlib import Path
from pprint import pprint as pp
from functools import reduce

VELOCITY_VECTORS = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')
map_rows = [
    file_line.strip()
    for file_line in
    file_handler.readlines()
]
row_length = len(map_rows[0])


def get_significant_rows(down_step):
  return (
      row
      for index, row in enumerate(map_rows)
      if index % down_step == 0
  )


def count_next_tree(right_step, row_index, row_contents):
    cell_content = row_contents[(row_index * right_step) % row_length]
    return 1 if cell_content == '#' else 0


def count_trees(right_step, rows):
  return sum(
      count_next_tree(right_step, index, row)
      for index, row in enumerate(rows)
  )


solutions = [
    {
        'velocity_vector': velocity_vector,
        'tree_count': count_trees(
            right_step=velocity_vector[0],
            rows=get_significant_rows(down_step=velocity_vector[1])
        )
    } for velocity_vector in VELOCITY_VECTORS
]


pp(solutions)

puzzle_1_solution = next(
    solution['tree_count']
    for solution in solutions
    if solution['velocity_vector'] == (3, 1)
)

pp(f"Puzzle 1: {puzzle_1_solution}")

puzzle_2_solution = reduce(
    lambda x, y: x * y,
    (
        solution['tree_count']
        for solution in solutions
    )
)

pp(f"Puzzle 2: {puzzle_2_solution}")
