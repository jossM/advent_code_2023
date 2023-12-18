raw_races = """"""  # fill this with input

raw_times, raw_distances = raw_races.split("\n")

# part_1 
all_race_times = list(map(int, filter(bool, raw_times.split(':')[1].split())))
all_race_distances = list(map(int, filter(bool, raw_distances.split(':')[1].split())))

solution_products = 1
for race_index, (race_time, race_distance) in enumerate(zip(all_race_times, all_race_distances)):
    record_solutions = sum(int((race_time - load_time) * load_time > race_distance) for load_time in range(race_time))
    print(f"Race {race_index}, {record_solutions} solution(s)")
    solution_products *= record_solutions
print(f"part1 solution : {solution_products}")

# part 2
  import math

race_time = int("".join(raw_times.split(':')[1].split()))
race_distance = int("".join(raw_distances.split(':')[1].split()))
print(f"race time: {race_time}, distance {race_distance}")
# distance compared to record = (race_time - load_time) * load_time - race_distance
delta = (race_time ** 2 - 4 * race_distance)
if delta < 0:
    solution_cout = 0
elif delta == 0:
    solution_cout = 1 if float(int(race_time / 2.)) == race_time / 2. else 0  # number of millisecond is not reachable on implied descreet spectrum 
else:  # delta > 0
    equation_roots = (race_time - math.sqrt(delta)) / 2., (race_time + math.sqrt(delta)) / 2.
    print(f"square roots are {equation_roots} for delta {delta}")
    solution_cout = math.floor(equation_roots[1]) - math.ceil(equation_roots[0]) + 1
print(solution_cout)
