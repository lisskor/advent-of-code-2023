import sys
import numpy as np


class Schematic:
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf8') as fh:
            all_lines = [line.strip() for line in fh.readlines()]
        self.height = len(all_lines)
        self.width = len(all_lines[0])
        self.symbols_matrix = np.zeros((self.height, self.width))

        for line_num, line in enumerate(all_lines):
            symbol_indices = [i for i, char in enumerate(line) if (not char.isnumeric() and char != '.')]
            for index in symbol_indices:
                self.symbols_matrix[line_num, index] = 1

        self.numbers = []
        for line_num, line in enumerate(all_lines):
            num_as_str = ''
            for char_num, char in enumerate(line):
                if char.isnumeric():
                    num_as_str += char
                elif not char.isnumeric() and num_as_str:
                    self.numbers.append(Number(num_as_str, (line_num, char_num)))
                    num_as_str = ''
            if num_as_str:
                self.numbers.append(Number(num_as_str, (line_num, self.width)))

        self.part_numbers_sum = 0
        for number in self.numbers:
            if self.adjacent_to_symbol(number):
                self.part_numbers_sum += number.number

        self.asterisks_indices = np.argwhere(
                np.array([[char for char in line] for line in all_lines]) == "*"
        )

        self.gear_ratios_sum = 0
        for asterisk in self.asterisks_indices:
            self.gear_ratios_sum += self.adjacent_numbers_product(asterisk)

    def adjacent_to_symbol(self, number):
        adjacent_indices_rows = np.clip(
                [number.start_index[0] - 1,
                 number.start_index[0] + 2],
                0, self.height
        )
        adjacent_indices_cols = np.clip(
                [number.start_index[1] - 1,
                 number.start_index[1] + number.length + 1],
                0, self.width
        )
        adjacent_matrix = self.symbols_matrix[
                          adjacent_indices_rows[0]:adjacent_indices_rows[1],
                          adjacent_indices_cols[0]:adjacent_indices_cols[1]
                          ]
        if np.sum(adjacent_matrix) > 0:
            return True
        else:
            return False

    def adjacent_numbers_product(self, pos):
        adjacent_numbers = []
        adjacent_indices_rows = np.clip([pos[0] - 1, pos[0] + 1], 0, self.height)
        adjacent_indices_cols = np.clip([pos[1] - 1, pos[1] + 1], 0, self.width)
        for number in self.numbers:
            if len(adjacent_numbers) == 3:
                return 0
            if adjacent_indices_rows[0] <= number.start_index[0] <= adjacent_indices_rows[1]:
                for i in range(number.length):
                    if adjacent_indices_cols[0] <= number.start_index[1] + i <= adjacent_indices_cols[1]:
                        adjacent_numbers.append(number.number)
                        break

        if len(adjacent_numbers) == 2:
            return adjacent_numbers[0] * adjacent_numbers[1]
        return 0


class Number:
    def __init__(self, number_as_string, adding_pos):
        self.number = int(number_as_string)
        self.length = len(number_as_string)
        self.start_index = (adding_pos[0], adding_pos[1] - self.length)
        self.end_index = (adding_pos[0], adding_pos[1])

    def __repr__(self):
        return f"{self.number} @ {self.start_index}"


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    schematic = Schematic(input_file)
    if part == "1":
        print(schematic.part_numbers_sum)
    elif part == "2":
        print(schematic.gear_ratios_sum)
