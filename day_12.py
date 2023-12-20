from typing import List, Tuple, Iterable

raw_spring_patterns = list(filter(bool, """""".split("\n"))) # fill this with input


def describe_pattern(springs_pattern: str) -> List[Tuple[str, int]]:
    group_description = []
    while springs_pattern:
        start_char = springs_pattern[0]
        start_group = next(re.finditer(springs_pattern[0]) + "+", springs_pattern))
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

def fuse_same_adjacent_groups(spring_pattern: List[Tuple[str, int]]) -> List[Tuple[str, int]:
    result = []
    previous_group_char = None
    for group_char, group_size in spring_pattern:
        if group_char == previous_group_char:
            result[-1] = (group_char, group_size + result[-1][1])
        elif group_size > 0:
            result.append(group_char, group_size)
            previous_group_char = group_char
    return result


def find_patterns(spring_pattern: List[Tuple[str, int]], broken_springs_spec: List[int]) -> Iterable[str]
    if not start_pattern_could_match(spring_pattern, broken_springs_spec):
        return
    if not any("?" == char for char, _ in raw_spring_pattern):
        yield ''.join(char * group_size for char, group_size in raw_spring_pattern)
        return
    first_question_group_index, question_group_size = next((group_index, group_size) for group_index, (group_char, group_size) in enumerate(spring_pattern) if group_char == "?" )
    if question_group_size > 1:
        remainging_question_group = [('?', question_group_size-1)]
    else:
        remainging_question_group = []
    
    for group_choice in [("#",1), (".",1)]:
        yield from find_patterns(fuse_same_adjacent_groups(
            spring_pattern[:first_question_group_index] 
            + [group_choice]
            + remainging_question_group
            + spring_pattern[first_question_group_index+1:]
        ))

