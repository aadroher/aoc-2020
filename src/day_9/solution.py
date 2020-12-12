from pathlib import Path
from pprint import pprint as pp
from itertools import product
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

indexes = list(range(0, len(numbers) + 1))
pp(indexes)

def is_valid(index, number):
    start = index - PREFIX_LENGTH
    end = index
    prefix = numbers[start:end]
    return any(
        x + y == number
        for x, y in product(prefix, prefix)
    )


def is_weakness(start, end, first_invalid_number):
    return sum()


first_invalid_number = next(
    number
    for i, number
    in enumerate(numbers)
    if i >= PREFIX_LENGTH and not is_valid(i, number)
)

intervals = (
    (start, end)
    for start, end
    in product(indexes, indexes)
    if start + 3 < end
)

encryption_weakness = next(
    numbers[start] + numbers[end - 1]
    for start, end
    in intervals
    if sum(numbers[start:end]) == first_invalid_number
)

pp(f"Puzzle: {first_invalid_number}")

pp(f"Puzzle: {encryption_weakness}")
