from inputs.reader import read_input_file


def parse_numbers(lines):
    return [ int(line) for line in lines ]


def is_compliant(number, window):
    for candidate in window:
        buddy = number - candidate
        if buddy != candidate and buddy in window:
            return True

    return False


def find_first_uncompliant(numbers, window_size):
    assert len(numbers) > window_size, "The list of numbers is too small"

    for i, number in enumerate(numbers):
        if i < window_size:
            continue

        window = numbers[i-window_size: i]
        if not is_compliant(number, window):
            return number

    return None


def find_contiguous_range_with_sum(numbers, target_sum):
    if len(numbers) < 2:
        return None

    contiguous_range = [ numbers[0] ]
    range_sum =  numbers[0]

    for number in numbers[1:]:
        contiguous_range.append(number)
        range_sum += number

        if range_sum == target_sum:
            return contiguous_range

        if range_sum > target_sum:
            break

    # the first number does not belong to the contiguous range
    return find_contiguous_range_with_sum(numbers[1:], target_sum)


def find_encryption_weakness(contiguous_range):
    return min(contiguous_range) + max(contiguous_range)


def main():
    lines = read_input_file("9.txt")
    numbers = parse_numbers(lines)
    uncompliant_number = find_first_uncompliant(numbers, window_size=25)
    print("Part 1: the first uncompliant number is {}".format(uncompliant_number))

    contiguous_range = find_contiguous_range_with_sum(numbers, target_sum=uncompliant_number)
    weakness = find_encryption_weakness(contiguous_range)
    print("Part 2: the encryption weakness is {}".format(weakness))


if __name__ == '__main__':
    main()
