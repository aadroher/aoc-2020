from pathlib import Path
from itertools import product


current_dir = Path(__file__).parent
expense_report = open(current_dir/"input.txt", 'r')

expenses = [
    int(expense_str) for expense_str in expense_report.readlines()
]

target_value = 2020

n, m = next(
    (n, m) for n, m
    in product(expenses, expenses)
    if n + m == target_value
)

pair_product = n * m

print(f"Puzzle 1: {pair_product}")

n, m, k = next(
    (n, m, k) for n, m, k
    in product(expenses, expenses, expenses)
    if n + m + k == target_value
)

triplet_product = n * m * k

print(f"Puzzle 2: {triplet_product}")
