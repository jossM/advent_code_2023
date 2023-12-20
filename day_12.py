from typing import List, Tuple

_re_patterns = dict()


def describe_pattern(springs_pattern: str) -> List[Tuple[str, int]]:
    group_description = []
    while springs_pattern:
        start_char = springs_pattern[0]
        if start_char not in _re_patterns:
            _re_patterns[start_char] = re.compile(springs_pattern[0]) + "+")
        re_pattern_matcher = _re_patterns[start_char]
        start_group = next(re_pattern_matcher.finditer(springs_pattern))
        group_description.append((start_char, start_group.end()))
        springs_pattern = springs_pattern[start_group.end():]
    return group_description

def start_pattern_could_match(springs_pattern: List[Tuple[str, int]], broken_springs_spec: List[int]) -> bool:
    next_group_index = None
    broken_spring_pattern = []
    has_unknown_slots = False
    for group_index, (char, group_size) in enumerate(springs_pattern):
        if char == "#":
            broken_spring_pattern.append(group_size)
            next_group_index = group_index + 1
        if char == "?":
            has_unknown_slots = True
            break
  
    if not has_unknown_slots:
        return broken_spring_pattern == broken_springs_spec
    
    exact_match_length = len(broken_spring_pattern)
    if springs_pattern[next_group_index][0] == "?":
        exact_match_length -= 1
    
    return all([
        broken_spring_pattern[:exact_match_length] == broken_springs_spec[:exact_match_length],
        broken_spring_pattern[exact_match_length - 1] <= broken_springs_spec[exact_match_length - 1]
    )

# wip
