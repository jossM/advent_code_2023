from functools import cache
from typing import List, Tuple, Iterable

raw_spring_patterns = list(filter(bool, """""".split("\n"))) # fill this with input
part_1 = True


def describe_pattern(springs_pattern: str) -> Tuple[Tuple[str, int]]:
    group_description = []
    while springs_pattern:
        start_char = springs_pattern[0]
        start_group = next(re.finditer(re.escape(start_char) + "+", springs_pattern))
        group_description.append((start_char, start_group.end()))
        springs_pattern = springs_pattern[start_group.end():]
    return tuple(group_description)


def get_starting_pattern_match_index(springs_pattern: List[Tuple[str, int]], broken_springs_spec: List[int]) -> bool:
    broken_spring_pattern = []
    last_broken_group_index = None
    last_unknown_block = None
    
    for group_index, (char, group_size) in enumerate(springs_pattern):
        if char == "#":
            broken_spring_pattern.append(group_size)
            last_broken_group_index = group_index
        if char == "?":
            last_unknown_block = group_index
            break

    if last_unknown_block is None:
        if broken_spring_pattern == broken_springs_spec:
            return len(springs_pattern)
        else:
            return None

    question_count = sum(group_size for char, group_size in springs_pattern if char == "?")
    broken_count = sum(group_size for char, group_size in springs_pattern if char == "#")
    spec_count = sum(broken_springs_spec)
    if not broken_count <= spec_count <= broken_count + question_count:
        return None

    if last_broken_group_index is None:
        return last_unknown_block

    exact_match_length = len(broken_spring_pattern)
    if last_unknown_block == last_broken_group_index + 1:
        exact_match_length -= 1
    
    if (
            broken_spring_pattern[:exact_match_length] != broken_springs_spec[:exact_match_length]
            or len(broken_spring_pattern) > len(broken_springs_spec)
            or (exact_match_length != len(broken_spring_pattern) and broken_spring_pattern[exact_match_length] > broken_springs_spec[
        exact_match_length])
    ):
        return None
    if last_unknown_block == last_broken_group_index + 1:
        return last_broken_group_index
    return last_unknown_block


def simplify_groups(spring_pattern: Tuple[Tuple[str, int]]) -> Tuple[Tuple[str, int]]:
    result = []
    previous_group_char = None
    for group_char, group_size in spring_pattern:
        if group_char == previous_group_char:
            result[-1] = (group_char, group_size + result[-1][1] if group_char != "." else 1)
        elif group_size > 0:
            result.append((group_char, group_size if group_char != "." else 1))
            previous_group_char = group_char
    return tuple([(char, group_size) for i, (char, group_size) in enumerate(result) if i not in [0, len(result)-1] or char != "."])


@cache
def find_patterns(spring_pattern: Tuple[Tuple[str, int], ...], broken_springs_spec: Tuple[int, ...]) -> Iterable[str]:
    starting_match_index = get_starting_pattern_match_index(spring_pattern, broken_springs_spec)
    if starting_match_index is None:
        return
    if not any("?" == char for char, _ in spring_pattern):
        yield ''.join(char * group_size for char, group_size in spring_pattern)
        return
    first_question_group_index, question_group_size = next(
        (group_index, group_size) for group_index, (group_char, group_size) in enumerate(spring_pattern) if group_char == "?")
    
    matched_pattern = spring_pattern[:starting_match_index]
    truncated_broken_springs_spec = tuple(broken_springs_spec[:len([char for char, _ in matched_pattern if char == '#'])])
    for group_choice in [("#", 1), (".", 1)]:
        truncated_pattern = simplify_groups(
            list(spring_pattern[starting_match_index:first_question_group_index])
            + [group_choice, ('?', question_group_size - 1)]
            + list(spring_pattern[first_question_group_index + 1:])
        )
        
        for sub_pattern in find_patterns(truncated_pattern, truncated_broken_springs_spec):
            yield ''.join(char for char, _ in spring_pattern[:starting_match_index]) + sub_pattern

multiplier = 1 if part_1 else 5

total = 0
for pattern, raw_spec in map(lambda s: s.split(), raw_spring_patterns):
    spec = list(map(lambda s: int(s), raw_spec.split(',')))
    pattern = '?'.join([pattern] * multiplier)
    spec *= multiplier
    print(f"Studying {pattern}, {spec}")
    possibilities = len(list(find_patterns(simplify_groups(describe_pattern('?'.join(pattern for i in range(5)))), tuple(spec*5))))
    print(f"Found {possibilities} for pattern {pattern}")
    total += possibilities

# wip
