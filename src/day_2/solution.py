from pathlib import Path
from pprint import pprint as pp


current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')
file_lines = list(file_handler.readlines())


def get_old_rule(line):
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


def old_is_valid(rule, password):
    num_letter_occurrences = password.count(rule['letter'])
    valid_range = range(
        rule['lower_bound'],
        rule['upper_bound'] + 1
    )
    return num_letter_occurrences in valid_range


old_rule_and_passwords = [
    {
        'rule': get_old_rule(line),
        'password': get_password(line)
    }
    for line in file_lines
]

num_old_rule_valid_passwords = sum(
    1 if old_is_valid(**rule_and_password)
    else 0
    for rule_and_password
    in old_rule_and_passwords
)

pp(f"Puzze 1: {num_old_rule_valid_passwords}")


def get_new_rule(line):
    rule_str = line.split(':')[0]
    range_str, letter = rule_str.split(' ')
    i, j = [int(n) - 1 for n in range_str.split('-')]
    return {
        'indexes': (i, j),
        'letter': letter
    }


def new_is_valid(rule, password):
    i, j = rule['indexes']
    return [password[i], password[j]].count(rule['letter']) == 1


new_rule_and_passwords = [
    {
        'rule': get_new_rule(line),
        'password': get_password(line)
    }
    for line in file_lines
]

num_new_rule_valid_passwords = sum(
    1 if new_is_valid(**rule_and_password)
    else 0
    for rule_and_password
    in new_rule_and_passwords
)

pp(f"Puzze 2: {num_new_rule_valid_passwords}")
