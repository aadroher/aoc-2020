from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce
from math import ceil
from collections import namedtuple

Connection = namedtuple('Connection', ['input', 'output', 'diff'])

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
        Connection(
            input=x,
            output=y,
            diff=y-x
        )
        for x, y
        in zip(
            with_initial_value,
            with_end_value
        )
    ]

def get_one_step_intervals(connections):
  dividers = [
    i for i, connection
    in enumerate(connections)
    if connection.diff == 3
  ]

  pp(len(dividers))

  intervals = []
  for i, divider in enumerate(dividers):
    next_index = i + 1
    if next_index < len(dividers):
      intervals += [
        connections[divider + 1:dividers[next_index]]
      ] 
  return intervals
  
  # return [
  #   connections[divider:dividers[i + 1]]
  #   for i, divider 
  #   in enumerate(dividers)
  #   if i + 1 < len(dividers) 
  # ]

def get_subpaths(connections):
    pass


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
pp(all_adapters_diffs)

ones_interval_lengths = [
    len(ones)
    for ones
    in "".join(
        map(
            str,
            all_adapters_diffs
        )
    ).split('3')
    if len(ones) > 0
]

pp(get_one_step_intervals(connections))

pp(ones_interval_lengths)

# branches = [
#     sum(
#         sum(
#             1 for combination
#             in combinations(
#                 range(n + 1),
#                 r
#             )
#         ) for r
#         in range(min(n, 3) + 1)
#     )
#     for n in ones_interval_lengths
# ]

# pp(branches)

# num_combinations = reduce(
#     lambda n, m: n * m,
#     branches
# )

# pp(f"Puzzle 2: {num_allowed_combinations}")
