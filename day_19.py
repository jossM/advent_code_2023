from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import Union, Dict, Tuple, List, Optional

raw_input = """""".strip()
part_1 = True


class Outcome(Enum):
    Accepted = "A"
    Refused = "R"


@dataclass
class Rule:
    applied_on_symbol: str
    inferior: bool
    limit: int

    if_true: Union["Rule", Outcome, "str"]
    otherwise: Union["Rule", Outcome, "str"]


def parse_rule(rule_str: str) -> Tuple[Rule, str]:
    end_criteria_index = rule_str.index(":")
    criteria = rule_str[:end_criteria_index]
    inferior_operand = '<' in criteria
    applied_on_symbol, limit = criteria.split("<" if inferior_operand else '>')
    limit = int(limit)
    raw_if_true = rule_str[end_criteria_index+1:].split(',')[0]
    if ':' in raw_if_true:
        if_true_rule, remainder = parse_rule(rule_str[end_criteria_index+1:])
    else:
        remainder = rule_str[end_criteria_index + 1 + len(raw_if_true) + 1:]
        try:
            if_true_rule = Outcome(raw_if_true)
        except ValueError:
            if_true_rule = raw_if_true
    raw_otherwise = remainder.split(",")[0]
    if ':' in raw_otherwise:
        otherwise_rule, unparsed_str = parse_rule(remainder)
    else:
        unparsed_str = remainder[len(raw_otherwise)+2:]
        try:
            otherwise_rule = Outcome(raw_otherwise)
        except ValueError:
            otherwise_rule = raw_otherwise
    return (
        Rule(
            applied_on_symbol=applied_on_symbol,
            inferior=inferior_operand,
            limit=limit,
            if_true=if_true_rule,
            otherwise=otherwise_rule,
        ),
        unparsed_str
    )


def evaluate_rule(data: Dict[str, int], rule: Rule) -> Union[str, Outcome]:
    if rule.inferior:
        if data[rule.applied_on_symbol] < rule.limit:
            case = rule.if_true
        else:
            case = rule.otherwise
    else:
        if data[rule.applied_on_symbol] > rule.limit:
            case = rule.if_true
        else:
            case = rule.otherwise
    if isinstance(case, Rule):
        return evaluate_rule(data, case)
    else:
        return case


@dataclass
class Range:
    start: Optional[int]
    end: Optional[int]


def evaluate_rule_on_range(data: Dict[str, Range], rule: Rule) -> List[Tuple[Dict[str, Range], Union[Outcome, str]]]:
    symbol_range = data[rule.applied_on_symbol]
    if rule.inferior:
        applied_on_symbol_parts = [
            (Range(symbol_range.start, rule.limit - 1), rule.if_true),
            (Range(rule.limit, symbol_range.end), rule.otherwise)
        ]
    else:
        applied_on_symbol_parts = [
            (Range(symbol_range.start, rule.limit), rule.otherwise),
            (Range(rule.limit + 1, symbol_range.end), rule.if_true)
        ]
    # filtering absurd cases introduced above
    applied_on_symbol_parts = [(r, case) for r, case in applied_on_symbol_parts if r.start is None or r.end is None or r.start <= r.end]

    results = []
    for r, case in applied_on_symbol_parts:
        part = dict(**{k: v for k, v in data.items() if k != rule.applied_on_symbol},
                    **{rule.applied_on_symbol: r})
        if isinstance(case, Rule):
            results.extend(evaluate_rule_on_range(part, case))
        else:
            results.append((part, case))
    return results


if __name__ == '__main__':
    all_raw_rules, all_raw_parts = raw_input.split('\n\n')
    rules_index: Dict[str, Rule] = OrderedDict()
    for raw_rule in all_raw_rules.split("\n"):
        rule_name, raw_rule_content = raw_rule.strip("} ").split("{")
        rules_index[rule_name] = parse_rule(raw_rule_content)[0]

    if part_1:
        all_parts = []
        for raw_part in all_raw_parts.split("\n"):
            line_data = {}
            for part in raw_part[1:-1].split(","):
                key, value = part.split("=")
                line_data[key] = int(value)
            all_parts.append(line_data)

        total = 0
        first_rule_key, first_rule = 'in', rules_index['in']
        for part in all_parts:
            rule = first_rule
            applied_rules = [first_rule_key]
            while True:
                outcome = evaluate_rule(part, rule)
                if isinstance(outcome, Outcome):
                    break
                else:
                    rule = rules_index[outcome]
                    applied_rules.append(outcome)
            if outcome == Outcome.Accepted:
                total += sum(part.values())
    else:
        outcome_per_range = []
        # 0 and 4000 appear in instructions on the site
        ranges_rule_pair_to_study = [({key: Range(1, 4000) for key in ("x", "m", "a", "s")}, 'in', [])]
        while ranges_rule_pair_to_study:
            new_ranges_to_study = []
            for r, rule_key, key_pass in ranges_rule_pair_to_study:
                next_key_pass = key_pass + [rule_key]
                all_outcomes = evaluate_rule_on_range(r, rules_index[rule_key])
                outcome_per_range.extend([(studied_range, outcome, key_pass + next_key_pass)
                                          for studied_range, outcome in all_outcomes if isinstance(outcome, Outcome)])
                new_ranges_to_study.extend([(studied_range, outcome, next_key_pass)
                                            for studied_range, outcome in all_outcomes if not isinstance(outcome, Outcome)])
            ranges_rule_pair_to_study = new_ranges_to_study

        print('\n'.join(map(repr, outcome_per_range)))
        total = 0
        for range_per_key, outcome, key_pass in outcome_per_range:
            if outcome == Outcome.Refused:
                continue
            if any(r.start is None or r.end is None for r in range_per_key.values()):
                raise ValueError(f"Range {range_per_key} was accepted but has infinite size (rules {key_pass})")
            combinations = 1
            for r in range_per_key.values():
                combinations *= r.end - r.start + 1
            total += combinations
    print(f"Found total of {total}")

