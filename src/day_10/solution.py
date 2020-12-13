from pathlib import Path
from pprint import pprint as pp
from functools import reduce

allowed_jolt_diff_range = range(1, 4)

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

joltages = [
    int(line.strip())
    for line
    in file_handler.readlines()
]

outlet_joltage = 0
device_joltage = max(joltages) + 3

sorted_joltages = [
    *sorted(joltages),
    device_joltage
]

connections = [
    (
        sorted_joltages[i-1] if i > 0 else 0,
        joltage
    )
    for i, joltage
    in enumerate(sorted_joltages)
]

diffs = [
    y - x for x, y in connections
]

diff_counts = [
    (
        allowed_diff,
        sum(
            1 if diff == allowed_diff else 0
            for diff in diffs
        )
    )
    for allowed_diff
    in allowed_jolt_diff_range
]

product_of_1_and_3_diff_counts = diff_counts[0][1] * diff_counts[2][1]

pp(f"Puzzle 1: {product_of_1_and_3_diff_counts}")
