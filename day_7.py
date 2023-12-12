from collections import (
    OrderedDict,  # dict are ordered on the latest version of python but it's nice to make things explicit
    Counter
)

raw_games = """"""

# part 1
games = [(game_line.split()[0], int(game_line.split()[1])) for game_line in raw_games.split("\n")]

cards_strength = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

hand_patterns = OrderedDict([
  ("High card", lambda hand: Counter(hand).most_common(1)[0][1] == 5),
  ("Four of a kind", lambda hand: Counter(hand).most_common(1)[0][1] == 4),
  ("Full house", lambda hand: [card_count for _, card_count in Counter(hand).most_common(2)] == [3, 2]),
  ("Three of a kind", lambda hand: Counter(hand).most_common(1)[0][1] == 3),
  ("Two pair", lambda hand: [card_count for _, card_count in Counter(hand).most_common(2)] == [2, 2]),
  ("One pair", lambda hand: Counter(hand).most_common(1)[0][1] == 2),
  ("High card", lambda hand: Counter(hand).most_common(1)[0][1] == 1),
])

def attribute_score(hand: str) -> int:
    print("Studying hand : " + hand)
    score = 0
    for pattern_index, (pattern_name, validate_pattern) in enumerate(hand_patterns.items()):
        if validate_pattern(hand):
            print(pattern_name + " found")
            score += (len(hand_patterns) - pattern_index) * 100**5
            break
    for card_index, card in enumerate(hand):
        score += cards_strength.index(card) * 100 ** (4 - card_index)
    print(score)
    return score

sorted_games = sorted(games, key=lambda g:attribute_score(g[0]), reverse=True)
total = sum(hand_rank*bid for hand_rank, (_, bid) in enumerate(sorted_games))
print(total)
