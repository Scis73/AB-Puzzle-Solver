import sys
import math
import heapq as hq

"""
CMPT 355 - Group 2
AB Puzzle

Aidan, Sam, Steve, Braeden

Usage:
    ./AB <number_of_disks>
    (Then two inputs)

Run program by:
    1) cd into git folder
    2) '$ python3 Project_Group2.py 10'
    2a) You can also pipe in the test_input.txt by:
        2a) '$ python3 Project_Group2.py 10 < test_input.txt'
    3) Read results


"""

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
        # hq.heappush(self.fringe, (initial_state.f, self.counter, initial_state)) # Braeden version
        hq.heappush(self.fringe, initial_state) # Steve version

    class SmallDisks:
        def __init__(self, small_disks_data):
            self.small_disks = small_disks_data
            self.zero_index = self.small_disks.index(0)
            # This is going to use a lot of memory for bigger problems
            # 10 nodes at depth 10 = 10 lists of 10 + more lists for shallower nodes
            # Can probably just track parent of each node then trace back to root once solution found
            self.trace_back_state = [small_disks_data]
            self.trace_back_move = []
            self.g = 0
            self.h = 0
            self.f = 0
            # self.parent?
            # self.children?

        def __lt__(self, other):
            # Override less than for SmallDisks to compare their costs, needed for heapq
            if self.f == other.f:
                return self.h < other.h
            return self.f < other.f

    def print_children(self, current, children):
        # takes list of children of current node and prints them
        print("Children of",*current.small_disks, "are")
        for child in children:
            print(*child.small_disks)

    def print_fringe(self):
        print("Current fringe is", self.fringe)

    def print_solution(self, trace_back_state):
        # Takes list of states on path to solution and prints them
        print("Solution is")
        for state in trace_back_state:
            print(*state)

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
        
        # Debug Print
        #print(f"0 is at: [{zero_index}]")
        #print(f"Large Disk at 0 is: [{jump_distance}]")
        #print("==================")
        #print(f"Right Jump to:      [{zero_index}] to Small disk index: [{right_jump_index}].  Value: {self.small_disks[right_jump_index]}")
        #print(f"Left Jump to:       [{zero_index}] to Small disk index: [{left_jump_index}].  Value: {self.small_disks[left_jump_index]}")
        #print(f"Right neighbor to:  [{zero_index}] to Small disk index: [{right_neighbor}].  Value: {self.small_disks[right_neighbor]}")
        #print(f"Left neighbor to:   [{zero_index}] to Small disk index: [{left_neighbor}].  Value: {self.small_disks[left_neighbor]}")
        
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
    '''
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
    ''' 
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
def rep_check(closed_set, og_list):
    return tuple(og_list) in closed_set

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
