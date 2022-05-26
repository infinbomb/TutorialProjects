import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    # prints maze to screen using the color pairs
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row): # like a for each loop
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start):
    # just finds the entrance to the maze "O"
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start: # uses parameter
                return i, j # returns the 2d array index

    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue() #Queue is a queue
    q.put((start_pos, [start_pos])) #puts start position in the queue

    visited = set()

    while not q.empty(): # returns true or false
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear() # clears the screen
        print_maze(maze, stdscr, path)
        time.sleep(0.2) # wait .2 secs
        stdscr.refresh()

        if maze[row][col] == end: # return the path when it reaches X, the end
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                # if just visited
                continue # skip that iteration of loop

            r, c = neighbor
            if maze[r][c] == "#": # if wall, skip
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row, col):
    # just finds and returns all neighbors thats in the maze, including border
    neighbors = []

    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) # number, foreground color, background color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()  # ?


wrapper(main) # importing the curses.wrapper() function and using it like this will make debugging easier