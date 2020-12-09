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


def add_rule(result, rule):
  parent_colour = rule['colour']
  for child in rule['contents']:
    child_colour = child['colour']
    parent_colour_set = result.get(child_colour, set())
    new_parent_colour_set = {*parent_colour_set, parent_colour}
    result[child_colour] = new_parent_colour_set
  return result


def get_parents_by_child(rules):
  return reduce(
      add_rule,
      rules,
      {}
  )


rules = [
    parse_rule(rule_str.strip())
    for rule_str
    in file_lines
]

parents_by_child = get_parents_by_child(rules)


pp(parents_by_child)
