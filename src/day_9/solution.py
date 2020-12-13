from pathlib import Path
from pprint import pprint as pp
from itertools import product, combinations
from functools import reduce, cache
from collections import namedtuple

PREFIX_LENGTH = 25

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

numbers = [
    int(line.strip())
    for line
    in file_handler.readlines()
]

indexes = range(0, len(numbers))


def is_valid(index, number):
    start = index - PREFIX_LENGTH
    end = index
    prefix = numbers[start:end]
    return any(
        x + y == number
        for x, y in product(prefix, prefix)
    )


first_invalid_number = next(
    number
    for i, number
    in enumerate(numbers)
    if i >= PREFIX_LENGTH and (not is_valid(i, number))
)

intervals = (
    numbers[start: end + 1]
    for start, end
    in combinations(indexes, 2)
    if start + 3 < end
)

encryption_weakness_range = next(
    interval
    for interval in intervals
    if sum(interval) == first_invalid_number
)

encryption_weakness = \
    min(encryption_weakness_range) + max(encryption_weakness_range)

pp(f"Puzzle 1: {first_invalid_number}")

pp(f"Puzzle 2: {encryption_weakness}")
