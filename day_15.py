def find_spoken_number(numbers, nth):
    last_turns = { value: i for i, value in enumerate(numbers[:-1]) }
    spoken_number = numbers[-1]

    for turn in range(len(numbers), nth):
        previous_turn = turn - 1

        if spoken_number in last_turns:
            number_to_speak = previous_turn - last_turns[spoken_number]
            last_turns[spoken_number] = previous_turn
            spoken_number = number_to_speak
        else:
            last_turns[spoken_number] = previous_turn
            spoken_number = 0

    return spoken_number


def main():
    numbers = [ 16, 11, 15, 0, 1, 7 ]
    number_part_1 = find_spoken_number(numbers, 2020)
    print("Part 1: the 2020th number is {}".format(number_part_1))

    number_part_2 = find_spoken_number(numbers, 30000000)
    print("Part 2: the 30000000th number is {}".format(number_part_2))


if __name__ == "__main__":
    main()
