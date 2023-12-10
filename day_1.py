
calibration_lines = """""".split("\n") # todo : fill this with input from advent code 
# for part 1 just remove the letter ones
chars_value = {"one": 1, "1": 1, 
               "two": 2, "2": 2, 
               "three": 3, "3": 3,
               "four": 4, "4": 4,
               "five": 5, "5": 5,
               "six": 6, "6": 6,
               "seven": 7, "7": 7,
               "eight": 8, "8": 8,
               "nine": 9, "9": 9,
               "zero": 0, "0": 0}
total = 0
for print_i, line in enumerate(calibration_lines):
    match = []
    for i in range(len(line)):
        matched_line_chars = [chars for chars in chars_value if line[i:].startswith(chars)]
        if matched_line_chars:
            match.append(matched_line_chars[0])
            break
    for i in range(len(line)):
        if i == 0:
            matched_line_chars = [chars for chars in chars_value if line.endswith(chars)]
        else:
            matched_line_chars = [chars for chars in chars_value if line[:-i].endswith(chars)]
        if matched_line_chars:
            match.append(matched_line_chars[0])
            break
    total += chars_value[match[0]] * 10 + chars_value[match[-1]]
print(total)
