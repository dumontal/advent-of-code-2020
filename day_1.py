from inputs.reader import read_input_file


def find_pair(entries_set, target_sum):
    for value in entries_set:
        complementary_value = target_sum - value

        if complementary_value in entries_set:
            return value, complementary_value

    return None


def find_trio(entries_set, target_sum):
    for value in entries_set:
        sub_set = entries_set - { value }
        sub_target_sum = target_sum - value
        complementary_pair = find_pair(sub_set, sub_target_sum)

        if complementary_pair is not None:
            (second, third) = complementary_pair
            return value, second, third

    return None


def main():
    lines = read_input_file("1.txt")
    entries = [int(line) for line in lines]

    entries_set = set(entries)
    assert len(entries) == len(entries_set), "Implementation requires no duplicates in the input"

    pair = find_pair(entries_set, 2020)

    if pair is None:
        print("Pair not found")
    else:
        first, second = pair
        print("Found pair {} x {} = {}".format(first, second, first * second))

    trio = find_trio(entries_set, 2020)

    if trio is None:
        print("Trio not found")
    else:
        (first, second, third) = trio
        print("Found trio {} x {} x {} = {}".format(first, second, third, first * second * third))


if __name__ == '__main__':
    main()
