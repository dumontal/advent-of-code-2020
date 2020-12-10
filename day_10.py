from inputs.reader import read_input_file


def get_pairwise_hops(adapters):
    # Include 0 as the first adapter
    chain = [0] + sorted(adapters)
    hops = [ chain[i] - chain[i - 1] for i in range(1, len(chain)) ]
    # The last hop must always be 3
    return hops + [3]


def count_number_of_hops(hops, value):
    return sum(1 for hop in hops if hop == value)


def get_joltage_number(adapters):
    hops = get_pairwise_hops(adapters)
    return count_number_of_hops(hops, value=1) * count_number_of_hops(hops, value=3)


def get_all_combinations_count(adapters):
    sorted_adapters = [0] + sorted(adapters)
    last_adapter = sorted_adapters[-1]
    combinations = { last_adapter: 1 }

    for adapter in reversed(sorted_adapters[:-1]):
        candidates = (adapter + 1, adapter + 2, adapter + 3)
        combinations[adapter] = sum(combinations.get(candidate, 0) for candidate in candidates)

    # The number we look for is the sum of combinations to reach the beginning of the list
    return combinations[0]


def main():
    lines = read_input_file("10.txt")
    adapters = [ int(line) for line in lines ]
    number = get_joltage_number(adapters)
    print("Part 1: the product number is {}".format(number))

    combinations_count = get_all_combinations_count(adapters)
    print("Part 2: found a total of {} combinations".format(combinations_count))


if __name__ == '__main__':
    main()
