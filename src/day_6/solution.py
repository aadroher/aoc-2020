from pathlib import Path
from pprint import pprint as pp
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')


file_lines = [
    line for line
    in file_handler.readlines()
]

groups_answer_sets = [
    tuple(
        {question for question in questions}
        for questions in group_data.split('\n')
    )
    for group_data
    in "".join(file_lines).strip().split("\n\n")
]

group_answer_unions = [
    reduce(
        lambda group_answer_union, group_answer_set: group_answer_union | group_answer_set,
        group_answer_sets
    )
    for group_answer_sets
    in groups_answer_sets
]

union_sizes_sum = sum(
    len(group_answer_union)
    for group_answer_union
    in group_answer_unions
)

pp(f"Puzzle 1: {union_sizes_sum}")

group_answer_intersections = [
    reduce(
        lambda group_answer_intersection, group_answer_set: group_answer_intersection & group_answer_set,
        group_answer_sets
    )
    for group_answer_sets
    in groups_answer_sets
]

intersection_sizes_sum = sum(
    len(group_answer_intersection)
    for group_answer_intersection
    in group_answer_intersections
)

pp(f"Puzzle 1: {intersection_sizes_sum}")
