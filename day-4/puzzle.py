import re


def read_file(name):
    with open(name, "r") as file:
        return [line.strip() for line in file]


def gather_passports(lines):
    passports = []
    current_passport = {}

    for line in lines:
        if line == '':
            passports.append(current_passport)
            current_passport = {}
            continue

        for word in line.split():
            key, value = word.split(":")
            current_passport[key] = value

    passports.append(current_passport)
    return passports


def is_valid_v1(passport):
    mandatory_keys = passport.keys() - { "cid" }
    return len(mandatory_keys) == 7


def is_valid_v2(passport):
    return has_all_keys(passport) \
        and has_valid_year(passport, "byr", 1920, 2002) \
        and has_valid_year(passport, "iyr", 2010, 2020) \
        and has_valid_year(passport, "eyr", 2020, 2030) \
        and has_valid_height(passport) \
        and has_valid_hair_color(passport) \
        and has_valid_eye_color(passport) \
        and has_valid_passport_id(passport)


def has_all_keys(passport):
    mandatory_keys = { "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid" }
    return len(mandatory_keys - passport.keys()) == 0


FOUR_DIGITS_PATTERN = re.compile(r"\d{4}")
NINE_DIGITS_PATTERN = re.compile(r"\d{9}")
HEIGHT_PATTERN = re.compile(r"(\d+)(in|cm)")
HAIR_COLOR_PATTERN = re.compile(r"#[a-f0-9]{6}")
ALLOWED_EYE_COLORS = { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" }


def has_valid_year(passport, year_field, min_year, max_year):
    year = passport[year_field]
    match = FOUR_DIGITS_PATTERN.fullmatch(year)
    return match is not None and min_year <= int(year) <= max_year


def has_valid_height(passport):
    match = HEIGHT_PATTERN.fullmatch(passport["hgt"])

    if match is None:
        return False

    (height, unit) = match.group(1, 2)
    height = int(height)
    min_height = 150 if unit == "cm" else 59
    max_height = 193 if unit == "cm" else 76
    return min_height <= height <= max_height


def has_valid_hair_color(passport):
    match = HAIR_COLOR_PATTERN.fullmatch(passport["hcl"])
    return match is not None


def has_valid_eye_color(passport):
    return passport["ecl"] in ALLOWED_EYE_COLORS


def has_valid_passport_id(passport):
    match = NINE_DIGITS_PATTERN.fullmatch(passport["pid"])
    return match is not None


def main():
    lines = read_file("passports.txt")
    passports = gather_passports(lines)
    valid_passports = [passport for passport in passports if is_valid_v1(passport)]
    print("Part 1: found {} valid passports".format(len(valid_passports)))

    valid_passports = [passport for passport in passports if is_valid_v2(passport)]
    print("Part 2: found {} valid passports".format(len(valid_passports)))


if __name__ == '__main__':
    main()
