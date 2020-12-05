def read_file(name):
    with open(name, "r") as file:
        return [line.strip() for line in file]


def decode_seat(line):
    assert len(line) == 7 + 3, "The encoded seat is not 10 characters long"
    row = decode_binary_string(line[:7], "B")
    column = decode_binary_string(line[7:], "R")
    return row, column


def decode_binary_string(binary_string, positive_char):
    bits_enumerator = enumerate(reversed(binary_string))
    values = [ 2**i if char == positive_char else 0 for i, char in bits_enumerator ]
    return sum(values)


def get_seat_id(seat):
    return seat[0] * 8 + seat[1]


def find_missing_seat_id(seat_ids):
    ids_set = set(seat_ids)

    for seat_id in sorted(seat_ids):
        candidate_id = seat_id + 1
        if candidate_id not in ids_set:
            return candidate_id

    return None


def main():
    lines = read_file("boarding-passes.txt")
    seats = [ decode_seat(line) for line in lines ]
    seat_ids = [ get_seat_id(seat) for seat in seats ]
    max_seat_id = max(seat_ids)
    print("Part 1: the maximum seat id is {}".format(max_seat_id))

    missing_seat_id = find_missing_seat_id(seat_ids)
    if missing_seat_id is None:
        print("Part 2: no missing seat id has been found. Weird.")
    else:
        print("Part 2: the missing seat id is {}".format(missing_seat_id))


if __name__ == '__main__':
    main()
