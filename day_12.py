from dataclasses import dataclass, asdict
from datetime import datetime
from itertools import chain
from functools import cache
import re
from typing import Tuple, Iterable

PatternSpec = Tuple[int, ...]

raw_spring_patterns = list(filter(bool, """""".split("\n"))) # fill this with input
part_1 = False


block_pattern = re.compile("#+")


def deduce_pattern(spec: PatternSpec, spec_to_remove: PatternSpec) -> PatternSpec:
    if not spec_to_remove:
        return spec
    if spec_to_remove[-1] == spec[len(spec_to_remove) - 1]:
        return spec[len(spec_to_remove):]
    return tuple(chain([spec[len(spec_to_remove) - 1] - spec_to_remove[-1]], spec[len(spec_to_remove):]))


@cache
def max_spec_part_in_pattern(pattern_part: str, spec: PatternSpec) -> PatternSpec:
    """Find the maximum spec that can be fitted in a given pattern."""
    if not spec:
        return spec

    max_broken_spec = tuple(group.end() - group.start() for group in block_pattern.finditer(pattern_part.replace('?', "#")))
    spec_iterator = iter(max_broken_spec)
    max_spec = []
    try:
        current_spec = next(spec_iterator)
        last_group_size_too_small = False
        group_size = 0
        for group_size in max_broken_spec:
            last_group_size_too_small = False
            while True:
                if current_spec < group_size:
                    max_spec.append(current_spec)
                    group_size -= current_spec + 1
                    current_spec = next(spec_iterator)
                elif current_spec == group_size:
                    max_spec.append(current_spec)
                    current_spec = next(spec_iterator)
                    break
                else:
                    last_group_size_too_small = True
                    break
        if last_group_size_too_small and group_size:
            max_spec.append(group_size)
    except StopIteration:
        return spec
    return tuple(max_spec)


def spec_range(min_spec: PatternSpec, max_spec: PatternSpec) -> Iterable[PatternSpec]:
    last_comparable_index = len(min_spec) - 1
    if (
            len(max_spec) < len(min_spec)
            or min_spec[:max(last_comparable_index, 0)] != max_spec[:max(last_comparable_index, 0)]
            or (min_spec and min_spec[last_comparable_index] > max_spec[last_comparable_index])
    ):
        raise ValueError(f"min spec is not lower than max_spec:  {min_spec} > {max_spec}")
    max_spec = list(max_spec)
    if not min_spec:
        yield tuple()
    for spec_index in range(max(last_comparable_index, 0), len(max_spec)):
        min_range = 1 if spec_index != last_comparable_index or not min_spec else min_spec[last_comparable_index]
        for last_elem_value in range(min_range, max_spec[spec_index] + 1):
            yield tuple(max_spec[:spec_index] + [last_elem_value])


@dataclass(frozen=True)
class PatternCount:
    starts_with_dot: int = 0
    ends_with_dot: int = 0
    dot_on_sides: int = 0
    no_dot_on_sides: int = 0

    def __int__(self):
        return sum(asdict(self).values())

    def __bool__(self):
        return bool(int(self))

    def __add__(self, other: "PatternCount"):
        return PatternCount(**{k: getattr(other, k) + v for k, v in asdict(self).items()})


ZERO_PATTERN = PatternCount()


@cache
def count_pattern(spring_pattern: str) -> PatternCount:
    if spring_pattern.startswith(".") and spring_pattern.endswith("."):
        return PatternCount(dot_on_sides=1)
    elif spring_pattern.startswith("."):
        return PatternCount(starts_with_dot=1)
    elif spring_pattern.endswith("."):
        return PatternCount(ends_with_dot=1)
    return PatternCount(no_dot_on_sides=1)


