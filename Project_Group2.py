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
        self.start_state = list(small_disks_data)
        
        # Determine how many 1s, 2s, etc.
        unique_values = set(small_disks_data)
        if 0 in unique_values: # Dont count 0 of course
            unique_values.remove(0)
        self.unique_n = len(unique_values)
        
        # Goal State Calculation
        # Pre Clac the winning state to make checking is_solved() fast.
        # Expected: n 1s, n 2s, ... n ns, followed by 0. 
        # Yes the Zero can be anywhere but just easier if we keep it in the end like in the lab spec
        self.goal_state_list = []
        self.goal_state_set = set()
        #for i in range(1, self.unique_n + 1):
         #   self.goal_state_list.extend([i] * self.unique_n)
        #self.goal_state_list.append(0)
        for i in range(self.n):
            self.goal_state_list.append(math.ceil(i/self.unique_n))

        for i in range(self.n):
            rotated_goal = self.goal_state_list[i:self.n] + self.goal_state_list[0: (i + self.n) % self.n]
            self.goal_state_set.add(tuple(rotated_goal))
        # Convert to tuple for comparison
        # Fringe (Banger Festival Btw :D )
        self.fringe = []
        
        
        self.counter = 0
        
        # Initial Node 
        initial_state = self.SmallDisks(tuple(small_disks_data), parent=None, g=0)
        initial_state.g = 0
        initial_state.h = self.heuristic(initial_state)
        initial_state.f = initial_state.g + initial_state.h
        # hq.heappush(self.fringe, (initial_state.f, self.counter, initial_state)) # Braeden version
        # If costs of 2 states are the same, compare number of potential children as tiebreaker
        # More children is better, reasoning is that more children means higher chance of finding a better move
        hq.heappush(self.fringe, (initial_state, self.large_disks[initial_state.zero_index] * -1)) # Steve version

    # Inner Class represents one node in tree
    class SmallDisks:
        def __init__(self, small_disks_data, parent=None, g=0):
            self.small_disks = small_disks_data
            
            # Parent Pointer, this will save a lot on mem
            self.parent = parent
            
            # Find 0 (empty slot) immediately
            self.zero_index = self.small_disks.index(0)
            
            
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
            # FINAL TIE BREAKER: Compare the actual lists to prevent crashes (Happend...)
            #return self.small_disks < other.small_disks
        
        
    # ============ Helper Functions 

    def print_children(self, current, children):
        # takes list of children of current node and prints them
        print("Children of",*current.small_disks, "are")
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
       # print(f"(Goal State):       {self.goal_state}")
        print("==================")
    
    def get_valid_moves(self, small_disks_state):
        zero_index = small_disks_state.zero_index
        jump_distance = self.large_disks[zero_index]
        
        right_jump_index = (zero_index + jump_distance) % self.n
        left_jump_index  = (zero_index - jump_distance) % self.n
        right_neighbor   = (zero_index + 1) % self.n
        left_neighbor    = (zero_index - 1) % self.n
        
        # Debug Print
        # print(f"0 is at: [{zero_index}]")
        # print(f"Large Disk at 0 is: [{jump_distance}]")
        # print("==================")
        # print(f"Right Jump to:      [{zero_index}] to Small disk index: [{right_jump_index}].  Value: {self.small_disks[right_jump_index]}")
        # print(f"Left Jump to:       [{zero_index}] to Small disk index: [{left_jump_index}].  Value: {self.small_disks[left_jump_index]}")
        # print(f"Right neighbor to:  [{zero_index}] to Small disk index: [{right_neighbor}].  Value: {self.small_disks[right_neighbor]}")
        # print(f"Left neighbor to:   [{zero_index}] to Small disk index: [{left_neighbor}].  Value: {self.small_disks[left_neighbor]}")
        
        # [[left_jump_index, left_neighbor, right_neighbor, right_jump_index], ["left by "+str(jump_distance), "left by 1", "right by 1", "right by "+str(jump_distance)]]
        moves = {right_jump_index, left_jump_index, right_neighbor, left_neighbor}

        return moves
        
    def create_children(self, current_node):
        children = []
        valid_indices = self.get_valid_moves(current_node)
        
        for target_i in valid_indices:
            children.append(self.move_disk(target_i, current_node))
            
        return children

    def move_disk(self, target_i, current_node):
        # Create a copy of the list data
        #new_data = list(current_node.small_disks)
        old_tuple = current_node.small_disks
        zero_index = current_node.zero_index
        # Create new tuple with values in zero_index and target_i swapped
        new_tuple = tuple(old_tuple[zero_index] if x == target_i else old_tuple[target_i] if x == zero_index else old_tuple[x] for x in range(self.n))
        
        # Swap '0' with the target
        #new_data[zero_index], new_data[target_i] = new_data[target_i], new_data[zero_index]
        
        # Create new Node
        # Parent is 'current_node'
        # Cost g increases by 1
        new_node = self.SmallDisks(new_tuple, parent=current_node, g=current_node.g + 1)
        
        # Calculate Heuristic
        new_node.h = self.heuristic(new_node)
        new_node.f = new_node.g + new_node.h
        
        return new_node
    
    def is_solved(self, small_disks_state):
        # Aidan Version
        # Checks if current state matches the pre-calculated goal state
        return small_disks_state.small_disks in self.goal_state_set
    
    '''
    def is_solved(self, small_disks_state):
        # Steve version
        last_disk = small_disks_state.small_disks[-1] 
        for i in range(self.n):
            current_disk = small_disks_state.small_disks[i]
            if not((current_disk == last_disk) or (current_disk == ((last_disk + 1) % self.unique_n))):
        #        print("Not solved")
                return False
            last_disk = current_disk
        #print(f"{small_disks_state.small_disks} is a solution!")
        return True
    def is_solved(self, small_disks_state):
        # Braeden version
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
        '''
    def solve(self):
        # Aidan Version
        # Closed Set: Stores visited states to prevent loops.
        closed_set = set()
        loop_counter = 0
            
        while self.fringe:
        # while loop_counter < 30: # Debug so print doesnt go crazy 
            loop_counter += 1
            # Get rid of node with lowest 'f' score
            current_node = hq.heappop(self.fringe)[0]
            
            print(f"\n--- LOOP {loop_counter} ---")
            #print(f"Checking Node:  {current_node.small_disks}")
            print(f"Costs:          f={current_node.f} (g={current_node.g} + h={current_node.h})")
            #print(f"Fringe Size:    {len(self.fringe)}")
            #print(f"Closed Set:     {len(closed_set)}")
                
            if self.is_solved(current_node):
                self.print_solution(current_node)
                return True
            
            # Then check to see if we have been to it already
            #state_tuple = tuple(current_node.small_disks)
            if current_node.small_disks in closed_set:
                continue
            closed_set.add(current_node.small_disks)
                
            # Expand neighbors
            children = self.create_children(current_node)
           # self.print_children(current_node, children) 
                
            for child in children:
                hq.heappush(self.fringe, (child, self.large_disks[child.zero_index] * -1))
            
        # Else No Solution
        print("No Solution")
            
        return False
    '''
    def solve(self):
        # Steve version
        closed_set=set()
        
        fringe = self.fringe
        while fringe:
            next_node = hq.heappop(fringe)
            print(f"Checking {next_node.small_disks}")
            seen=rep_check(closed_set,next_node.small_disks)
            if seen:
                continue
            else:
                if self.is_solved(next_node):
                    self.print_solution(next_node.trace_back_state)
                    return True
                closed_set.add(tuple(next_node.small_disks))
                children, move_made = (self.create_children(next_node))
                #move_made=(self.create_children(next_node))[1]
                self.print_children(next_node, children)
                for i, child in enumerate(children):
                    child.trace_back_state = next_node.trace_back_state + [child.small_disks]
                    child.trace_back_move = next_node.trace_back_move + [move_made[i]]
                    hq.heappush(fringe, child)

    def solve(self):
        # Braeden version
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
    '''
