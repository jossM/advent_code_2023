from collections import OrderedDict

raw_initial_instructions = """""".strip()  # fill this with input
part_1 = True


def hash_string(input_str: str) -> int:
    str_hash = 0
    for c in input_str:
        str_hash += ord(c)
        str_hash *= 17
        str_hash %= 256
    return str_hash


# case basically explained what needed to be coded. Code hasn't been refined much since there was no need
all_instructions = raw_initial_instructions.split(',')
if part_1:
    total = 0
    for instruction in all_instructions:
        total += hash_string(instruction)
    print(total)
else:
    boxes_states = [OrderedDict() for _ in range(256)]
    for instruction in all_instructions:
        if instruction[-1] == "-":
            label = instruction[:-1]
            box_hash = hash_string(label)
            boxes_states[box_hash].pop(label, None)
        else:
            try:
                label, lens = instruction.split("=")
            except ValueError:
                raise ValueError(f"Invalid instruction {instruction}")
            box_hash = hash_string(label)
            boxes_states[box_hash][label] = int(lens)

    total = 0
    for i in range(len(boxes_states)):
        for j, lens in enumerate(boxes_states[i].values()):
            total += (i+1) * (j+1) * lens
    print(total)
