from pathlib import Path
from pprint import pprint as pp
from functools import reduce
from collections import namedtuple

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

file_lines = [
    line for line
    in file_handler.readlines()
]


def parse_content(contained_bag_str):
    number, *colour_tokens = contained_bag_str.strip().split(' ')[:3]
    return {
        'number': int(number),
        'colour': "_".join(colour_tokens)
    }


def parse_rule(rule_str):
    container_statement, content_statement = (
        token.strip()
        for token
        in rule_str.split('contain')
    )
    container_colour = "_".join(container_statement.split()[:2])
    contents = [
        parse_content(contained_bag_str)
        for contained_bag_str
        in content_statement.split(',')
    ] if "no other" not in content_statement else []
    return {
        'colour': container_colour,
        'contents': contents
    }


def get_membership_edges(rules):
    return reduce(
        lambda membership_set, rule:  {
            *membership_set,
            *{
                (content['colour'], rule['colour'])
                for content
                in rule['contents']
            }
        }, rules, set()
    )


def get_membership_paths(path_prefixes, edge_set):
    path_extensions = reduce(
        lambda new_path_prefixes, path_prefix: {
            *new_path_prefixes,
            *{
                (*path_prefix, parent)
                for child, parent
                in edge_set
                if path_prefix[-1] == child
            }
        },
        path_prefixes,
        {}
    )
    if len(path_extensions) == 0:
        return path_extensions
    else:
        return {
            *path_extensions,
            *get_membership_paths(path_extensions, edge_set)
        }


def count_child_bags(colour, rules):
    rule = next(
        rule for rule in rules if rule['colour'] == colour
    )
    return sum(
        content['number'] + (
            content['number'] * count_child_bags(content['colour'], rules)
        )
        for content in rule['contents']
    )


rules = [
    parse_rule(rule_str.strip())
    for rule_str
    in file_lines
]

membership_edges = get_membership_edges(rules)
paths = get_membership_paths({('shiny_gold',)}, membership_edges)
end_colours = {path[-1] for path in paths}
num_end_colours = len(end_colours)

pp(f"Puzzle 1: {num_end_colours}")

child_bags = count_child_bags(colour='shiny_gold', rules=rules)

pp(f"Puzzle 2: {child_bags}")
