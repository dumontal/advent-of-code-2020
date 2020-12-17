from inputs.reader import read_input_file


def parse_layer(lines):
    active_coords = set()

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                active_coords.add((i, j, 0, 0))

    return {
        "min_i": 0,
        "max_i": len(lines) - 1,
        "min_j": 0,
        "max_j": len(lines[0]) - 1,
        "min_k": 0,
        "max_k": 0,
        "min_l": 0,
        "max_l": 0,
        "active_coords": active_coords
    }


def enumerate_neighbours_coords(coords):
    min_i, max_i = coords[0] - 1, coords[0] + 1
    min_j, max_j = coords[1] - 1, coords[1] + 1
    min_k, max_k = coords[2] - 1, coords[2] + 1
    min_l, max_l = coords[3] - 1, coords[3] + 1

    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            for k in range(min_k, max_k + 1):
                for l in range(min_l, max_l + 1):

                    if (i, j, k, l) == coords:
                        continue

                    yield (i, j, k, l)


def is_active_at_next_cycle(space, coords):
    active_coords = space["active_coords"]

    active_neighbours_count = sum(
        1 for neighbour_coords in enumerate_neighbours_coords(coords)
            if neighbour_coords in active_coords
    )

    if coords in active_coords:
        return active_neighbours_count in { 2, 3 }

    return active_neighbours_count == 3


def apply_cycle(space, include_hyperspace_dimension):
    min_i = space["min_i"] - 1
    max_i = space["max_i"] + 1
    min_j = space["min_j"] - 1
    max_j = space["max_j"] + 1
    min_k = space["min_k"] - 1
    max_k = space["max_k"] + 1
    min_l = space["min_l"] - (1 if include_hyperspace_dimension else 0)
    max_l = space["max_l"] + (1 if include_hyperspace_dimension else 0)

    active_coords = set()

    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            for k in range(min_k, max_k + 1):
                for l in range(min_l, max_l + 1):
                    coords = (i, j, k, l)

                    if is_active_at_next_cycle(space, coords):
                        active_coords.add(coords)

    return {
        "min_i": min_i,
        "max_i": max_i,
        "min_j": min_j,
        "max_j": max_j,
        "min_k": min_k,
        "max_k": max_k,
        "min_l": min_l,
        "max_l": max_l,
        "active_coords": active_coords
    }


def apply_cycles(space, n_cycles, include_hyperspace_dimension):
    next_space = space

    for _ in range(n_cycles):
        next_space = apply_cycle(next_space, include_hyperspace_dimension)

    return len(next_space["active_coords"])


def main():
    lines = read_input_file("17.txt")
    space = parse_layer(lines)

    count_active = apply_cycles(space, n_cycles=6, include_hyperspace_dimension=False)
    print("Part 1: the number of active cubes after 6 cycles is {}".format(count_active))

    count_active = apply_cycles(space, n_cycles=6, include_hyperspace_dimension=True)
    print("Part 2: the number of active cubes after 6 cycles is {}".format(count_active))


if __name__ == "__main__":
    main()
