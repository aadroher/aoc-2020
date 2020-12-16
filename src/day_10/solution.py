from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce
from math import ceil
from collections import namedtuple

Adapter = namedtuple('Adapter', ['name', 'joltage', 'diff'])

allowed_jolt_diff_range = range(1, 4)

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

total_adapter_chain = get_total_adapter_chain(
    sorted_joltages
)

pp(sorted_joltages)

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


def valid_steps(combination):
    return all(
        combination[i + 1] - joltage in {1, 2, 3}
        if i + 1 < len(combination) else True
        for i, joltage
        in enumerate(combination)
    )

def valid_limits(combination):
  bottom = combination[0]
  top = combination[-1]
  return bottom in {1, 2, 3} and top == max(joltages) 


def is_valid_combination(combination):
    return valid_limits(combination) and valid_steps(combination)

num_joltages = len(joltages)
total_combinations = [
    combination
    for r in range(
        ceil(num_joltages / 3),
        num_joltages + 1
    )
    for combination
    in combinations(sorted_joltages, r)
    if is_valid_combination(combination)
]

pp(len(total_combinations))


# connections = list(get_connections(sorted_joltages))

# pp(connections)

# one_step_intervals = get_one_step_intervals(connections)

# interval_subpaths = list(
#     map(
#         get_subpaths,
#         one_step_intervals
#     )
# )

# total_combinations = reduce(
#     lambda acc, subpaths:
#         len(subpaths[1]) * acc,
#     interval_subpaths,
#     1
# )

# pp(total_combinations)
