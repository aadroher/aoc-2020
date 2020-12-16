from pathlib import Path
from pprint import pprint as pp
from itertools import chain, combinations, product, takewhile, islice
from functools import reduce, cache
from math import ceil
from collections import namedtuple
from multiprocessing import Pool

Adapter = namedtuple('Adapter', ['name', 'joltage', 'diff'])

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

joltages = [
    int(line.strip())
    for line
    in file_handler.readlines()
]

allowed_jolt_diffs = range(1, 4)
outlet_joltage = 0
device_joltage = max(joltages) + max(allowed_jolt_diffs)


def get_diffs(sorted_joltages):
    return [
        ((n, m), m - n)
        for n, m
        in zip(
            chain([0], sorted_joltages),
            chain(sorted_joltages, [device_joltage])
        )
    ]


def get_diff_counts(sorted_diffs):
    return [
        (
            allowed_diff,
            sum(
                1 if diff == allowed_diff else 0
                for _, diff in sorted_diffs
            )
        )
        for allowed_diff
        in allowed_jolt_diffs
    ]


def get_one_step_intervals(sorted_diffs):
    intervals = [[]]
    for (_, m), diff in sorted_diffs:
        if diff == 1:
            intervals[-1].append(m)
        else:
            intervals.append([])
    return intervals


def count_paths(current, end, steps):
    if current == end:
        return 1
    else:
        valid_next_steps = [
            step
            for step
            in steps
            if step - current in allowed_jolt_diffs
        ]
        if len(valid_next_steps) == 0:
            return 0
        else:
            return sum(
                count_paths(
                    next_step,
                    end,
                    {*steps} - {next_step}
                )
                for next_step
                in valid_next_steps
            )


def add_num_paths(one_step_intervals):
    return (
        (
            interval,
            count_paths(
                min(interval) - 1,
                max(interval),
                {min(interval) - 1} | {*interval}
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


sorted_joltages = (*sorted(joltages),)
diffs = get_diffs(sorted_joltages)
all_adapters_diff_counts = get_diff_counts(diffs)
product_of_1_and_3_diff_counts = \
    all_adapters_diff_counts[0][1] * all_adapters_diff_counts[2][1]

pp(f"Puzzle 1: {product_of_1_and_3_diff_counts}")

one_step_intervals = get_one_step_intervals(diffs)
with_num_paths = add_num_paths(one_step_intervals)
num_paths = get_num_paths(with_num_paths)

pp(f"Puzzle 2: {num_paths}")
