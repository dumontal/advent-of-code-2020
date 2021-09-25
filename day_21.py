from inputs.reader import read_input_file


def parse_recipes(lines):
    return list(parse_recipe(line) for line in lines)


def parse_recipe(line):
    foods = line.split(" (contains ")[0].split()
    allergens = line.split(" (contains ")[1].replace(")", "").split(", ")
    return (foods, allergens)





def main():
    lines = read_input_file("21.txt")
    recipes = parse_recipes(lines)
    for r in recipes:
        print(r)


if __name__ == "__main__":
    main()
