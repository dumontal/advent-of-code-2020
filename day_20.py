from inputs.reader import read_input_file


Tile = list[str]


def parse_tiles(lines: list[str]) -> dict[int, Tile]:
    tiles = {}
    tile_id, tile = None, []

    for line in lines:
        if len(line) == 0:
            tiles[tile_id] = tile
            tile_id, tile = None, []

        elif "Tile" in line:
            tile_id = int(line.replace("Tile ", "").replace(":", ""))

        else:
            tile.append(line)

    tiles[tile_id] = tile
    return tiles


def rotate(tile: Tile) -> Tile:
    return list(''.join(col[::-1]) for col in zip(*tile))


def flip(tile: Tile) -> Tile:
    return list(reversed(tile.copy()))


def build_transformed_tiles(tile: Tile) -> list[Tile]:
    tile90 = rotate(tile)
    tile180 = rotate(tile90)
    tile270 = rotate(tile180)

    return [
        tile, tile90, tile180, tile270,
        flip(tile), flip(tile90), flip(tile180), flip(tile270)
    ]


def build_all_transformed_tiles(tiles: dict[int, Tile]) -> dict[int, list[Tile]]:
    return {
        tile_id: build_transformed_tiles(tile)
            for tile_id, tile in tiles.items()
    }


def are_matching_up(below_tile: Tile, above_tile: Tile) -> bool:
    size = len(below_tile)
    return all(below_tile[0][i] == above_tile[-1][i] for i in range(size))


def are_matching_left(right_tile: Tile, left_tile: Tile) -> bool:
    size = len(right_tile)
    return all(right_tile[i][0] == left_tile[i][-1] for i in range(size))


def assemble(tile_transformations: dict[int, list[Tile]]) -> list[list[tuple[int, int]]]:
    size = len(tile_transformations)
    n = int(size ** 0.5)

    # assembled = matrix of tuples (tile_id, tile_transformation_id)
    assembled = list([(None, None)] * n for _ in range(n))
    remaining_tile_ids = set(tile_transformations.keys())


    def _assemble(row_column):
        if row_column == n * n:
            return True

        r, c = row_column // n, row_column % n

        for tile_id in list(remaining_tile_ids):
            for i, transformation in enumerate(tile_transformations[tile_id]):
                up_edge_matching = True
                left_edge_matching = True

                if r > 0:
                    up_tile_id, up_transformation = assembled[r - 1][c]
                    up_edge_matching = are_matching_up(
                        below_tile = transformation,
                        above_tile = tile_transformations[up_tile_id][up_transformation]
                    )

                if c > 0:
                    left_tile_id, left_transformation = assembled[r][c - 1]
                    left_edge_matching = are_matching_left(
                        right_tile = transformation,
                        left_tile = tile_transformations[left_tile_id][left_transformation]
                    )

                if up_edge_matching and left_edge_matching:
                    assembled[r][c] = (tile_id, i)
                    remaining_tile_ids.remove(tile_id)

                    if _assemble(row_column + 1):
                        return True

                    remaining_tile_ids.add(tile_id)

        return False

    are_assembled = _assemble(0)
    assert are_assembled, "Could not assemble all tiles"
    assert len(remaining_tile_ids) == 0, "Assembled all tiles but some tiles are remaining, weird"
    return assembled


def part_1(assembled_matrix: list[list[tuple[int, int]]]):
    return (
        assembled_matrix[0][0][0]   *
        assembled_matrix[0][-1][0]  *
        assembled_matrix[-1][0][0]  *
        assembled_matrix[-1][-1][0]
    )


def main():
    lines = read_input_file("20.txt")
    tiles = parse_tiles(lines)

    all_transformed_tiles = build_all_transformed_tiles(tiles)
    assembled_matrix = assemble(all_transformed_tiles)
    value = part_1(assembled_matrix)

    print("Part 1: the value is {}".format(value))


if __name__ == "__main__":
    main()
