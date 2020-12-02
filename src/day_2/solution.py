from pathlib import Path
from pprint import pprint as pp


current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')


def get_rule(line):
    rule_str = line.split(':')[0]
    range_str, letter = rule_str.split(' ')
    lower_bound, upper_bound = [int(n) for n in range_str.split('-')]
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'letter': letter
    }


def get_password(line):
    return line.split(': ')[1].strip()


def is_valid(rule, password):
    num_letter_occurrences = password.count(rule['letter'])
    valid_range = range(
        rule['lower_bound'],
        rule['upper_bound'] + 1
    )
    return num_letter_occurrences in valid_range


rule_and_passwords = [
    {
        'rule': get_rule(line),
        'password': get_password(line)
    }
    for line in file_handler.readlines()
]

num_valid_passwords = sum(
    1 if is_valid(**rule_and_password)
    else 0
    for rule_and_password
    in rule_and_passwords
)

pp(f"Puzze 1: {num_valid_passwords}")
