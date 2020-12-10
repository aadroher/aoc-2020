from pathlib import Path
from pprint import pprint as pp
from functools import reduce
from collections import namedtuple

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

instructions = [
    line.strip()
    for line
    in file_handler.readlines()
]

with_execution_count = [
    (instruction, 0)
    for instruction in instructions
]


def execute_next(
    instruction_pointer=0,
    accumulator=0,
    instructions_with_counter=with_execution_count
):
    instruction, execution_count = \
        instructions_with_counter[instruction_pointer]

    if execution_count == 0:
        instructions_with_counter[instruction_pointer] = (instruction, 1)

        operation, argument = instruction.split(' ')
        if operation == 'acc':
            return execute_next(
                instruction_pointer=instruction_pointer + 1,
                accumulator=accumulator + int(argument),
                instructions_with_counter=instructions_with_counter
            )
        elif operation == 'jmp':
            return execute_next(
                instruction_pointer=(
                    instruction_pointer + int(argument)
                ),
                accumulator=accumulator,
                instructions_with_counter=instructions_with_counter
            )
        elif operation == 'nop':
            return execute_next(
                instruction_pointer=instruction_pointer + 1,
                accumulator=accumulator,
                instructions_with_counter=instructions_with_counter
            )
    else:
        return accumulator


accumulator = execute_next()

pp(f"Puzzle 1: {accumulator}")
