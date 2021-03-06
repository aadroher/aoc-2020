from pathlib import Path
from pprint import pprint as pp
from functools import reduce

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')


def get_binary_parser(one_symbol):
    return lambda row_spec_string: sum(
        2**i if char == one_symbol else 0
        for i, char
        in enumerate(
            reversed(row_spec_string)
        )
    )


def get_location_data(location_spec_str):
    parse_row = get_binary_parser(one_symbol='B')
    parse_column = get_binary_parser(one_symbol='R')
    row = parse_row(location_spec_str[:7])
    column = parse_column(location_spec_str[7:])
    seat_id = row * 8 + column
    return {
        'row': row,
        'column': column,
        'seat_id': seat_id
    }


def get_empty_seat_id(seat_ids):
    sorted_seats = list(sorted(seat_ids))
    return next(
        seat_id + 1 for i, seat_id in enumerate(sorted_seats)
        if sorted_seats[i+1] != seat_id + 1
    )


location_spec_strs = (
    location_spec_str.strip()
    for location_spec_str
    in file_handler.readlines()
)

locations = (
    get_location_data(location_spec_str)
    for location_spec_str
    in location_spec_strs
)

seat_ids = [
    location['seat_id'] for location in locations
]

max_seat_id = max(seat_ids)
empty_seat_id = get_empty_seat_id(seat_ids)

pp(f"Puzzle 1: {max_seat_id}")
pp(f"Puzzle 2: {empty_seat_id}")
