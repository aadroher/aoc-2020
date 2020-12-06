from pathlib import Path
from pprint import pprint as pp
from functools import reduce
import re

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')


def is_valid_height(value_str):
    amount = value_str[:-2]
    unit = value_str[-2:]

    is_valid_metric = (
        unit == 'cm' and int(amount) in range(150, 193 + 1)
    )
    is_valid_imperial = (
        unit == 'in' and int(amount) in range(59, 76 + 1)
    )

    return is_valid_metric or is_valid_imperial


FIELDS = [
    {
        'name': 'byr',
        'is_valid': lambda value: int(value) in range(1920, 2002 + 1)
    },
    {
        'name': 'iyr',
        'is_valid': lambda value: int(value) in range(2010, 2020 + 1)
    },
    {
        'name': 'eyr',
        'is_valid': lambda value: int(value) in range(2020, 2030 + 1)
    },
    {
        'name': 'hgt',
        'is_valid': is_valid_height
    },
    {
        'name': 'hcl',
        'is_valid': lambda value: bool(re.match('^#[0-9a-f]{6}$', value))
    },
    {
        'name': 'ecl',
        'is_valid': lambda value: value in {
            'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'
        }
    },
    {
        'name': 'pid',
        'is_valid': lambda value: bool(re.match('^[0-9]{9}$', value))
    }
]


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


def has_required_fields(document):
    required_field_names = {
        field['name']
        for field in FIELDS
    }
    return all(
        required_field_name in document
        for required_field_name
        in required_field_names
    )


def has_valid_field_values(document):
  return all(
      next(
          field['is_valid']
          for field in FIELDS
          if field_name == field['name']
      )(value)
      for field_name, value in document.items()
      if field_name != 'cid'
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

num_documents_with_required_fields = sum(
    1 if has_required_fields(document) else 0
    for document in documents
)


pp(f"Puzzle 1: {num_documents_with_required_fields}")

num_valid_documents = sum(
    1 if (
        has_required_fields(document)
        and has_valid_field_values(document)
    ) else 0
    for document in documents
)

pp(f"Puzzle 2: {num_valid_documents}")
