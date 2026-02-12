# CMPT 355 - Project 1

**Group 2:** Aidan, Sam, Steve, Braeden  
**Course:** Introduction to Artificial Intelligence  
**Date:** February 11, 2026

---

## Overview
This program implements an A* (A-Star) search algorithm to solve the "AB Puzzle." It finds the optimal sequence of moves to sort a circular array of disks based on dynamic jump constraints provided by a set of large underlying disks.

The program includes:
- **Heuristic Search:** Uses a Circular Manhattan Distance heuristic.
- **Optimization:** Efficient state hashing and parent-pointer path reconstruction.


## Requirements
- **Python 3.x**


## How to Compile (Build)
This project uses a `Makefile` to create an executable wrapper for the Python script.

1. Open your terminal in the project directory.
2. Run the following command:
```bash
$ make
```
3. This will create an executable file named **`AB`**.

---

## How to Run
The program accepts the number of disks (`N`) as a command-line argument and reads the puzzle configuration from Standard Input (Stdin).

**Syntax:**

./AB <number_of_disks>


**Example (Interactive Mode):**
```bash
./AB 10
#Then type the two lines of input:
1 2 1 2 1 2 1 2 1 2
1 1 1 3 2 2 3 3 0 2
```
---
## Running with Test Files
We have provided sample inputs located in the `./TestFolder` directory. The files are named `AB#` where `#` corresponds to the number of disks (e.g., `AB10` for N=10).

To run a test case, redirect the file into the program using the `<` operator:

**Example for N=10:**
```bash
./AB 10 < ./TestFolder/AB10
```

**Example for N=5:**
```bash
$ ./AB 5 < ./TestFolder/AB5
```
---
## Cleaning Up
To remove the executable, run:
```bash
$ make clean
```