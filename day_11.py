import abc

from inputs.reader import read_input_file


OCCUPIED = '#'
FREE = 'L'
FLOOR = '.'


def parse_initial_configuration(lines):
    return [ list(line) for line in lines ]


class Simulator(abc.ABC):

    def __init__(self, configuration):
        self.configuration = configuration


    @abc.abstractmethod
    def rule_occupied(self, i, j):
        pass


    @abc.abstractmethod
    def rule_free(self, i, j):
        pass


    def count_occupied_seats(self):
        count_occupied_seats_in_row = lambda row: sum(1 for seat in row if seat == OCCUPIED)
        return sum(count_occupied_seats_in_row(row) for row in self.configuration)


    def next_tick_seat(self, seat, i, j):
        if seat == OCCUPIED:
            return self.rule_occupied(i, j)

        if seat == FREE:
            return self.rule_free(i, j)

        return seat


    def next_tick(self):
        next_configuration = []
        is_stable = True

        for i, row in enumerate(self.configuration):
            next_row = []

            for j, seat in enumerate(row):
                next_tick_seat = self.next_tick_seat(seat, i, j)
                is_stable = is_stable and next_tick_seat == seat
                next_row.append(next_tick_seat)

            next_configuration.append(next_row)

        self.configuration = next_configuration
        return is_stable


    def run(self):
        is_stable = False

        while not is_stable:
            is_stable = self.next_tick()

        return self.count_occupied_seats()


class Part1Simulator(Simulator):

    def enumerate_adjacent_seats(self, i, j):
        max_i = len(self.configuration)
        max_j = len(self.configuration[0])

        positions = [
           (i - 1, j),
           (i - 1, j + 1),
           (i - 1, j - 1),
           (i, j + 1),
           (i, j - 1),
           (i + 1, j),
           (i + 1, j + 1),
           (i + 1, j - 1)
        ]

        for pos_i, pos_j in positions:
            if 0 <= pos_i < max_i and 0 <= pos_j < max_j:
                yield self.configuration[pos_i][pos_j]


    def rule_occupied(self, i, j):
        seats = self.enumerate_adjacent_seats(i, j)
        return FREE if sum(1 for seat in seats if seat == OCCUPIED) >= 4 else OCCUPIED


    def rule_free(self, i, j):
        seats = self.enumerate_adjacent_seats(i, j)
        return OCCUPIED if all(seat != OCCUPIED for seat in seats) else FREE


class Part2Simulator(Simulator):

    def find_first_seat(self, seat_i, seat_j, move):
        max_i = len(self.configuration)
        max_j = len(self.configuration[0])
        i, j = move(seat_i, seat_j)

        while 0 <= i < max_i and 0 <= j < max_j:
            seat = self.configuration[i][j]
            if seat != FLOOR:
                return seat

            i, j = move(i, j)

        return None


    def enumerate_sightable_seats(self, seat_i, seat_j):
        moves = [
            lambda i, j: (i - 1, j),
            lambda i, j: (i - 1, j + 1),
            lambda i, j: (i - 1, j - 1),
            lambda i, j: (i, j + 1),
            lambda i, j: (i, j - 1),
            lambda i, j: (i + 1, j),
            lambda i, j: (i + 1, j + 1),
            lambda i, j: (i + 1, j - 1),
        ]

        for move in moves:
            sightable_seat = self.find_first_seat(seat_i, seat_j, move)
            if sightable_seat is not None:
                yield sightable_seat


    def rule_occupied(self, i, j):
        seats = self.enumerate_sightable_seats(i, j)
        return FREE if sum(1 for seat in seats if seat == OCCUPIED) >= 5 else OCCUPIED


    def rule_free(self, i, j):
        seats = self.enumerate_sightable_seats(i, j)
        return OCCUPIED if all(seat != OCCUPIED for seat in seats) else FREE


def main():
    lines = read_input_file("11.txt")
    configuration = parse_initial_configuration(lines)

    simulator = Part1Simulator(configuration)
    occupied_seats = simulator.run()
    print("Part 1: the number of occupied seats is {}".format(occupied_seats))

    simulator = Part2Simulator(configuration)
    occupied_seats = simulator.run()
    print("Part 2: the number of occupied seats is {}".format(occupied_seats))


if __name__ == '__main__':
    main()
