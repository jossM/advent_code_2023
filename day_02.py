all_games = list(filter(bool, """""".split("\n"))) # fill this with input

# part 1
max_per_color = {
    'red': 0,
    'green': 0,
    'blue': 0,
} # adapt values to instructions
total = 0
for i, game_info in enumerate(g.split(':')[-1] for g in all_games):
    max_game_colors = {}
    parts = [game_info]
    for split_char in ",;":
        parts = [s for p in parts for s in p.split(split_char)]
    for number, color in map(lambda p: list(filter(bool, p.split(" "))), parts):
        max_game_colors[color] = max(max_game_colors.get(color, 0), int(number))
    if all(max_game_count <= max_per_color.get(color, 0) for color, max_game_count in max_game_colors.items()):
        total += i + 1
print(total)

# part 2
total = 0
for i, game_info in enumerate(g.split(':')[-1] for g in all_games):
    max_game_colors = {}
    parts = [game_info]
    for split_char in ",;":
        parts = [s for p in parts for s in p.split(split_char)]
    for number, color in map(lambda p: list(filter(bool, p.split(" "))), parts):
        max_game_colors[color] = max(max_game_colors.get(color, 0), int(number))
    game_total = 1
    for color, min_bagged in max_game_colors.items():
        game_total *= min_bagged
    if max_game_colors:
        total += game_total
print(total)
