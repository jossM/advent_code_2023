import re

cards = list(filter(bool, """""".split("\n"))) # fill this with input

num_regex = re.compile('\d+')

# part 1
total = 0
for raw_card in cards:
    raw_winning_numbers, raw_played_number = raw_card.split(":")[-1].split("|")
    winning_numbers = set(map(lambda m: int(m.group()), num_regex.finditer(raw_winning_numbers)))
    played_numbers = list(map(lambda m: int(m.group()), num_regex.finditer(raw_played_number)))
    card_matches = [n for n in played_numbers if n in winning_numbers]  # supposes same number twice on card count twice
    if card_matches:
        total += 2**(len(card_matches)-1)
print(total)

# part 2
from collections import defaultdict

card_count = defaultdict(lambda:1)
for i, raw_card in enumerate(cards):
    raw_winning_numbers, raw_played_number = raw_card.split(":")[-1].split("|")
    winning_numbers = set(map(lambda m: int(m.group()), num_regex.finditer(raw_winning_numbers)))
    played_numbers = list(map(lambda m: int(m.group()), num_regex.finditer(raw_played_number)))
    card_matches = [n for n in played_numbers if n in winning_numbers]
    if not card_matches:
        continue
    for j in range(len(card_matches)):
        card_count[i + j + 1] += card_count[i]
print(sum(card_count[i] for i in range(len(cards))))
  
