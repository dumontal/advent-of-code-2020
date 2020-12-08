from inputs.reader import read_input_file


def parse_instruction(line):
    instruction_name, value = line.split(" ")
    return instruction_name, int(value)


def parse_instructions(lines):
    return [ parse_instruction(line) for line in lines ]


def execute(instruction, accumulator, program_counter):
    instruction_name, value = instruction

    if instruction_name == 'nop':
        return accumulator, program_counter + 1

    if instruction_name == 'acc':
        return accumulator + value, program_counter + 1

    if instruction_name == 'jmp':
        return accumulator, program_counter + value

    raise Exception('Unexpected instruction', instruction)


def run_and_stop_at_first_cycle(instructions):
    accumulator = 0
    program_counter = 0
    explored_program_counters = set()

    while True:
        explored_program_counters.add(program_counter)
        instruction = instructions[program_counter]
        accumulator, program_counter = execute(instruction, accumulator, program_counter)

        if program_counter in explored_program_counters or program_counter == len(instructions):
            break

    return accumulator, program_counter


def fix_instructions(instructions, index):
    instruction_name, value = instructions[index]
    new_instructions = instructions.copy()
    new_instructions[index] = ('jmp', value) if instruction_name == 'nop' else ('nop', value)
    return new_instructions


def enumerate_fixed_instructions(instructions):
    yield instructions

    for i, (instruction_name, _) in enumerate(instructions):
        if instruction_name in { 'nop', 'jmp' }:
            yield fix_instructions(instructions, i)


def search_fixed_instructions(instructions):
    program_end = len(instructions)

    for fixed_instructions in enumerate_fixed_instructions(instructions):
        accumulator, program_counter = run_and_stop_at_first_cycle(fixed_instructions)

        if program_counter == program_end:
            return accumulator, program_counter

    return None


def main():
    lines = read_input_file("8.txt")
    instructions = parse_instructions(lines)
    accumulator, _ = run_and_stop_at_first_cycle(instructions)
    print("Part 1: the value in the accumulator is {}".format(accumulator))

    search_result = search_fixed_instructions(instructions)
    if search_result is None:
        print("Part 2: no search result was found ... suspicious")
    else:
        accumulator, _ = search_result
        print("Part 2: the value in the accumulator is {}".format(accumulator))


if __name__ == '__main__':
    main()
