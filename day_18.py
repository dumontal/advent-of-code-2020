from inputs.reader import read_input_file


VERSION = 1


def tokenize(line):
    tokens = []
    current_number_token = ''

    for char in line.replace(" ", ""):
        if char.isdigit():
            current_number_token += char

        elif char in { '(', ')', '*', '+' }:
            if len(current_number_token) > 0:
                tokens.append(int(current_number_token))
                current_number_token = ''

            tokens.append(char)

        else:
            raise Exception("Unknown token {} in {}".format(char, line))

    if len(current_number_token) > 0:
        tokens.append(int(current_number_token))

    return tokens


def evaluate_simple(expression):
    global VERSION

    evaluators = {
        1: evaluate_simple_v1,
        2: evaluate_simple_v2
    }

    return evaluators[VERSION](expression)


def evaluate_simple_v1(expression):
    result = 0
    operation = "+"

    for token in expression:
        if token in { '*', '+' }:
            operation = token

        elif operation == "+":
            result += token

        elif operation == "*":
            result *= token

        else:
            raise Exception("Unknown token {}".format(token))

    return result


def evaluate_simple_v2(expression):
    reduced_expression = expression.copy()

    while "+" in reduced_expression:
        i = reduced_expression.index("+")
        result = reduced_expression[i - 1] + reduced_expression[i + 1]
        del reduced_expression[i - 1: i + 2]
        reduced_expression.insert(i - 1, result)

    while "*" in reduced_expression:
        i = reduced_expression.index("*")
        result = reduced_expression[i - 1] * reduced_expression[i + 1]
        del reduced_expression[i - 1: i + 2]
        reduced_expression.insert(i - 1, result)

    assert len(reduced_expression) == 1
    return reduced_expression.pop()


def evaluate_innermost(full_expression):
    expression = full_expression.copy()
    start = expression.index('(')
    end = start

    while end < len(expression):
        if expression[end] == ')':
            break

        if expression[end] == '(':
            start = end

        end += 1

    sub_expression = expression[start + 1 : end]
    evaluated_sub_expression = evaluate_simple(sub_expression)

    del expression[start: end + 1]
    expression.insert(start, evaluated_sub_expression)
    return expression


def evaluate(full_expression):
    expression = full_expression

    while '(' in expression:
        expression = evaluate_innermost(expression)

    return evaluate_simple(expression)


def evaluate_all(expressions):
    return sum(evaluate(expression) for expression in expressions)


def main():
    global VERSION

    lines = read_input_file("18.txt")
    expressions = list(tokenize(line) for line in lines)

    VERSION = 1
    total = evaluate_all(expressions)
    print("Part 1: the sum of evaluated expressions is {}".format(total))

    VERSION = 2
    total = evaluate_all(expressions)
    print("Part 2: the sum of evaluated expressions is {}".format(total))


if __name__ == "__main__":
    main()
