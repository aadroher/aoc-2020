from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce
from math import ceil
from collections import namedtuple
from multiprocessing import Pool

Adapter = namedtuple('Adapter', ['name', 'joltage', 'diff'])

allowed_jolt_diff_range = {*range(1, 4)}

current_dir = Path(__file__).parent
file_handler = open(current_dir/"test_1.txt", 'r')

joltages = [
    int(line.strip())
    for line
    in file_handler.readlines()
]

outlet_joltage = 0
device_joltage = max(joltages) + 3


def get_total_adapter_chain(sorted_joltages):
    with_initial_value = chain(
        [outlet_joltage],
        sorted_joltages
    )
    with_end_value = chain(
        sorted_joltages,
        [device_joltage]
    )
    return [
        Adapter(
            name=i,
            joltage=x,
            diff=y-x
        )
        for i, (x, y)
        in enumerate(
            zip(
                with_initial_value,
                with_end_value
            )
        )
    ]


def get_path_to_end(current, steps):
    # pp((current, steps))
    if current == 0:
        return 1
    else:
        valid_next_steps = {
            step
            for step
            in steps
            if current - step in allowed_jolt_diff_range
        }
        if len(valid_next_steps) == 0:
            return 0
        else:
            return sum(
                get_path_to_end(
                    next_step,
                    steps - {next_step},
                )
                for next_step
                in valid_next_steps
            )


sorted_joltages = list(sorted(joltages))

total_adapter_chain = get_total_adapter_chain(
    sorted_joltages
)

all_adapters_diffs = [
    connection.diff
    for connection
    in total_adapter_chain
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

# reversed_joltages = list(reversed(sorted_joltages)) + [0]
joltages_set = {*joltages, 0}
max_joltage = max(joltages_set)
rest = joltages_set - {max_joltage}
# pp((max_joltage, rest))
pp(
    get_path_to_end(
        max_joltage,
        rest
    )
)
