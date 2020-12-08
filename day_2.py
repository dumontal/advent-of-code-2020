import re

from inputs.reader import read_input_file


class PassWordPolicy:

    def __init__(self, lower_bound, upper_bound, char, password):
        self._min = lower_bound
        self._max = upper_bound
        self._char = char
        self._password = password


    def is_compliant_v1(self):
        count = self._password.count(self._char)
        return self._min <= count <= self._max


    def is_compliant_v2(self):
        first_char = self._password[self._min - 1]
        second_char = self._password[self._max - 1]
        return (first_char == self._char) != (second_char == self._char)


LINE_PATTERN = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def parse_policy(line):
    match = LINE_PATTERN.match(line)

    if match is None:
        return None

    return PassWordPolicy(
        lower_bound = int(match.group(1)),
        upper_bound = int(match.group(2)),
        char = match.group(3),
        password = match.group(4)
    )


def main():
    lines = read_input_file("2.txt")
    policies = [parse_policy(line) for line in lines]

    compliant_policies_v1 = [policy for policy in policies if policy.is_compliant_v1()]
    print("Part 1: found {} compliant policies".format(len(compliant_policies_v1)))

    compliant_policies_v2 = [policy for policy in policies if policy.is_compliant_v2()]
    print("Part 2: found {} compliant policies".format(len(compliant_policies_v2)))


if __name__ == '__main__':
    main()
