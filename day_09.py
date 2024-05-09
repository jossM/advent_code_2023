raw_instability_report = """"""  # fill this
part_1 = True

instability_lines = [list(map(int, raw_line.split())) for raw_line in filter(bool, raw_instability_report.split("\n"))]

next_line_value = []
for instabilities in instability_lines:
    derived_instabilities = [instabilities]
    while not all(i == 0 for i in derived_instabilities[-1]):
        derived_instabilities.append([derived_instabilities[-1][i + 1] - derived_instabilities[-1][i] for i in
                                      range(len(derived_instabilities[-1]) - 1)])
    print("_" * 10 + "\nfirst derived_instabilities")
    for l in derived_instabilities:
        print(l)

    derived_instabilities[-1].append(0)
    for i in range(len(derived_instabilities) - 1):
        computed_line_index = len(derived_instabilities) - 1 - i - 1
        computed_line = derived_instabilities[computed_line_index]
        line_below = derived_instabilities[computed_line_index + 1]
        if part_1:
            computed_line.append(computed_line[-1] + line_below[-1])
        else:
            derived_instabilities[computed_line_index] = [computed_line[0] - line_below[0]] + computed_line
    print("next item")
    for l in derived_instabilities:
        print(l)
    next_line_value.append(derived_instabilities[0][-1 if part_1 else 0])

print(sum(next_line_value))