@cache
def find_patterns(spring_pattern: str, broken_springs_spec: PatternSpec) -> PatternCount:
    # Recursivity out conditions :
    question_count = spring_pattern.count("?")
    if question_count == 0:
        if tuple(block.end() - block.start() for block in block_pattern.finditer(spring_pattern)) == broken_springs_spec:
            return count_pattern(spring_pattern)  # tuple([spring_pattern])
        else:
            return ZERO_PATTERN  # tuple()

    if broken_springs_spec:  # if we have a spec, check special cases that simplify solutions
        if spring_pattern.count("#") > sum(broken_springs_spec):
            return ZERO_PATTERN  # tuple()
        if sum(broken_springs_spec) + len(broken_springs_spec) - 1 > len(spring_pattern):
            return ZERO_PATTERN  # tuple()
        if len(broken_springs_spec) == 1:
            if "#" * broken_springs_spec[0] in spring_pattern:
                return count_pattern(spring_pattern.replace("?", "."))
            if broken_springs_spec[0] == len(spring_pattern):
                if '.' not in spring_pattern:
                    return PatternCount(no_dot_on_sides=1)  # tuple([spring_pattern.replace("?", "#")])
                else:
                    return ZERO_PATTERN  # tuple()

    else:  # broken_springs_spec is empty no # block expected
        if "#" not in spring_pattern:
            return PatternCount(dot_on_sides=1)  # tuple([spring_pattern.replace("?", ".")])
        else:
            return ZERO_PATTERN  # tuple()

    if len(spring_pattern) == 1:
        if len(broken_springs_spec) > 1 or broken_springs_spec[0] > 1:
            return ZERO_PATTERN  # tuple()
        if broken_springs_spec and spring_pattern != ".":
            return count_pattern(spring_pattern.replace("?", "#"))
        if spring_pattern == "." and not broken_springs_spec:
            return count_pattern(spring_pattern.replace("?", "."))
        return ZERO_PATTERN  # tuple()

    result: PatternCount = ZERO_PATTERN  # : [str] = []

    # Recursive logic : split the pattern in two and see which part of the spec can be where
    middel = int(len(spring_pattern) / 2)
    pattern_part_left, pattern_part_right = spring_pattern[:middel], spring_pattern[middel:]
    max_left_pattern = max_spec_part_in_pattern(pattern_part_left, broken_springs_spec)
    max_right_pattern_inverted = max_spec_part_in_pattern(pattern_part_right[::-1], broken_springs_spec[::-1])
    min_left_pattern = deduce_pattern(spec=broken_springs_spec[::-1], spec_to_remove=max_right_pattern_inverted)[::-1]
    for spec_left in spec_range(min_left_pattern, max_left_pattern):
        spec_right = broken_springs_spec[len(spec_left):]
        # split is not supposed to be in the middle of a group
        if not spec_left or spec_left[-1] == broken_springs_spec[len(spec_left) - 1]:
            left = find_patterns(pattern_part_left, spec_left)
            if not left:
                continue
            right = find_patterns(pattern_part_right, spec_right)
            if not right:
                continue
            found_patterns = PatternCount(
                starts_with_dot=
                    (left.starts_with_dot + left.dot_on_sides) * right.starts_with_dot + left.dot_on_sides * right.no_dot_on_sides,
                    # .[]? * .[]# + .[]. * #[]#
                dot_on_sides=
                    (left.starts_with_dot + left.dot_on_sides) * right.dot_on_sides + left.dot_on_sides * right.ends_with_dot,
                    # .[]? * .[]. + .[]. * #[].
                ends_with_dot=
                    (left.ends_with_dot + left.no_dot_on_sides) * right.dot_on_sides + left.ends_with_dot * right.ends_with_dot,
                    # #[]? * .[]. + #[]. * #[].
                no_dot_on_sides=(left.ends_with_dot + left.no_dot_on_sides) * right.starts_with_dot + left.ends_with_dot * right.no_dot_on_sides,
                    # #[]? * .[]# + #[]. * #[]#
            )
            result += found_patterns
            #.extend(
            #    found_left + found_right
            #    for found_left in left
            #    for found_right in right
            #    if not found_left.endswith("#") or found_right.startswith(".")
            #)
            continue
        # a group is supposed to be split in the two parts
        imposed_left, imposed_right = "." + "#" * spec_left[-1], "#" * (broken_springs_spec[len(spec_left) - 1] - spec_left[-1]) + "."
        spec_is_possible = True
        for imposed, on_side_pattern in [(imposed_left[::-1], pattern_part_left[::-1]), (imposed_right, pattern_part_right)]:
            if "." in on_side_pattern[:len(imposed) - 1]:
                spec_is_possible = False
                break
            if len(on_side_pattern) >= len(imposed) and on_side_pattern[len(imposed) - 1] == "#":
                spec_is_possible = False
                break
            if len(imposed) - 1 > len(on_side_pattern):
                spec_is_possible = False
                break
        if not spec_is_possible:
            continue
        truncated_left = pattern_part_left[:-len(imposed_left)]
        if not truncated_left and len(spec_left) <= 1:
            left = count_pattern(imposed_left[-len(pattern_part_left):])
        else:
            left = find_patterns(truncated_left, spec_left[:-1])
        if not left:
            continue
        truncated_right = pattern_part_right[len(imposed_right):]
        if not truncated_right and not spec_right:
            right = count_pattern(imposed_right[:len(pattern_part_right)])
        else:
            right = find_patterns(pattern_part_right[len(imposed_right):], spec_right)
        if not right:
            continue
        found_patterns = PatternCount(
            starts_with_dot=(left.starts_with_dot + left.dot_on_sides) * (right.starts_with_dot + right.no_dot_on_sides),
            # .[]? * ?[]#
            dot_on_sides=
            (left.starts_with_dot + left.dot_on_sides) * (right.dot_on_sides + right.ends_with_dot),
            # .[]? * ?[].
            ends_with_dot=
            (left.ends_with_dot + left.no_dot_on_sides) * (right.dot_on_sides + right.ends_with_dot),
            # #[]? * ?[].
            no_dot_on_sides=(left.ends_with_dot + left.no_dot_on_sides) * (right.starts_with_dot + right.no_dot_on_sides),
            # #[]? * ?[]#
        )

        result += found_patterns
        #.extend(
        #   found_left + imposed_left[-len(pattern_part_left):] + imposed_right[:len(pattern_part_right)] + found_right
        #   for found_left in all_patterns_found_left
        #    for found_right in all_patterns_found_right
        #)
    return result


multiplier = 1 if part_1 else 5
if __name__ == "__main__":
    total = 0
    start = datetime.now()
    print("Start now")
    for pattern, raw_spec in map(lambda s: s.split(), raw_spring_patterns):
        spec = list(map(lambda s: int(s), raw_spec.split(',')))
        pattern = '?'.join([pattern] * multiplier)
        spec *= multiplier
        print(f"Studying {pattern}, {spec}")
        possibilities = find_patterns(pattern, tuple(spec))
        total += int(possibilities)
    print(f"Found {total} in {datetime.now() - start}")
    print(f'Total {total}')  # Found 10^13 combinations in 0:00:20.313506