def rep_check(closed_set, og_tuple):
    return og_tuple in closed_set

def main():
    '''
    # Test check_closed function
    seen0=check_closed([[0,1,2,3],[0,3,1,2]],[0, 1,2,3])
    if seen0==False:
        print("Error in check_closed()")
    else:
        print("check_closed() passed test 0")
    seen1=check_closed([[0,1,2,3],[0,3,1,2]],[1,2,3,0])
    if seen1==False:
        print("Error in check_closed()")
    else:
        print("check_closed() passed test 1")
    seen2=check_closed([[0,1,2,3],[0,3,1,2]], [2, 3,0,1])
    if seen2==False:
        print("Error in check_closed()")
    else:
        print("check_closed() passed test 2")
    seen3=check_closed([[0,1,2,3],[0,3,1,2]], [3, 0, 1, 2])
    if seen3==False:
        print("Error in check_closed()")
    else:
        print("check_closed() passed test 3")
    seen4=check_closed([[0,1,2,3],[0,3,1,2]], [0, 1, 2, 3])
    if seen4==False:
        print("Error in check_closed()")
    else:
        print("check_closed() passed test 4")
    seen5=check_closed([[0,1,2,3],[0,3,1,2]], [0,1, 3, 2])
    if seen5==True:
        print("Error in check_closed()")
    else:
        print("check_closed() passed test 5")
    '''

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
    
    # puzzle.print_details()
    # puzzle.get_valid_moves()
    puzzle.solve()


if __name__ == "__main__":
    main()
