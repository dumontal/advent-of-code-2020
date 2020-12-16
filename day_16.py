import re

from inputs.reader import read_input_file


class Parser:

    RULE_PATTERN = re.compile(r"([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)")


    def __init__(self):
        self.rules = []
        self.my_ticket = []
        self.nearby_tickets = []


    # A rule is a tuple (name, interval_1, interval_2).
    # An interval is a tuple (min, max).
    def parse_rule(self, line):
        match = self.RULE_PATTERN.fullmatch(line)

        if match is None:
            raise Exception("Cannot parse rule", line)

        rule = (
            match.group(1),
            (
                int(match.group(2)),
                int(match.group(3))
            ),
            (
                int(match.group(4)),
                int(match.group(5))
            )
        )

        self.rules.append(rule)


    def parse_my_ticket(self, line):
        self.my_ticket = Parser.parse_ticket(line)


    def parse_nearby_ticket(self, line):
        ticket = Parser.parse_ticket(line)
        self.nearby_tickets.append(ticket)


    # A ticket is a list of numbers.
    @staticmethod
    def parse_ticket(line):
        return list(int(number) for number in line.split(","))


    def parse(self, lines):
        parser = self.parse_rule

        for line in lines:
            if len(line) == 0:
                continue

            if line == "your ticket:":
                parser = self.parse_my_ticket
                continue

            if line == "nearby tickets:":
                parser = self.parse_nearby_ticket
                continue

            parser(line)

        return self.rules, self.my_ticket, self.nearby_tickets


def feature_satisfies_rule(feature, rule):
    min_1, max_1 = rule[1]
    min_2, max_2 = rule[2]
    return min_1 <= feature <= max_1 or min_2 <= feature <= max_2


# A ticket is a list of features.
def find_invalid_features(ticket, rules):
    invalid_features = []

    for feature in ticket:
        if all(not feature_satisfies_rule(feature, rule) for rule in rules):
            invalid_features.append(feature)

    return invalid_features


# In version 1, a ticket is valid if all of its features
# are not rejected by at least one rule.
def is_ticket_valid(ticket, rules):
    return len(find_invalid_features(ticket, rules)) == 0


def find_error_rate(rules, nearby_tickets):
    return sum(
        sum(feature for feature in find_invalid_features(ticket, rules))
            for ticket in nearby_tickets
    )


# Returns a map { rule_name -> list of possible positions }
def find_eligible_positions(rules, tickets):
    n_rules = len(rules)
    eligible_positions = { rule[0]: set(range(n_rules)) for rule in rules }

    for ticket in tickets:
        for i, feature in enumerate(ticket):
            for rule in rules:
                if feature_satisfies_rule(feature, rule):
                    continue

                eligible_positions[rule[0]].discard(i)

    return eligible_positions


def find_feature_order(eligible_positions):
    all_positions = eligible_positions.copy()
    names = [ None ] * len(all_positions)

    while len(all_positions) > 0:
        name = None
        position = None

        for rule_name, positions in all_positions.items():
            if len(positions) == 1:
                name = rule_name
                position = positions.pop()
                break

        names[position] = name

        del all_positions[name]
        for positions in all_positions.values():
            positions.discard(position)

    return names


def multiply(numbers):
    result = 1
    for number in numbers:
        result *= number

    return result


def resolve_my_ticket(rules, my_ticket, nearby_tickets):
    valid_nearby_tickets = list(
        ticket for ticket in nearby_tickets
            if is_ticket_valid(ticket, rules)
    )

    eligible_positions = find_eligible_positions(rules, valid_nearby_tickets)
    ordered_feature_names = find_feature_order(eligible_positions)
    assert len(ordered_feature_names) == len(my_ticket)

    filtered_ticket = list(
        value for name, value in zip(ordered_feature_names, my_ticket)
            if name.startswith("departure")
    )
    assert len(filtered_ticket) == 6

    return multiply(filtered_ticket)


def main():
    lines = read_input_file("16.txt")
    rules, my_ticket, nearby_tickets = Parser().parse(lines)

    error_rate = find_error_rate(rules, nearby_tickets)
    print("Part 1: the error rate is {}".format(error_rate))

    value = resolve_my_ticket(rules, my_ticket, nearby_tickets)
    print("Part 2: the value is {}".format(value))


if __name__ == "__main__":
    main()
