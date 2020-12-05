from pathlib import Path
from pprint import pprint as pp

RIGHT_STEP = 3
DOWN_STEP = 1

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')
map_rows = [
    file_line.strip()
    for file_line in
    list(file_handler.readlines())
]
row_length = len(map_rows[0])


def get_tree_count(index, map_row):
    cell_content = map_row[(index * RIGHT_STEP) % row_length]
    return 1 if cell_content == '#' else 0


num_trees = sum(
    get_tree_count(index, map_row)
    for index, map_row in enumerate(map_rows)
)

pp(f"Puzzle 1: {num_trees}")
