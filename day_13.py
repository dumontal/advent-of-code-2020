from inputs.reader import read_input_file


def parse_lines(lines):
    assert len(lines) == 2, "Invalid file format"
    earliest_timestamp = int(lines[0])
    bus_ids = list(map(
        lambda bus_id: (int(bus_id) if bus_id != "x" else bus_id),
        lines[1].split(",")
    ))

    return earliest_timestamp, bus_ids


def find_earliest_bus(earliest_timestamp, bus_ids):
    earliest_bus_id = None
    min_waiting_time = None

    for bus_id in bus_ids:
        if bus_id == "x":
            continue

        waiting_time = get_waiting_time(earliest_timestamp, bus_id)

        if earliest_bus_id is None or waiting_time < min_waiting_time:
            earliest_bus_id = bus_id
            min_waiting_time = waiting_time

    return earliest_bus_id, min_waiting_time


def get_waiting_time(timestamp, bus_id):
    remaining_time = timestamp % bus_id
    return bus_id - remaining_time if remaining_time > 0 else 0


def combine_buses(bus_1, bus_2, earliest_timestamp):
    bus_1_cycle, bus_1_offset = bus_1
    bus_2_cycle, bus_2_offset = bus_2
    timestamp = earliest_timestamp
    cycle_start = None

    while True:
        if (timestamp + bus_2_offset - bus_1_offset) % bus_2_cycle == 0:
            # Yay, the second bus is synchronized in this cycle
            if cycle_start is None:
                cycle_start = timestamp
            else:
                break

        timestamp += bus_1_cycle

    new_earliest_timestamp = cycle_start
    combined_bus_cycle = timestamp - new_earliest_timestamp
    combined_bus_offset = 0
    return (combined_bus_cycle, combined_bus_offset), new_earliest_timestamp


def find_earliest_timestamp(bus_ids):
    # a bus == (id, offset)
    buses = list((bus_id, offset)
        for offset, bus_id in enumerate(bus_ids) if bus_id != "x"
    )

    current_bus = buses[0]
    timestamp = 0

    for bus in buses[1:]:
        current_bus, timestamp = combine_buses(current_bus, bus, timestamp)

    return timestamp


def main():
    lines = read_input_file("13.txt")
    earliest_timestamp, bus_ids = parse_lines(lines)

    bus_id, waiting_time = find_earliest_bus(earliest_timestamp, bus_ids)
    print("Part 1: the earliest bus ID is {}, arriving in {} minutes".format(bus_id, waiting_time))
    print("  > the answer is {}".format(bus_id * waiting_time))

    timestamp = find_earliest_timestamp(bus_ids)
    print("Part 2: the earliest timestamp found is {}".format(timestamp))


if __name__ == "__main__":
    main()
