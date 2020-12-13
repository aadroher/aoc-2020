from pathlib import Path
from pprint import pprint as pp
from itertools import chain
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


def get_connections(adapter_joltages):
    with_initial_value = chain(
        [outlet_joltage],
        adapter_joltages
    )
    with_end_value = chain(
        adapter_joltages,
        [device_joltage]
    )
    return zip(
        with_initial_value,
        with_end_value
    )


def is_valid_chain(connections):
    return all(
        y - x in allowed_jolt_diff_range
        for x, y in connections
    )


sorted_joltages = sorted(joltages)

all_adapters_diffs = [
    y - x for x, y
    in get_connections(
        sorted_joltages
    )
]

all_adapters_diff_counts = [
    (
        allowed_diff,
        sum(
            1 if diff == allowed_diff else 0
            for diff in all_adapters_diffs
        )
    )
    for allowed_diff
    in allowed_jolt_diff_range
]

product_of_1_and_3_diff_counts = \
    all_adapters_diff_counts[0][1] * all_adapters_diff_counts[2][1]

pp(f"Puzzle 1: {product_of_1_and_3_diff_counts}")
