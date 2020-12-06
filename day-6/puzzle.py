def read_file(name):
    with open(name, "r") as file:
        return [line.strip() for line in file]


def gather_all_group_answers(lines, accumulator):
    all_group_answers = []
    current_group_answers = None

    for line in lines:
        if line == '':
            all_group_answers.append(current_group_answers)
            current_group_answers = None
            continue

        line_as_set = set(line)
        if current_group_answers is None:
            current_group_answers = line_as_set
        else:
            current_group_answers = accumulator(current_group_answers, line_as_set)

    all_group_answers.append(current_group_answers)
    return all_group_answers


def from_anyone(accumulated_set, current_set):
    return accumulated_set | current_set


def from_everyone(accumulated_set, current_set):
    return accumulated_set & current_set


def sum_count_answers(all_group_answers):
    return sum([ len(group_answers) for group_answers in all_group_answers ])


def main():
    lines = read_file("answers.txt")
    all_group_answers = gather_all_group_answers(lines, from_anyone)
    sum_counts = sum_count_answers(all_group_answers)
    print("Part 1 - anyone: the sum of all counts is {}".format(sum_counts))

    all_group_answers = gather_all_group_answers(lines, from_everyone)
    sum_counts = sum_count_answers(all_group_answers)
    print("Part 2 - everyone: the sum of all counts is {}".format(sum_counts))


if __name__ == '__main__':
    main()
