from pathlib import Path
from pprint import pprint as pp
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')


def get_binary_parser(unit_symbol):
  return lambda row_spec_string: sum(
      2**i if char == unit_symbol else 0
      for i, char
      in enumerate(
          reversed(row_spec_string)
      )
  )


def get_location_data(location_spec_str):
  parse_row = get_binary_parser('B')
  parse_column = get_binary_parser('R')
  row = parse_row(location_spec_str[:7])
  column = parse_column(location_spec_str[7:])
  seat_id = row * 8 + column
  return {
      'row': row,
      'column': column,
      'seat_id': seat_id
  }


location_spec_strs = [
    location_spec_str.strip()
    for location_spec_str
    in file_handler.readlines()
]

locations = [
    get_location_data(location_spec_str)
    for location_spec_str
    in location_spec_strs
]

max_seat_id = max(
    location['seat_id'] for location in locations
)

pp(f"Puzzle 1: {max_seat_id}")
