import sys


RED = 12
GREEN = 13
BLUE = 14


def read_file(filename):
    all_games = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh.readlines():
            all_games.append(Game(line.strip()))
    return all_games


def game_is_possible(game, red, green, blue):
    for step in game.steps:
        if step['red'] > red or step['green'] > green or step['blue'] > blue:
            return False
    return True


class Game:
    def __init__(self, input_str):
        game, game_steps = input_str.strip().split(":")
        self.game_id = int(game.split(" ")[1])
        game_steps = game_steps.split(";")
        self.steps = []
        for step in game_steps:
            count_dict = {'red': 0, 'green': 0, 'blue': 0}
            for count in step.split(","):
                for color in count_dict:
                    if count.endswith(color):
                        count_dict[color] = int(count.split(" ")[1])
            self.steps.append(count_dict)
        self.min_set_power = self.power()

    def power(self):
        min_cubes = {'red': 0, 'green': 0, 'blue': 0}
        for step in self.steps:
            for color in step:
                if step[color] > min_cubes[color]:
                    min_cubes[color] = step[color]
        return min_cubes['red'] * min_cubes['green'] * min_cubes['blue']


def sum_possible_game_ids(filename):
    result = 0
    games = read_file(filename)
    for game in games:
        if game_is_possible(game, RED, GREEN, BLUE):
            result += game.game_id
    return result


def sum_min_set_powers(filename):
    result = 0
    games = read_file(filename)
    for game in games:
        result += game.min_set_power
    return result


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(sum_possible_game_ids(input_file))
    elif part == "2":
        print(sum_min_set_powers(input_file))
