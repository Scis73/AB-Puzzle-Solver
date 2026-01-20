import sys

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

        # Large Disks
        # Represented as list, as they dont change. 
        self.large_disks = list(large_disks_data)

        # Small Disks
        # Represented as Tuple, Since they are immutable and hashable.
        # set(), dict() are good to know here so that we can make sure we havent visited the same state before
        self.small_disks = tuple(small_disks_data) 

    def print_details(self):
        # Print Statement for some deets
        print("==================")
        print(f"System Size (N):    {self.n}")
        print(f"(Large Disks):      {self.large_disks}")
        print(f"(Small Disks):      {self.small_disks}")
        print("==================")

    def get_valid_moves(self):
        # TODO: 
        # Double check if this is correct - Aidan

        # Locate empty spot
        zero_index = self.small_disks.index(0)

        # Refer to large disk data to see how far we can jump
        jump_distance = self.large_disks[zero_index]
        
        
        
        # Jump calculation, use modN to "wrap around the circle"
        # Right is addition
        # Left is subtraction
        right_jump_index = (zero_index + jump_distance) % self.n
        left_jump_index  = (zero_index - jump_distance) % self.n
        right_neighbor   = (zero_index + 1)
        left_neighbor    = (zero_index - 1)
        
        # Debug Print
        print(f"0 is at: [{zero_index}]")
        print(f"Large Disk at 0 is: [{jump_distance}]")
        print("==================")
        print(f"Right Jump to:      [{zero_index}] to Small disk index: [{right_jump_index}].  Value: {self.small_disks[right_jump_index]}")
        print(f"Left Jump to:       [{zero_index}] to Small disk index: [{left_jump_index}].  Value: {self.small_disks[left_jump_index]}")
        print(f"Right neighbor to:  [{zero_index}] to Small disk index: [{right_neighbor}].  Value: {self.small_disks[right_neighbor]}")
        print(f"Left neighbor to:   [{zero_index}] to Small disk index: [{left_neighbor}].  Value: {self.small_disks[left_neighbor]}")
        
        return [left_jump_index, right_jump_index]
    
def main():
    
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
        # Reading all lines from stdin
        input_lines = sys.stdin.read().strip().split('\n')
        if len(input_lines) < 2:
            print("Error: Expected 2 lines of input (Large Disks, Small Disks).")
            sys.exit(1)
            
        line1 = input_lines[0].strip().split()
        line2 = input_lines[1].strip().split()
        
        # Convert strings to integers
        large_disks_input = [int(x) for x in line1]
        small_disks_input = [int(x) for x in line2]
        
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)
        
    puzzle = Disks(n_arg, large_disks_input, small_disks_input)
    
    puzzle.print_details()
    puzzle.get_valid_moves()
    
if __name__ == "__main__":
    main()