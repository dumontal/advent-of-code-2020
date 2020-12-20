from inputs.reader import read_input_file


def parse(lines):
    rules = {}
    messages = []
    must_parse_rule = True

    for line in lines:
        if len(line) == 0:
            must_parse_rule = False
            continue

        if must_parse_rule:
            rule_id, rule_definition = parse_rule(line)
            rules[rule_id] = rule_definition
        else:
            messages.append(line)

    return rules, messages


# Returns a pair (rule_id, rule_definition) where
# rule_definition = 'a' or
# rule_definition = [[other_rule_1_id, other_rule_2_id], ...]
def parse_rule(line):
    rule_id_str, rule_definition_raw = line.split(": ")
    rule_id = int(rule_id_str)

    if '"' in rule_definition_raw:
        char = rule_definition_raw.replace('"', "")
        return (rule_id, char)

    definition = []

    for sub_definition in rule_definition_raw.split(" | "):
        other_rule_ids = list(int(other_rule_id) for other_rule_id in sub_definition.split())
        definition.append(other_rule_ids)

    return (rule_id, definition)


class Solver:

    def __init__(self, rules, part_2=False):
        self.rules = rules.copy()

        if part_2:
            self.rules[8] = [[42], [42, 8]]
            self.rules[11] = [[42, 31], [42, 11, 31]]


    # Is it possible to match message using the rules in rule_sequence?
    def is_matching(self, message, rule_sequence):
        if len(message) == 0 or len(rule_sequence) == 0:
            return len(message) == 0 and len(rule_sequence) == 0

        first_rule_definition = self.rules[rule_sequence[0]]

        if isinstance(first_rule_definition, str):
            if message[0] in first_rule_definition:
                return self.is_matching(message[1:], rule_sequence[1:])

            return False

        return any(
            self.is_matching(message, sub_sequence + rule_sequence[1:])
                for sub_sequence in first_rule_definition
        )


    def count_matching(self, messages):
        return sum(self.is_matching(message, [0]) for message in messages)


def main():
    lines = read_input_file("19.txt")
    rules, messages = parse(lines)

    count = Solver(rules).count_matching(messages)
    print("Part 1: the number of matching messages is {}".format(count))

    count = Solver(rules, part_2=True).count_matching(messages)
    print("Part 2: the number of matching messages is {}".format(count))



if __name__ == "__main__":
    main()
