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
            lambda result, parent_colour: (
                result +
                get_parent_colours(parent_colour, child_to_parent_colours)
            ),
            parent_colours,
            0
        )
    else:
        return 1


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
  result = {}
  for path_prefix in path_prefixes:
    next_step = {
        (*path_prefix, parent)
        for child, parent
        in edge_set
        if path_prefix[-1] == child
    }
    result = {
        *result,
        *next_step
    }
  if len(result) == 0:
    return result
  else:
    return {
        *result,
        *get_membership_paths(result, edge_set)
    }

rules = [
    parse_rule(rule_str.strip())
    for rule_str
    in file_lines
]

# child_to_parent_colours = get_child_to_parent_colours(rules)

# pp(rules)

membership_edges = get_membership_edges(rules)
paths = get_membership_paths({('shiny_gold',)}, membership_edges)
end_colours = {path[-1] for path in paths}
pp(paths)
pp(end_colours)
pp(len(end_colours))
# pp(get_parent_colours(
#     'shiny_gold',
#     child_to_parent_colours
# ))
