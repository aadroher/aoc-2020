from pathlib import Path
from pprint import pprint as pp
from itertools import chain
from functools import reduce, cache
from collections import namedtuple

current_dir = Path(__file__).parent
file_handler = open(current_dir/"input.txt", 'r')

instructions = [
    line.strip()
    for line
    in file_handler.readlines()
]
termination_pointer_value = len(instructions) - 1


def initialise_execution_count(instruction_list):
    return [
        (instruction, 0)
        for instruction in instruction_list
    ]


def execute_next(
    instruction_pointer=0,
    accumulator=0,
    instructions_with_counter=initialise_execution_count(instructions)
):
    try:
        instruction, execution_count = \
            instructions_with_counter[instruction_pointer]
        if execution_count == 0 and instruction_pointer != termination_pointer_value:
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
            return {
                'instruction_pointer': instruction_pointer,
                'accumulator': accumulator,
            }
    except Exception:
        return {
            'instruction_pointer': instruction_pointer,
            'accumulator': accumulator,
        }


def get_enumerated_instructions_by_operation(operation):
    return (
        (i, instruction)
        for i, instruction
        in enumerate(instructions)
        if instruction.split(' ')[0] == operation
    )


def change_operation(new_operation, index, instruction_list):
    _, argument = instruction_list[index].split(' ')
    new_instruction = f"{new_operation} {argument}"
    new_instruction_list = list(instruction_list)
    new_instruction_list[index] = new_instruction
    return new_instruction_list


def get_instruction_combinations():
    enumerated_jmp_instructions = \
        get_enumerated_instructions_by_operation('jmp')
    jmp_instruction_changes = (
        change_operation('nop', index, instructions)
        for index, _ in enumerated_jmp_instructions
    )
    enumerated_nop_instructions = \
        get_enumerated_instructions_by_operation('nop')
    nop_instruction_changes = (
        change_operation('jmp', index, instructions)
        for index, _ in enumerated_nop_instructions
    )
    return chain(
        jmp_instruction_changes,
        nop_instruction_changes
    )


def did_terminate(execution_result):
    return execution_result['instruction_pointer'] == termination_pointer_value


def check_all_fixes():
    results = (
        execute_next(
            instructions_with_counter=initialise_execution_count(
                instruction_combination
            )
        ) for instruction_combination
        in get_instruction_combinations()
    )
    return next(
        result for result in results if did_terminate(result)
    )


result = execute_next()
fixed_result = check_all_fixes()

pp(f"Puzzle 1: {result['accumulator']}")

pp(f"Puzzle 2: {fixed_result['accumulator']}")
