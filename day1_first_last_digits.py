import sys


WORD_TO_DIGIT = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }


def backwards(input_str):
    return ''.join(input_str[::-1])


def first_numeric(input_str):
    for char in input_str:
        if char.isnumeric():
            first_num = char
            break
    return first_num


def last_numeric(input_str):
    for char in input_str[::-1]:
        if char.isnumeric():
            last_num = char
            break
    return last_num


def sum_all_numbers_p1(filename):
    total = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            total += int(first_numeric(line.strip()) + last_numeric(line.strip()))
    return total


def replace_first_str(input_str):
    min_index = 999999999
    first_word = None
    for word in WORD_TO_DIGIT.keys():
        word_index = input_str.find(word)
        if word_index != -1:
            if word_index < min_index:
                min_index = word_index
                first_word = word
    if first_word:
        return input_str.replace(first_word, WORD_TO_DIGIT[first_word], 1)
    return input_str


def replace_last_str(input_str):
    reversed_input = backwards(input_str)
    min_index = 999999999
    last_word = None
    for word in WORD_TO_DIGIT.keys():
        reversed_word = backwards(word)
        word_index = reversed_input.find(reversed_word)
        if word_index != -1:
            if word_index < min_index:
                min_index = word_index
                last_word = backwards(word)
    if last_word:
        return backwards(reversed_input.replace(last_word, WORD_TO_DIGIT[backwards(last_word)], 1))
    return input_str


def sum_all_numbers_p2(filename):
    total = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            first_str_replaced = replace_first_str(line.strip())
            last_str_replaced = replace_last_str(line.strip())
            total += int(first_numeric(first_str_replaced) + last_numeric(last_str_replaced))
    return total


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(sum_all_numbers_p1(input_file))
    elif part == "2":
        print(sum_all_numbers_p2(input_file))
