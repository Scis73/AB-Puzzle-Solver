import sys
import math
import heapq

class Disks:
    def __init__(self, n, large_disks_data, small_disks_data):
        self.n = n
        self.large_disks = list(large_disks_data)
        self.unique_n = int(math.sqrt(n-1)) + 1
        self.fringe = []
        self.counter = 0
        initial_state = self.SmallDisks(list(small_disks_data))
        initial_state.g = 0
        initial_state.h = self.heuristic(initial_state)
        initial_state.f = initial_state.g + initial_state.h
        heapq.heappush(self.fringe, (initial_state.f, self.counter, initial_state))

    class SmallDisks:
        def __init__(self, small_disks_data):
            self.small_disks = small_disks_data
            self.zero_index = self.small_disks.index(0)
            self.trace_back_state = [small_disks_data]
            self.trace_back_move = []
            self.g = 0
            self.h = 0
            self.f = 0

    def heuristic(self, small_disks_state):
        disks = small_disks_state.small_disks
        violations = 0
        for i in range(self.n):
            current = disks[i]
            next_disk = disks[(i + 1) % self.n]
            if current == 0 or next_disk == 0:
                continue
            if current != next_disk:
                expected_next = (current % self.unique_n) + 1
                if next_disk != expected_next:
                    violations += 1
        return violations // 2

    def print_details(self):
        print("==================")
        print(f"System Size (N):    {self.n}")
        print(f"(Large Disks):      {self.large_disks}")
        print(f"(Unique n):         {self.unique_n}")
        print("==================")
    
    def get_valid_moves(self, small_disks_state):
        zero_index = small_disks_state.zero_index
        jump_distance = self.large_disks[zero_index]
        
        right_jump_index = (zero_index + jump_distance) % self.n
        left_jump_index  = (zero_index - jump_distance) % self.n
        right_neighbor   = (zero_index + 1) % self.n
        left_neighbor    = (zero_index - 1) % self.n
        
        if left_jump_index == left_neighbor: 
            return [[left_neighbor, right_neighbor],["left by 1","right by 1"]]

        return [[left_jump_index, left_neighbor, right_neighbor, right_jump_index], ["left by "+str(jump_distance), "left by 1", "right by 1", "right by "+str(jump_distance)]]

        
    def create_children(self, small_disks_state):
        children = []
        move_states = (self.get_valid_moves(small_disks_state))[0]
        move_made = (self.get_valid_moves(small_disks_state))[1]
        for move in move_states:
            children.append(self.move_disk(move, small_disks_state))
        return [children, move_made]

    def move_disk(self, target_i, small_disks_state):
        zero_index = small_disks_state.zero_index
        new_state = self.SmallDisks(list(small_disks_state.small_disks))
        new_state.small_disks[zero_index] = new_state.small_disks[target_i]
        new_state.small_disks[target_i] = 0
        new_state.zero_index = target_i
        new_state.g = small_disks_state.g + 1
        new_state.h = self.heuristic(new_state)
        new_state.f = new_state.g + new_state.h
        return new_state

    def is_solved(self, small_disks_state):
        zero_pos = small_disks_state.zero_index
        
        ordered = []
        for i in range(1, self.n):
            ordered.append(small_disks_state.small_disks[(zero_pos + i) % self.n])
        
        last_disk = ordered[0]
        for i in range(1, len(ordered)):
            current_disk = ordered[i]
            next_expected = (last_disk % (self.unique_n - 1)) + 1
            if current_disk != last_disk and current_disk != next_expected:
                return False
            last_disk = current_disk
        
        first_disk = ordered[0]
        last_disk = ordered[-1]
        if first_disk == last_disk:
            if not all(d == first_disk for d in ordered):
                return False
        
        return True
   
    def solve(self):
        closed_set = set()
        while self.fringe:
            _, _, next_node = heapq.heappop(self.fringe)
            seen = rep_check(closed_set, next_node.small_disks)
            if seen:
                continue
            else:
                if self.is_solved(next_node):
                    print("Solution is")
                    for state in next_node.trace_back_state:
                        print(" ".join(map(str, state)))
                    return True
                closed_set.add(tuple(next_node.small_disks))
                children = (self.create_children(next_node))[0]
                move_made = (self.create_children(next_node))[1]
                for i, child in enumerate(children):
                    child.trace_back_state = next_node.trace_back_state + [child.small_disks]
                    child.trace_back_move = next_node.trace_back_move + [move_made[i]]
                    self.counter += 1
                    heapq.heappush(self.fringe, (child.f, self.counter, child))
        print("No solution")
        return False

def rep_check(closed_set, og_list):
    seen = False
    l = len(og_list)
    for n in range(l):
        rotated_list = og_list[-n:] + og_list[:-n]
        if tuple(rotated_list) in closed_set:
            seen = True
    return seen

    
def main():
    if len(sys.argv) < 2:
        print("Error: Missing argument.")
        print("Usage: ./AB <number_of_disks>")
        sys.exit(1)
    
    try:
        n_arg = int(sys.argv[1])
    except ValueError:
        print("Error: Argument must be an integer.")
        sys.exit(1)
        
    try:
        line1_str = sys.stdin.readline()
        line2_str = sys.stdin.readline()
        
        if not line1_str or not line2_str:
            print("Error: Expected 2 lines of input.")
            sys.exit(1)

        line1 = line1_str.strip().split()
        line2 = line2_str.strip().split()
        
        large_disks_input = [int(x) for x in line1]
        small_disks_input = [int(x) for x in line2]
        
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)
        
    puzzle = Disks(n_arg, large_disks_input, small_disks_input)
    puzzle.solve()


if __name__ == "__main__":
    main()