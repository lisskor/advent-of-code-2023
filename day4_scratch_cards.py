import sys


def read_file(filename):
    all_cards = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh.readlines():
            line = line.strip()
            p1, p2 = line.split("|")
            card_id = int(p1.split(":")[0].split(" ")[-1])
            winning = [int(n) for n in p1.split(":")[1].split(" ") if n]
            have = [int(n) for n in p2.split(" ") if n]
            all_cards.append([card_id, winning, have])
    return all_cards


def calculate_points(cards):
    points = 0
    for card in cards:
        card_id, winning, have = card
        winning_numbers = set(winning) & set(have)
        if winning_numbers:
            points += 2 ** (len(winning_numbers) - 1)
    return points


class CardSet:
    def __init__(self, input_lists):
        self.initial_cards = {item[0]: ScratchCard(item) for item in input_lists}
        self.unprocessed_cards = {card_id: 1 for card_id in self.initial_cards}
        self.all_cards = {card_id: 1 for card_id in self.initial_cards}

    def generate_cards(self):
        while sum([self.unprocessed_cards[k] for k in self.unprocessed_cards]) > 0:
            current_id = max(self.unprocessed_cards, key=self.unprocessed_cards.get)
            current_card = self.initial_cards[current_id]

            for i in range(current_card.matches):
                self.all_cards[current_card.id + i + 1] += self.unprocessed_cards[current_id]
                self.unprocessed_cards[current_card.id + i + 1] += self.unprocessed_cards[current_id]

            self.unprocessed_cards[current_id] = 0
        return sum([self.all_cards[k] for k in self.all_cards])


class ScratchCard:
    def __init__(self, input_list):
        self.id, self.winning, self.have = input_list
        self.matches = len(set(self.winning) & set(self.have))


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(calculate_points(read_file(input_file)))
    elif part == "2":
        print(CardSet(read_file(input_file)).generate_cards())
