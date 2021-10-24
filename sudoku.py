#!/usr/bin/env python3

import copy, sys, time

# Global variables
n_iter = 0
range9 = range(9)

def open_puzzle(puzzle_path):
    def clean(s):
        line = []
        for ch in s:
            if ch in '123456789':
                line.append(ch)
            else:
                line.append('.')
        return line[:9]

    puzzle = []

    with open(puzzle_path) as puzzle_file:
        for line in puzzle_file:
            line = clean(line)
            assert len(line) == 9, 'Each row must have 9 elements'
            puzzle.append(line)
            if len(puzzle) == 9:
                break
    assert len(puzzle) == 9, 'Each column must have 9 elements'
    assert verify_valid(puzzle) == True, 'Check file for duplicate elements'

    return puzzle

def pprint(puzzle):
    global range9
    for r in range9:
        if r == 3 or r == 6:
            print('------+-------+------')
        for c in range9:
            if c == 3 or c == 6:
                print('|', end=' ')
            print(puzzle[r][c], end=' ')
        print()

def verify_valid(puzzle):
    def check(line):
        for el in line:
            if not el == '.' and line.count(el) > 1:
                return False
        return True

    global range9

    # Check rows and columns
    for j in range9:
        row = puzzle[j]
        if not check(row):
            return False
        col = []
        for i in range9:
            col.append(puzzle[i][j])
        if not check(col):
            return False

    # Check 3x3 boxes
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            line = [*puzzle[i][j:j+3], *puzzle[i+1][j:j+3], *puzzle[i+2][j:j+3]]
            if not check(line):
                return False

    return True

def solve(puzzle):
    def verify_complete(puzzle):
        global range9
        for i in range9:
            for j in range9:
                if puzzle[i][j] not in '123456789':
                    return False, (i, j)
        return True, (i, j)

    global n_iter
    n_iter += 1
    flag_complete, (i, j) = verify_complete(puzzle)

    if flag_complete:
        return puzzle, verify_valid(puzzle)

    candidate = copy.deepcopy(puzzle)
    for el in '123456789':
        candidate[i][j] = el
        if verify_valid(candidate):
            candidate, flag_complete = solve(candidate)
        if flag_complete:
            return candidate, flag_complete

    return puzzle, False

def main():
    """Sudoku puzzle solver. Reads puzzle from a file and prints the solution.

    Assumes:
    * Path to the file is specified as a command line argument. No other
      command line arguments are accepted.
    * Puzzle file format is text with 9 lines and 9 characters per line.
    """
    global n_iter
    starttime = time.perf_counter()
    puzzle = open_puzzle(sys.argv[1])
    print('Puzzle:')
    pprint(puzzle)
    print()

    solution, status = solve(puzzle)
    print('Solution:')
    pprint(solution)
    print()
    print('No. of iterations:', n_iter)
    print('Elapsed time:', time.perf_counter() - starttime)

if __name__ == '__main__':
    main()