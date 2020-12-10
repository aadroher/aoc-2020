from pathlib import Path
from pprint import pprint as pp
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

file_lines = [
    line for line
    in file_handler.readlines()
]


def parse_content(contained_bag_str):
    number, *colour_tokens = contained_bag_str.strip().split(' ')[:3]
    return {
        'number': number,
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
    ]
    return {
        'colour': container_colour,
        'contents': contents
    }


def update_parent_set(parent_colour, child_to_parent_colours, child_colour):
    parent_colour_set = child_to_parent_colours.get(child_colour, set())
    return {
        **child_to_parent_colours,
        child_colour: {*parent_colour_set, parent_colour}
    }


def add_rule(child_to_parent_colours, rule):
    parent_colour = rule['colour']
    return reduce(
        lambda updated_child_to_parent_colours, child: update_parent_set(
            parent_colour,
            updated_child_to_parent_colours,
            child['colour']
        ),
        rule['contents'],
        child_to_parent_colours
    )


def get_child_to_parent_colours(rules):
    return reduce(
        add_rule,
        rules,
        {}
    )


def get_parent_colours(child_colour, child_to_parent_colours):
    if child_colour in child_to_parent_colours:
        parent_colours = list(child_to_parent_colours[child_colour])
        return reduce(
            lambda result, parent_colour: [
                *result,
                *get_parent_colours(parent_colour, child_to_parent_colours)
            ],
            parent_colours,
            parent_colours
        )
    else:
        return ['END']


rules = [
    parse_rule(rule_str.strip())
    for rule_str
    in file_lines
]

child_to_parent_colours = get_child_to_parent_colours(rules)


pp(get_parent_colours(
    'shiny_gold',
    child_to_parent_colours
))
