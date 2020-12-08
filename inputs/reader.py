import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def read_input_file(name):
    path = os.path.join(dir_path, name)
    with open(path, "r") as file:
        return [line.strip() for line in file]
