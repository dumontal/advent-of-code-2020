def read_file(name):
    with open(name, "r") as file:
        return [line.strip() for line in file]


def build_locations(lines):
    return [[char for char in line] for line in lines]


def count_trees(locations, slope_x, slope_y):
    x, y = 0, 0
    x_bound = len(locations[0])
    y_bound = len(locations)

    count = 0
    while True:
        if locations[y][x % x_bound] == '#':
            count += 1

        x += slope_x
        y += slope_y

        if (y >= y_bound):
            break

    return count


def count_all_trees(locations, slopes):
    return [count_trees(locations, slope[0], slope[1]) for slope in slopes]


def product(values):
    res = 1
    for value in values:
        res *= value

    return res


def main():
    lines = read_file("map.txt")
    locations = build_locations(lines)
    count = count_trees(locations, slope_x=3, slope_y=1)
    print("Part 1: found {} tree(s) along the path".format(count))

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = count_all_trees(locations, slopes)
    counts_product = product(counts)
    print("Part 2: found product {}".format(counts_product))

    for i in range(len(slopes)):
        print("  > slope {}: found {} tree(s)".format(slopes[i], counts[i]))


if __name__ == '__main__':
    main()
