import sys
import math
from queue import Queue
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
        # TODO - Steve
        # For breadth-first graph, closed list of already seen states to avoid loops, hash table?
        # Some methods should probably be moved into SmallDisks class, also need to add more data (parent etc) to SmallDisks
        # Rework create_children so that we can use tuples for small disk state
        # Rename a bunch of variables probably for clarity
        # If we want to do A*, change fringe from queue to heap
        # For A*, need to decide on/implement a heuristic

        self.n = n

        # Large Disks
        # Represented as list, as they dont change. 
        self.large_disks = list(large_disks_data)


        # Small Disks
        # Represented as Tuple, Since they are immutable and hashable.
        # set(), dict() are good to know here so that we can make sure we havent visited the same state before

        # Changed to have queue/fringe with small disks data as initial state
        # Changed small_disks to list instead of tuple for creating children since need to copy and then change 
        # parent to create child, can change back to tuple if create_children reworked - Steve
        self.fringe = [] 
        self.init_state = self.SmallDisks(list(small_disks_data))
        hq.heappush(self.fringe, self.init_state)
       
        
        # Number of unique values on small disks
        self.unique_n = int(math.sqrt(n-1)) + 1
        

    # Do we want a separate class for state of small disks, so we can create multiple states without recreating
    # whole structure every time? added it for now - Steve
    # SmallDisks as graph nodes basically
    class SmallDisks:
        def __init__(self, small_disks_data):
            self.small_disks = small_disks_data
            # Moved initialization of zero_index here since it might be needed for multiple functions - Steve
            self.zero_index = self.small_disks.index(0)
            # This is going to use a lot of memory for bigger problems
            # 10 nodes at depth 10 = 10 lists of 10 + more lists for shallower nodes
            # Can probably just track parent of each node then trace back to root once solution found
            self.trace_back_state = [small_disks_data]
            self.trace_back_move = []
            self.cost = 0 # replace this when heuristics implemented
            # self.parent?
            # self.children?

        def __lt__(self, other):
            # Override less than for SmallDisks to compare their costs, needed for heapq
            return self.cost < other.cost

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

    def print_details(self):
        # Print Statement for some deets
        print("==================")
        print(f"System Size (N):    {self.n}")
        print(f"(Large Disks):      {self.large_disks}")
        print(f"(Small Disks):      {self.fringe}")
        print(f"(Unique n):         {self.unique_n}")
        print("==================")
    
    def get_valid_moves(self, small_disks_state):
        # TODO: 
        # Double check if this is correct - Aidan

        zero_index = small_disks_state.zero_index

        # Refer to large disk data to see how far we can jump
        jump_distance = self.large_disks[zero_index]
        
        
        
        # Jump calculation, use modN to "wrap around the circle"
        # Right is addition
        # Left is subtraction
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
            # if large disk is 1, neighbor and jump are same move
            return [[left_neighbor, right_neighbor],["left by 1","right by 1"]]

        return [[left_jump_index, left_neighbor, right_neighbor, right_jump_index], ["left by "+str(jump_distance), "left by 1", "right by 1", "right by "+str(jump_distance)]]

        
    def create_children(self, small_disks_state):
        # find possible moves of a given state and generate resulting states
        # This won't work as is, need to rewrite move_disk to create new object 
        # and rewrite get_valid_moves to take any state of small disks

        # Should this add children directly to queue instead?
        children = []
        move_states = (self.get_valid_moves(small_disks_state))[0]
        move_made=(self.get_valid_moves(small_disks_state))[1]
        for move in move_states:
            children.append(self.move_disk(move, small_disks_state))
        
        return [children,move_made]

    def move_disk(self, target_i, small_disks_state):
        # Create copy of state, then swap values of zero_index and target in copy and return it
        zero_index = small_disks_state.zero_index
        new_state = self.SmallDisks(list(small_disks_state.small_disks))
        new_state.small_disks[zero_index] = new_state.small_disks[target_i]
        new_state.small_disks[target_i] = 0
        new_state.zero_index = target_i
        return new_state

    def add_to_fringe(self, small_disks_state):
        self.fringe.put(small_disks_state)

    def is_solved(self, small_disks_state):
        # Loop around small disks list to see if all neighbours are correct
        last_disk = small_disks_state.small_disks[-1]
        
        for i in range(self.n):
            current_disk = small_disks_state.small_disks[i]
            if not((current_disk == last_disk) or (current_disk == ((last_disk + 1) % self.unique_n))):
        #        print("Not solved")
                return False
            last_disk = current_disk
        #print(f"{small_disks_state.small_disks} is a solution!")
        return True
   
    def solve(self):
        closed_set=set()
        #for i in range(50):
            #print(f"closed: {closed_set}")
        while True:
            fringe = self.fringe
            if not fringe:
                print("Fringe empty, no solution found")
                return False
            #self.print_fringe() update to work with heap
            next_node = hq.heappop(fringe)
            print(f"Checking {next_node.small_disks}")
            seen=rep_check(closed_set,next_node.small_disks)
            if seen:
                print("Already seen this state, skipping")
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



def rep_check(closed_set,og_list):
    #seen=False
    #l= len(og_list)
    #for n in range(l):
        # Rotate right by n each time
     #       rotated_list = og_list[-n:] + og_list[:-n]
   # if tuple(rotated_list) in closed_set:
    #        seen=True
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
    
    
    # Just incase if I fat finger a letter... 
    try:
        n_arg = int(sys.argv[1])
    except ValueError:
        print("Error: Argument must be an integer.")
        sys.exit(1)
        
    
    try:
        # Read input
        line1_str = sys.stdin.readline()
        line2_str = sys.stdin.readline()
        
        # Error check just in case
        if not line1_str or not line2_str:
            print("Error: Expected 2 lines of input.")
            sys.exit(1)

        # Split into lists
        line1 = line1_str.strip().split()
        line2 = line2_str.strip().split()
        
        # Convert strings to integers
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
