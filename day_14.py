import re

from inputs.reader import read_input_file


class Interpreter:

    MASK_PATTERN = re.compile(r"mask = (\w+)")
    MEM_PATTERN = re.compile(r"mem\[(\d+)\] = (\d+)")


    def __init__(self, version):
        self.current_mask = None
        self.memory = dict()

        apply_mask_versions = {
            1: self.apply_mask_v1,
            2: self.apply_mask_v2
        }

        self.apply_mask = apply_mask_versions[version]


    def interpret(self, lines):
        self.current_mask = None
        self.memory = dict()

        for line in lines:
            self.interpret_single(line)

        return sum(value for value in self.memory.values())


    def interpret_single(self, line):
        match = self.MASK_PATTERN.fullmatch(line)

        if match is not None:
            self.current_mask = match.group(1)
            return

        match = self.MEM_PATTERN.fullmatch(line)

        if match is None:
            raise Exception('Cannot parse line', line)

        address, value = match.group(1, 2)
        self.apply_mask(address, value)


    def apply_mask_v1(self, address, value):
        bits = to_bit_string(value, len(self.current_mask))

        masked_bits = ""
        for bit, mask_bit in zip(bits, self.current_mask):
            masked_bits += bit if mask_bit == "X" else mask_bit

        self.memory[int(address)] = to_int(masked_bits)


    def apply_mask_v2(self, address, value):
        bits = to_bit_string(address, len(self.current_mask))

        masked_bits = ""
        for bit, mask_bit in zip(bits, self.current_mask):
            masked = { "0": bit, "1": "1", "X": "X" }
            masked_bits += masked[mask_bit]

        for floating_address_bits in enumerate_floating(masked_bits):
            floating_address = to_int(floating_address_bits)
            self.memory[floating_address] = int(value)


def to_bit_string(int_string, length):
    value = int(int_string)
    binary_string = "{0:b}".format(value)
    return binary_string.zfill(length)


def to_int(binary_string):
    return int(binary_string, 2)


def enumerate_floating(masked_bits):
    index = masked_bits.find("X")
    if index == -1:
        yield masked_bits
    else:
        yield from enumerate_floating(masked_bits.replace("X", "0", 1))
        yield from enumerate_floating(masked_bits.replace("X", "1", 1))


def main():
    lines = read_input_file("14.txt")
    value = Interpreter(version=1).interpret(lines)
    print("Part 1: the sum of all masked memory values is {}".format(value))

    value = Interpreter(version=2).interpret(lines)
    print("Part 2: the sum of all masked memory values is {}".format(value))


if __name__ == "__main__":
    main()
