from enum import IntEnum
from typing import Dict, Union, Tuple

raw_connections = """
""".strip()
# solution only to part 1 as part 2 requires again a trick to assume the format of the generated circuit
# solution is basically to see the periodicity of the source of rx module and to do lcm on the periodicty


class Pulse(IntEnum):
    low = 0
    high = 1


class State:
    def __init__(self, new_state: Dict[str, Union["State", bool, Pulse, Dict]]):
        self._state = dict()
        for k, v in new_state.items():
            if isinstance(v, dict):
                v = State(v)
            self._state[k] = v

    def __getitem__(self, item):
        return self._state[item]

    def get(self, item, default=None):
        return self._state.get(item, default)

    def keys(self):
        return self._state.keys()

    def values(self):
        return self._state.values()

    def items(self):
        return self._state.items()

    def update(self, *args: dict, **kwargs):
        new_state = dict(self._state)
        if args:
            if len(args) > 1:
                raise ValueError("Only one dict can be passed")
            input_dict = args[0]
            intersection = set(input_dict.keys()).intersection(kwargs.keys())
            differences = ", ".join(f"{k} is set to both {input_dict[k]} and {kwargs[k]}"
                                    for k in intersection if input_dict[k] != kwargs[k])
            if differences:
                raise ValueError(f"Keys have been set to different values : {differences}")
            new_state.update(input_dict)
        new_state.update(**kwargs)
        return State(new_state)

    def __eq__(self, other):
        return isinstance(other, State) and other._state == self._state

    def __hash__(self):
        return tuple(map(hash, sorted(self._state.items(), key=lambda kv: kv[0])))

    def __repr__(self):
        return repr({k: repr(v) for k, v in self._state.items()})


def broadcast(connections: Dict[str, Tuple[str, ...]], state: State) -> Tuple[Tuple[Tuple[str, Pulse, str], ...], State]:
    signals = [("button", Pulse.low, "broadcaster")]
    signals_index = 0
    while signals_index < len(signals):
        source_module, pulse, module_name = signals[signals_index]
        signals_index += 1
        module_state = state.get(module_name)
        if module_state is None:  # broadcast module
            signals.extend([(module_name, pulse, mod) for mod in connections[module_name]])
        elif isinstance(module_state, bool):  # flipflop module
            if pulse == Pulse.high:
                continue
            signals.extend([(module_name, (Pulse.low if module_state else Pulse.high), mod)
                            for mod in connections[module_name]])
            state = state.update({module_name: not module_state})
        else:  # Conjunction module
            new_conjunction_state = module_state.update({source_module: pulse})
            state = state.update({module_name: new_conjunction_state})
            signals.extend([(module_name,
                             Pulse.low if all(last_input == Pulse.high for last_input in new_conjunction_state.values()) else Pulse.high,
                             mod)
                            for mod in connections[module_name]])
    return tuple(signals), state


if __name__ == '__main__':
    initial_state: Dict[str, Union[bool, Pulse, Dict]] = dict()
    conjunctions = []
    connections: Dict[str, Tuple[str, ...]] = {}
    for source_module, raw_destinations in map(lambda s: s.split(" -> "), raw_connections.split("\n")):
        if source_module.startswith("%"):
            source_module = source_module[1:]
            initial_state[source_module] = False
        elif source_module.startswith("&"):
            source_module = source_module[1:]
            conjunctions.append(source_module)
        else:  # broadcast
            pass
        connections[source_module] = tuple(raw_destinations.split(", "))

    connections.update({d: tuple() for all_destinations in connections.values() for d in all_destinations if d not in connections})

    for c in conjunctions:
        initial_state[c] = {source: Pulse.low for source, destinations in connections.items() if c in destinations}

    state = State(initial_state)

    print(f"connections: {connections}")
    low_signal_count = 0
    high_signal_count = 0
    for i in range(1000):
        # print("_" * 10)
        if i % 1000 == 0:
            print(f"Up to {i} button pushes")
        signals, state = broadcast(connections, state)
        push_low_signal_count = len([None for _, p, _ in signals if p == Pulse.low])
        low_signal_count += push_low_signal_count
        high_signal_count += (len(signals) - push_low_signal_count)
    print(f"total {low_signal_count} * {high_signal_count} = {low_signal_count * high_signal_count}")
    
