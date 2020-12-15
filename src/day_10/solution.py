from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce
from math import ceil
from collections import namedtuple

Adapter = namedtuple('Adapter', ['name', 'input', 'output', 'diff'])

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

min_adapter_chain_length = ceil(
    (device_joltage - outlet_joltage) / max(allowed_jolt_diff_range)
)


def get_connections(adapter_joltages):
    with_initial_value = chain(
        [outlet_joltage],
        adapter_joltages
    )
    with_end_value = chain(
        adapter_joltages,
        [device_joltage]
    )
    return [
        Adapter(
            name=i,
            input=x,
            output=y,
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


def get_one_step_intervals(connections):
    intervals = [[]]
    for connection in connections:
        if connection.diff == 1:
            intervals[-1].append(connection)
        else:
            intervals.append([])
    return intervals


def is_valid_subpath(bottom, top, subpath):
    if top - bottom <= 3:
        return True
    else:
        return len(subpath) * 3 >= top - bottom


def get_subpaths(connections):
    if len(connections) > 0:
        bottom = connections[0].input
        top = connections[-1].output
        lengths = range(len(connections))
        all_length_combinations = reduce(
            lambda acc, r: acc + [
                list(combination) for combination
                in combinations(connections, r)
                if is_valid_subpath(bottom, top, combination)
            ],
            lengths,
            []
        )
        return (bottom, all_length_combinations, top)
    else:
        return (None, [[]], None)


sorted_joltages = list(sorted(joltages))

all_adapters_diffs = [
    connection.diff
    for connection
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

connections = list(get_connections(sorted_joltages))

pp(connections)

one_step_intervals = get_one_step_intervals(connections)

interval_subpaths = list(
    map(
        get_subpaths,
        one_step_intervals
    )
)

total_combinations = reduce(
    lambda acc, subpaths:
        len(subpaths[1]) * acc,
    interval_subpaths,
    1
)

pp(total_combinations)
