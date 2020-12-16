from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce, cache
from math import ceil
from collections import namedtuple
from multiprocessing import Pool

Adapter = namedtuple('Adapter', ['name', 'joltage', 'diff'])

allowed_jolt_diff_range = {*range(1, 4)}

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

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


def get_diffs(sorted_joltages):
    return (
        ((n, m), m - n)
        for n, m
        in zip(
            chain([0], sorted_joltages),
            sorted_joltages
        )
    )


def get_one_step_intervals(sorted_diffs):
  intervals = [[]]
  for (_, m), diff in sorted_diffs:
    if diff == 1:
      intervals[-1].append(m)
    else:
      intervals.append([])
  return intervals


def get_path_to_end(current, end, steps):
    if current == end:
        return 1
    else:
        valid_next_steps = tuple(
            step
            for step
            in steps
            if current - step in allowed_jolt_diff_range
        )
        if len(valid_next_steps) == 0:
            return 0
        else:
            return sum(
                get_path_to_end(
                    next_step,
                    end,
                    tuple(
                        filter(
                            lambda step: step != next_step,
                            steps
                        )
                    )
                )
                for next_step
                in valid_next_steps
            )


def add_num_paths(one_step_intervals):
  return (
      (
          interval,
          get_path_to_end(
              max(interval),
              min(interval) - 1,
              list(reversed(interval)) + [min(interval) - 1]
          )
      )
      for interval
      in one_step_intervals
      if len(interval) > 0
  )


def get_num_paths(with_num_paths):
  return reduce(
      lambda acc, one_step_interval: acc * one_step_interval[-1],
      with_num_paths,
      1
  )

sorted_joltages = list(sorted(joltages))

total_adapter_chain = get_total_adapter_chain(
    sorted_joltages
)

pp(sorted_joltages)

diffs = list(get_diffs(sorted_joltages))
pp(diffs)

one_step_intervals = list(get_one_step_intervals(diffs))
pp(one_step_intervals)

with_num_paths = list(add_num_paths(one_step_intervals))
pp(with_num_paths)

num_paths = get_num_paths(with_num_paths)
pp(num_paths)


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

reversed_joltages = tuple(reversed(sorted_joltages)) + (0,)
# joltages_set = {*joltages, 0}
# max_joltage = max(joltages_set)
# rest = joltages_set - {max_joltage}
# pp((max_joltage, rest))

# num_combinations = get_path_to_end(
#     reversed_joltages[0],
#     reversed_joltages[1:]
# )

# pp(f"Puzzle 2: {num_combinations}")
