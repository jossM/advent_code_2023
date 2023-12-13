from collections import (
    OrderedDict,  # dict are ordered on the latest version of python but it's nice to make things explicit
    Counter
)
from typing import Optional, Callable, Dict, List

raw_games = """"""
part_1 = False

games = [(game_line.split()[0], int(game_line.split()[1])) for game_line in raw_games.split("\n")]

cards_strength = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
if not part_1:
    cards_strength.pop(cards_strength.index('J'))
    cards_strength = ["J"] + cards_strength


def make_compute_dist_to_pattern_set(most_common_counts: List[int]):
    def compute_distance_to_pattern(hand: str) -> int:
        edit_distance = 0
        most_common_in_hand = Counter(hand).most_common(len(most_common_counts))
        if len(most_common_in_hand) < len(most_common_counts):
            most_common_in_hand = most_common_in_hand + [(None, 0)] * (len(most_common_counts) - len(most_common_counts))
        for (_, card_count), expected_count in zip(most_common_in_hand, most_common_counts):
            if expected_count < card_count:
                return -1
            edit_distance += expected_count - card_count
        return edit_distance

    return compute_distance_to_pattern


hand_patterns_distance: Dict[str, Callable[[str], Optional[int]]] = OrderedDict([
    ("Five of a kind", lambda hand: 5 - Counter(hand).most_common(1)[0][1]),
    ("Four of a kind", lambda hand: 4 - Counter(hand).most_common(1)[0][1]),
    ("Full house", make_compute_dist_to_pattern_set([3, 2])),
    ("Three of a kind", lambda hand: 3 - Counter(hand).most_common(1)[0][1]),
    ("Two pair", make_compute_dist_to_pattern_set([2, 2])),
    ("One pair", lambda hand: 2 - Counter(hand).most_common(1)[0][1]),
    ("High card", lambda hand: 0 if Counter(hand).most_common(1)[0][1] == 1 else -1),
])


def attribute_score(hand: str) -> int:
    score = 0
    for pattern_index, (pattern_name, compute_pattern_edit_distance) in enumerate(hand_patterns_distance.items()):
        if part_1:
            pattern_does_match = compute_pattern_edit_distance(hand) == 0
        else:
            j_count = hand.count('J')
            clean_hand = "".join(filter(lambda c: c != 'J', hand))
            if not clean_hand:
                pattern_does_match = True
            else:
                pattern_edit_distance = compute_pattern_edit_distance(clean_hand)
                pattern_does_match = 0 <= pattern_edit_distance <= j_count
        if pattern_does_match:
            score += (len(hand_patterns) - pattern_index) * 100 ** 5
            break

    for card_index, card in enumerate(hand):
        score += cards_strength.index(card) * 100 ** (4 - card_index)
    return score


sorted_games = sorted(games, key=lambda g: attribute_score(g[0]))
total = sum((hand_rank + 1)* bid for hand_rank, (_, bid) in enumerate(sorted_games))
print(total)
