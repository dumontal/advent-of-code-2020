import re

from inputs.reader import read_input_file


OUTER_BAG_PATTERN = re.compile(r"(\w+ \w+) bags")
INNER_BAG_PATTERN = re.compile(r"(\d+) (\w+ \w+) bag[s]?")


def gather_rule(line):
    left_hand_side, right_hand_side = line[:-1].split(" contain ")
    outer_bag_match = OUTER_BAG_PATTERN.fullmatch(left_hand_side)

    if outer_bag_match is None:
        print("Could not parse the left hand side of rule {} -> {}".format(line, left_hand_side))
        return None, None

    outer_bag = outer_bag_match.group(1)

    if "no other bags" in right_hand_side:
        return outer_bag, {}

    inner_bags = {}

    for inner_bag_str in right_hand_side.split(", "):
        inner_bag_match = INNER_BAG_PATTERN.fullmatch(inner_bag_str)

        if inner_bag_match is None:
            print("Could not parse the right hand side of rule {} -> {}"\
                .format(line, inner_bag_str))
            return None, None

        count, inner_bag = inner_bag_match.group(1, 2)
        inner_bags[inner_bag] = int(count)

    return outer_bag, inner_bags


def gather_rules(lines):
    rules = [ gather_rule(line) for line in lines ]
    return { rule[0]: rule[1] for rule in rules }


def get_direct_outer_bags(rules, bag):
    return [ outer_bag for outer_bag, inner_bags in rules.items() if bag in inner_bags.keys() ]


def search_outer_bags(rules, bag):
    direct_outer_bags = get_direct_outer_bags(rules, bag)
    outer_bags = set(direct_outer_bags)

    for outer_bag in direct_outer_bags:
        outer_bags |= search_outer_bags(rules, outer_bag)

    return outer_bags


def count_inner_bags(rules, bag):
    inner_bags = rules[bag]

    if len(inner_bags) == 0:
        return 0

    inner_counts = [ count * (1 + count_inner_bags(rules, bag)) \
        for bag, count in inner_bags.items() ]

    return sum(inner_counts)


def main():
    lines = read_input_file("7.txt")
    rules = gather_rules(lines)

    outer_bags = search_outer_bags(rules, "shiny gold")
    count = len(outer_bags)
    print("Part 1 - {} bag(s) can contain a shiny gold one".format(count))

    count = count_inner_bags(rules, "shiny gold")
    print("Part 2 - a shiny gold bag contains {} other bags".format(count))


if __name__ == '__main__':
    main()
