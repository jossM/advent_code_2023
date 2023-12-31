from datetime import datetime
from enum import IntEnum, auto
import heapq
from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt

raw_map = """
""".strip()  # fill this with input
part_1 = True
path_to_save_advancement = ''.rstrip('/')  # fill this
file_prefixes = 'advent_of_code_day_17_part_' + ('1' if part_1 else "2") + "_step_"


class Direction(IntEnum):  # using IntEnum enable using heapq which is key for perf
    right = 0
    down = 1
    left = 2
    up = 3


class PointState(NamedTuple):  # using NamedTuple enable using heapq which is key for perf
    x: int
    y: int
    prev_direction: Direction
    straight_line_count: int


if part_1:
    min_straight_line = 1
    max_straight_line = 3
else:
    min_straight_line = 4
    max_straight_line = 10

if __name__ == '__main__':
    map_layout = np.array([list(map(int, line)) for line in raw_map.split('\n')])
    optimal_heat_loss = {PointState(0, 0, d, 0): 0 for d in Direction}
    state_to_explore = [(0, PointState(0, 0, Direction.right, 0))]
    print(f"exploring map of size {map_layout.shape} - {map_layout.shape[0] * map_layout.shape[1]} tiles")

    # A modified version of Dijkstra algorithm will be used for that
    reached = np.zeros(map_layout.shape, dtype=np.uint)
    step = 0
    computation_start = datetime.now()
    min_heatloss = None
    
    while state_to_explore:

        # monitoring (to be more patient as first version run for almost 1h before usage of heapq)
        if step % 50000 == 0:
            plt.imshow(reached, cmap='hot', interpolation='nearest')
            plt.savefig(f'{path_to_save_advancement}/{file_prefixes}{step}.png')
            to_explore = np.zeros(map_layout.shape, dtype=bool)
            for _, s in state_to_explore:
                to_explore[s.x, s.y] = True
            plt.imshow(to_explore, cmap='hot', interpolation='nearest')
            plt.savefig(f'{path_to_save_advancement}/{file_prefixes}_to_explore_{step}.png')
            reached_tiles = np.count_nonzero(reached != 0)
            print(f'Studied {step} steps. Reached so far {reached_tiles} tiles'
                  f' ({int(reached_tiles / (map_layout.shape[0] * map_layout.shape[1]) * 100)} %) after'
                  f' {datetime.now() - computation_start} - {to_explore.sum()} in queue.')
        step += 1

        # cutoff optim once we have reached a first solution
        heat_loss_so_far, start_state = heapq.heappop(state_to_explore)
        if min_heatloss is not None and optimal_heat_loss[start_state] >= min_heatloss:
            continue

        potential_directions = set(Direction)

        # turning constraints
        if start_state.straight_line_count >= max_straight_line:
            # no more than x straight lines consecutives
            potential_directions -= {start_state.prev_direction}
        elif start_state.straight_line_count != 0:  # excludes starting point
            # no more than 90° turns
            if start_state.prev_direction == Direction.right:
                potential_directions -= {Direction.left}
            elif start_state.prev_direction == Direction.down:
                potential_directions -= {Direction.up}
            elif start_state.prev_direction == Direction.left:
                potential_directions -= {Direction.right}
            else:  # Direction.up
                potential_directions -= {Direction.down}

        for d in potential_directions:
            if d == start_state.prev_direction and start_state.straight_line_count > 0:  # start_state.straight_line_count is only the starting point
                step_size = 1
                next_straight_line_size = start_state.straight_line_count + 1
            else:
                step_size = min_straight_line
                next_straight_line_size = min_straight_line
            if d == Direction.right:
                next_location = (start_state.x, start_state.y+step_size)
            elif d == Direction.down:
                next_location = (start_state.x+step_size, start_state.y)
            elif d == Direction.left:
                next_location = (start_state.x, start_state.y-step_size)
            else:  # Direction.up:
                next_location = (start_state.x-step_size, start_state.y)

            # ensure we stay in the grid
            if (
                    next_location[0] < 0 or next_location[0] >= map_layout.shape[0]
                    or next_location[1] < 0 or next_location[1] >= map_layout.shape[1]
            ):
                continue

            # jump start direction changes by going the min straight line distance all at once
            if d == Direction.right:
                path_heat_loss = map_layout[start_state.x, start_state.y+1:next_location[1]+1].sum()
            elif d == Direction.down:
                path_heat_loss = map_layout[start_state.x+1:next_location[0]+1, start_state.y].sum()
            elif d == Direction.left:
                path_heat_loss = map_layout[start_state.x, next_location[1]:start_state.y].sum()
            else:  # Direction.up:
                path_heat_loss = map_layout[next_location[0]:start_state.x, start_state.y].sum()

            reached[next_location] += 1
            cost_to_reach_position = heat_loss_so_far + path_heat_loss
            next_state = PointState(*next_location, d, next_straight_line_size)

            # cut off to ensure the exploration frontier advances and limits exploration of inner pathes that can't be optimum
            if next_state in optimal_heat_loss and optimal_heat_loss[next_state] <= cost_to_reach_position:
                continue
            optimal_heat_loss[next_state] = cost_to_reach_position

            # cut off to find the optimum
            if next_state.x == map_layout.shape[0] - 1 and next_state.y == map_layout.shape[1] - 1 and (
               min_heatloss is None or cost_to_reach_position < min_heatloss
            ):
                min_heatloss = cost_to_reach_position
            heapq.heappush(state_to_explore, (cost_to_reach_position, next_state))  # heapq usage is key for perf

    # Technically at this point we are all done but it's nice to see the actual path.
    print(f"Finished in {step} steps after exploring {np.count_nonzero(reached!=0)} tiles ({np.count_nonzero(reached!=0)/(map_layout.shape[0] * map_layout.shape[1]) * 100} %)")
    print(f"Minimum heat loss path found with {min_heatloss} in {datetime.now() - computation_start}")

    # Nice to have for analysis
    # display the actual path
    path = np.zeros(map_layout.shape, dtype=bool)
    for d in Direction:
        for line_length in range(max_straight_line + 1):
            new_state = PointState(map_layout.shape[0]-1, map_layout.shape[1]-1, d, line_length)
            if optimal_heat_loss.get(new_state) == min_heatloss:
                end_state = new_state
                break
    start_state = end_state
    current_total_heat_loss = optimal_heat_loss[start_state]
    turn_points = [((end_state.x, end_state.y), current_total_heat_loss)]
    while (start_state.x, start_state.y) != (0, 0):
        if start_state.prev_direction == Direction.right:
            path_heat_loss = map_layout[start_state.x, start_state.y-start_state.straight_line_count+1:start_state.y+1].sum()
            new_location = (start_state.x, start_state.y-start_state.straight_line_count)
            for i in range(start_state.straight_line_count):
                path[start_state.x, start_state.y-i] = True
        elif start_state.prev_direction == Direction.down:
            path_heat_loss = map_layout[start_state.x-start_state.straight_line_count+1:start_state.x+1, start_state.y].sum()
            new_location = (start_state.x-start_state.straight_line_count, start_state.y)
            for i in range(start_state.straight_line_count):
                path[start_state.x-i, start_state.y] = True
        elif start_state.prev_direction == Direction.left:
            path_heat_loss = map_layout[start_state.x, start_state.y:start_state.y+start_state.straight_line_count].sum()
            new_location = (start_state.x, start_state.y+start_state.straight_line_count)
            for i in range(start_state.straight_line_count):
                path[start_state.x, start_state.y+i] = True
        else:  # Direction.up:
            path_heat_loss = map_layout[start_state.x:start_state.x+start_state.straight_line_count, start_state.y].sum()
            new_location = (start_state.x + start_state.straight_line_count, start_state.y )
            for i in range(start_state.straight_line_count):
                path[start_state.x+i, start_state.y] = True
        current_total_heat_loss -= path_heat_loss
        turn_points.insert(0, (new_location, current_total_heat_loss))
        for d in Direction:
            if d == start_state.prev_direction:
                continue
            for line_length in range(max_straight_line+1):
                new_state = PointState(*new_location, d, line_length)
                if optimal_heat_loss.get(new_state) == current_total_heat_loss:
                    start_state = new_state
                    break
    plt.imshow(path, cmap='hot', interpolation='nearest')
    plt.savefig(f'{path_to_save_advancement}/{file_prefixes}optimal_path.png')
    print('Optimal path:\n' + '\n'.join(map(lambda i: f"Point {i[0]} - heat loss {i[1]}", turn_points)))
