from pathlib import Path
from pprint import pprint as pp
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

MANDATORY_FIELD_NAMES = {
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid'
}


def get_field_dictionary(field_str):
  field, value = field_str.split(':')
  return {field: value}


def get_document(document_file_line):
  return reduce(
      lambda record, field_str: {
          **record,
          **get_field_dictionary(field_str)
      },
      document_file_line.split(),
      {}
  )


def is_valid(document):
  return all(
      mandatory_field_name in document
      for mandatory_field_name
      in MANDATORY_FIELD_NAMES
  )


file_lines = [
    line for line
    in file_handler.readlines()
]

document_file_lines = "".join(file_lines).split("\n\n")

documents = [
    get_document(document_file_line)
    for document_file_line
    in document_file_lines
]

num_valid_documents = sum(
    1 if is_valid(document) else 0
    for document in documents
)


pp(f"Puzzle 1: {num_valid_documents}")
