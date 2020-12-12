import abc

from inputs.reader import read_input_file


def parse_commands(lines):
    return [ (line[0], int(line[1:])) for line in lines ]


class Ship(abc.ABC):

    def __init__(self):
        self.position = (0, 0)
        self.executors = {
            'N': self.exec_north,
            'S': self.exec_south,
            'E': self.exec_east,
            'W': self.exec_west,
            'L': self.exec_rotate_left,
            'R': self.exec_rotate_right,
            'F': self.exec_forward
        }


    def follow(self, commands):
        for (instruction, value) in commands:
            self.execute(instruction, value)


    def execute(self, instruction, value):
        executor = self.executors[instruction]
        executor(value)


    def get_manhattan_distance(self):
        position_x, position_y = self.position
        return abs(position_x) + abs(position_y)


    @abc.abstractmethod
    def exec_north(self, value):
        pass


    @abc.abstractmethod
    def exec_south(self, value):
        pass


    @abc.abstractmethod
    def exec_east(self, value):
        pass


    @abc.abstractmethod
    def exec_west(self, value):
        pass


    @abc.abstractmethod
    def exec_rotate_left(self, angle_degrees):
        pass


    @abc.abstractmethod
    def exec_rotate_right(self, angle_degrees):
        pass


    @abc.abstractmethod
    def exec_forward(self, value):
        pass


class Ship1(Ship):

    def __init__(self, facing_direction):
        self.facing_direction = facing_direction
        super().__init__()


    def exec_north(self, value):
        self.move_position(lambda x, y: (x, y + value))


    def exec_south(self, value):
        self.move_position(lambda x, y: (x, y - value))


    def exec_east(self, value):
        self.move_position(lambda x, y: (x + value, y))


    def exec_west(self, value):
        self.move_position(lambda x, y: (x - value, y))


    def exec_rotate_left(self, angle_degrees):
        self.rotate(angle_degrees, trigo=True)


    def exec_rotate_right(self, angle_degrees):
        self.rotate(angle_degrees, trigo=False)


    def exec_forward(self, value):
        instruction = self.facing_direction
        self.execute(instruction, value)


    def move_position(self, get_next):
        self.position = get_next(*self.position)


    def rotate(self, angle_degrees, trigo):
        directions = [ 'N', 'W', 'S', 'E' ]
        offset = (angle_degrees % 360) // 90

        if not trigo:
            offset = -offset

        current_index = directions.index(self.facing_direction)
        next_index = (current_index + offset) % len(directions)
        self.facing_direction = directions[next_index]


class Ship2(Ship):

    def __init__(self, waypoint):
        self.waypoint = waypoint
        super().__init__()


    def exec_north(self, value):
        self.move_waypoint(lambda x, y: (x, y + value))


    def exec_south(self, value):
        self.move_waypoint(lambda x, y: (x, y - value))


    def exec_east(self, value):
        self.move_waypoint(lambda x, y: (x + value, y))


    def exec_west(self, value):
        self.move_waypoint(lambda x, y: (x - value, y))


    def exec_rotate_left(self, angle_degrees):
        self.rotate_waypoint(angle_degrees, trigo=True)


    def exec_rotate_right(self, angle_degrees):
        self.rotate_waypoint(angle_degrees, trigo=False)


    def exec_forward(self, value):
        position_x, position_y = self.position
        waypoint_x, waypoint_y = self.waypoint
        self.position = (
            position_x + value * waypoint_x,
            position_y + value * waypoint_y
        )


    def move_waypoint(self, get_next):
        self.waypoint = get_next(*self.waypoint)


    def rotate_waypoint(self, angle_degrees, trigo):
        transformations = {
            90:  lambda x, y: (-y, x),
            180: lambda x, y: (-x, -y),
            270: lambda x, y: (y, -x),
            360: lambda x, y: (x, y),
        }

        angle = (angle_degrees if trigo else -angle_degrees) % 360
        self.move_waypoint(transformations[angle])


def main():
    lines = read_input_file("12.txt")
    commands = parse_commands(lines)

    ship = Ship1(facing_direction='E')
    ship.follow(commands)
    distance = ship.get_manhattan_distance()
    print('Part 1: the Manhattan distance is {}'.format(distance))

    ship = Ship2(waypoint=(10, 1))
    ship.follow(commands)
    distance = ship.get_manhattan_distance()
    print('Part 2: the Manhattan distance is {}'.format(distance))


if __name__ == '__main__':
    main()
