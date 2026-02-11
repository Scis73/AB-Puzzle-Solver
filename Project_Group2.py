import sys
import math
import heapq as hq

"""
CMPT 355 - Group 2
AB Puzzle

Aidan, Sam, Steve, Braeden

Usage:
    ./Project_Group2 <number_of_disks>
    (Then two inputs)

Run program by:
    1) cd into git folder
    2) '$ python3 Project_Group2.py 10'
    2a) You can also pipe in the test_input.txt by:
        2a) '$ python3 Project_Group2.py 10 < test_input.txt'
    3) Read results


Algo Details:
- Heuristic (h): Sum of Circular Manhattan Distances (How far each tile is from a valid spot)

"""

class Disks:
    def __init__(self, n, large_disks_data, small_disks_data):
        
        self.n = n
        # Store as static list
        self.large_disks = list(large_disks_data)
        # Store Init State for print
        self.start_state = tuple(small_disks_data)
        
        # Determine how many 1s, 2s, etc.
        unique_values = set(small_disks_data)
        if 0 in unique_values: # Dont count 0 of course
            unique_values.remove(0)
        self.unique_n = len(unique_values)
        
        # Goal State Calculation
        # Pre Clac the winning state to make checking is_solved() fast.
        # Expected: n 1s, n 2s, ... n ns, followed by 0. 
        self.goal_state_list = []
        self.goal_state_set = set()
        
        for i in range(self.n):
            self.goal_state_list.append(math.ceil(i/self.unique_n))

        for i in range(self.n):
            rotated_goal = self.goal_state_list[i:self.n] + self.goal_state_list[0: (i + self.n) % self.n]
            self.goal_state_set.add(tuple(rotated_goal))
        
        # Fringe (Banger Festival Btw :D )
        self.fringe = []
        
        self.counter = 0
        
        # Initial Node 
        initial_state = self.SmallDisks(tuple(small_disks_data), parent=None, g=0)
        initial_state.g = 0
        initial_state.h = self.heuristic(initial_state)
        initial_state.f = initial_state.g + initial_state.h
        
        # If costs of 2 states are the same, compare number of potential children as tiebreaker
        # More children is better, reasoning is that more children means higher chance of finding a better move
        # Ideally code would be refactored to allow access to large_disks from SmallDisks so we didn't need --
        # -- large_disks info as separate value
        hq.heappush(self.fringe, (initial_state, self.large_disks[initial_state.zero_index] * -1))

    # Inner Class represents one node in tree
    class SmallDisks:
        def __init__(self, small_disks_data, parent=None, g=0):
            self.small_disks = small_disks_data
            
            # Parent Pointer, this will save a lot on mem
            self.parent = parent
            
            # Find 0 (empty slot) by index on initial state
            # update it for children inside move_disk function at O(1) time
            self.zero_index = self.small_disks.index(0) if parent == None else None    
            
            # A* Costs
            self.g = g # Depth, Cost So Far
            self.h = 0 # Heuristic -> Cost to goal
            self.f = 0 # Total Score (g + h)
            

        def __lt__(self, other):
            # Needed for the Priority Queue to sort nodes.
            # We compare 'f' scores.
            if self.f != other.f:
                return self.f < other.f
            # TIE BREAKER: If f scores are equal, compare h scores (Greedy)
            if self.h != other.h:
                return self.h < other.h
        
        
    # ============ Helper Functions 

    def print_children(self, current, children):
        # takes list of children of current node and prints them
        print("Children of: [",*current.small_disks, "] are")
        for child in children:
            print(*child.small_disks)

    def print_fringe(self):
        print("Current fringe is", self.fringe)

    def print_solution(self, end_node):
        # Traces back from the end_node to the start using parent pointers,
        # then prints the path.
        path = []
        current = end_node
        while current:
            path.append(current.small_disks)
            current = current.parent
            
        # Path is currently goal so just reverse it
        path.reverse()
        
        print("Solution is")
        
        for state in path:
            # Print list as space-separated string
            print(" ".join(map(str, state)))

    def heuristic(self, small_disks_state):
        # Estimate Distance to goal using Manhattan Distance but just for a circle.
        # Calcs how far every tile is from target pos.
        
        total_distance = 0
        state = small_disks_state.small_disks
        n_group_size = self.unique_n
        
        for current_idx, val in enumerate(state):
            if val == 0: continue # Dont count empty spot
            
            # We have to calculate this value where it should ROUGHLY be. 
            # For example we estimate at the start of its group.
            # If we have 3 unique values and we want to estimate where the 2s go
            # (2-1) * 3 = Index 3, which is ROUGHLY where the start of 2s are. 
            target_group_start = (val - 1) * n_group_size
            
            # Distance clockwise
            diff = abs(current_idx - target_group_start)
            # Since cirlce, distance is min of wrap-around
            dist = min(diff, self.n - diff)
            
            total_distance += dist
            
        return total_distance

    def print_details(self):
        print("==================")
        print(f"System Size (N):    {self.n}")
        print(f"(Large Disks):      {self.large_disks}")
        print(f"(Small Disk Start): {self.start_state}") 
        print(f"(Unique n):         {self.unique_n}")
        print("==================")
    
    def get_valid_moves(self, small_disks_state):
        zero_index = small_disks_state.zero_index
        jump_distance = self.large_disks[zero_index]
        
        right_jump_index = (zero_index + jump_distance) % self.n
        left_jump_index  = (zero_index - jump_distance) % self.n
        right_neighbor   = (zero_index + 1) % self.n
        left_neighbor    = (zero_index - 1) % self.n
        
        moves = {right_jump_index, left_jump_index, right_neighbor, left_neighbor}

        return moves
        
    def create_children(self, current_node):
        children = []
        valid_indices = self.get_valid_moves(current_node)
        
        for target_i in valid_indices:
            children.append(self.move_disk(target_i, current_node))
            
        return children

    def move_disk(self, target_i, current_node):
        # Create a copy of the tuple data
        old_tuple = current_node.small_disks
        zero_index = current_node.zero_index
        # Create new tuple with values in zero_index and target_i swapped
        new_tuple = tuple(old_tuple[zero_index] if x == target_i else old_tuple[target_i] if x == zero_index else old_tuple[x] for x in range(self.n))
        
        # Swap '0' with the target
        
        # Create new Node
        # Parent is 'current_node'
        # Cost g increases by 1
        new_node = self.SmallDisks(new_tuple, parent=current_node, g=current_node.g + 1)
        
        # Calculate Heuristic
        new_node.h = self.heuristic(new_node)
        new_node.f = new_node.g + new_node.h
        # zero swaps with value in target_i, so target_i will be zero_index for new node
        new_node.zero_index = target_i
        return new_node
    
    def is_solved(self, small_disks_state):
        # Checks if current state matches the pre-calculated goal state
        return small_disks_state.small_disks in self.goal_state_set
    
    def solve(self):
        # Closed Set: Stores visited states to prevent loops.
        closed_set = set()
        loop_counter = 0
            
        while self.fringe:
        # while loop_counter < 2: # Debug so print doesnt go crazy 

            loop_counter += 1
            # Get rid of node with lowest 'f' score
            current_node = hq.heappop(self.fringe)[0]
            
            if self.is_solved(current_node):
                self.print_solution(current_node)
                return True
            
            # Then check to see if we have been to it already
            if current_node.small_disks in closed_set:
                continue
            closed_set.add(current_node.small_disks)
                
            # Expand neighbors
            children = self.create_children(current_node)
                
            for child in children:
                hq.heappush(self.fringe, (child, self.large_disks[child.zero_index] * -1))
            
        # Else No Solution
        print("No Solution")
            
        return False
def rep_check(closed_set, og_tuple):
    return og_tuple in closed_set

def main():

    # Command Line Arg
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
