import re


def read_file(name):
    with open(name, "r") as file:
        return [line.strip() for line in file]


class PassWordPolicy(object):

    def __init__(self, min, max, char, password):
        self._min = min
        self._max = max
        self._char = char
        self._password = password


    def is_compliant_v1(self):
        count = self._password.count(self._char)
        return self._min <= count and count <= self._max


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
        min = int(match.group(1)),
        max = int(match.group(2)),
        char = match.group(3),
        password = match.group(4)
    )


def main():
    lines = read_file("input.txt")
    policies = [parse_policy(line) for line in lines]

    compliant_policies_v1 = [policy for policy in policies if policy.is_compliant_v1()]
    print("Part 1: found {} compliant policies".format(len(compliant_policies_v1)))

    compliant_policies_v2 = [policy for policy in policies if policy.is_compliant_v2()]
    print("Part 2: found {} compliant policies".format(len(compliant_policies_v2)))


if __name__ == '__main__':
    main()
