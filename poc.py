from collections import deque

# The maze as a multiline string
maze_str = '''
OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
OSO O O O O O       O   O O O O O               O O   O   O   O   O O O O     O O     O O         O O
O O O O O O O OOOOOOO OOO O O O O OOOOO O OOO OOO O O OOO O OOO OOO O O OOO O O O OOOOO OOOOO OOOOO O
O O   O O       O O   O   O O   O O     O O O   O   O         O   O   O     O O     O           O   O
O O O O O OOOOO O OOO OOO O O OOOOOOO O O O OOO OOOOOOOOO OOOOOOO O OOOOOOO O OOO O O O O OOOOO O O O
O   O   O   O   O O   O   O     O   O O O O     O O O O O     O O O O O   O O O   O   O O O O   O O O
OOOOO O OOOOOOO O O OOO O O O O O O OOOOO OOOOO O O O O O O O O O O O O O OOO OOO OOO O OOO OOOOOOO O
O O   O   O O O     O   O O O O   O   O O O   O O   O   O O O       O O O O       O O O     O   O O O
O OOOOOOO O O O OOOOOOO OOO OOOOO OOO O OOO O O O OOO OOO OOO O OOOOO OOO OOOOOOOOO O OOOOOOOOO O O O
O O   O       O   O       O   O   O   O     O O       O O   O O   O     O     O     O O     O       O
O OOO O OOOOO O OOO OOOOOOOOOOOOO OOOOOOO OOO OOOOOOO O OOOOO OOO OOO OOOOO OOOOOOO O O OOO OOOOO O O
O O     O       O   O   O O     O           O O         O   O   O O       O     O     O   O O O O O O
O OOO O OOO OOO O OOO O O O O O OOO OOOOO OOO O O O OOOOOOO O O O O OOOOO O O OOO OOO O OOO O O O O O
O   O O   O O O     O O     O O     O     O O   O O     O O   O O   O   O   O   O   O     O O     O O
O OOOOO OOO O O O OOOOO OOOOO O O OOOOOOO O O O O OOO OOO OOOOOOO OOO O O OOO OOO OOO OOOOO OOO OOOOO
O     O O   O   O     O     O O O O   O   O   O O   O O   O       O   O   O O O     O   O O O       O
O O OOO O OOOOOOO OOO OOO O OOOOO OOO O OOOOOOOOOOOOOOOOO OOO OOOOOOO OOOOO OOOOOOO OOOOO OOO O O O O
O O O   O O         O   O O   O     O     O     O   O   O     O   O O   O       O   O         O O O O
O OOOOOOO O O OOOOO OOO OOO O O OOOOO O O O O O O O O O OOOOO O OOO OOOOOOOOO OOO O O O OOOOOOOOO OOO
O         O O     O O O     O O O O   O O O O O   O O O   O O O   O           O   O O O   O O     O O
O O OOOOO OOO OOOOO O OOO OOOOOOO OOOOOOOOOOOOOOOOO OOOOO O O OOO OOO OOOOO O OOO OOO OOO O OOOOO O O
O O O   O O       O O   O   O   O             O         O       O O O O   O O O   O     O     O   O O
O OOOOO O OOOOOOOOOOOOO O OOO OOOOOOO O O OOOOO OOOOO OOOOOOOOO O O OOO OOO OOO OOOOOOOOOOOOOOO OOO O
O     O       O     O O     O       O O O O     O O     O O O       O         O     O   O       O O O
O OOO OOOOOOO OOOOO O OOO O O OOOOOOO OOO O OOOOO O OOOOO O O OOO OOOOO OOOOOOOOOOO OOO O O OOO O O O
O   O O         O O       O   O   O O O     O                 O     O     O O           O O O O     O
OOOOOOOOOOO O O O O OOO OOOOOOO OOO OOO OOOOO O O OOOOO O OOOOOOO OOO OOOOO OOO OOO OOOOOOO O OOO O O
O   O   O O O O O     O   O O     O       O O O O     O O     O       O   O   O O O   O   O     O O O
OOO OOO O OOO O OOOOOOO OOO O O OOO OOO OOO OOOOOOOOOOOOO OOOOOOOOOOOOOOO OOO O O OOO OOO OOO O OOO O
O O   O   O   O O     O       O O O   O   O O     O     O     O O         O   O O O           O O   O
O O O O OOOOO OOOOO O OOOOO OOO O OOOOO OOO O OOOOOOO O OOO OOO O OOOOOOO O O O O O OOO O O O OOO OOO
O   O   O   O O   O O       O O O         O O   O O   O       O         O   O O   O O   O O O O     O
OOOOOOO OOO O O OOOOO O O O O OOO OOOOO OOO OOO O O O OOOOOOO O O O O OOO O O O O O OOO O OOO OOO O O
O   O   O O O O O O O O O O   O       O   O         O O O   O   O O O O   O O O O O O   O O O O O O O
O OOOOO O O OOO O O OOOOO O OOO OOO OOOOOOO OOO OOOOO O OOO OOOOOOO OOOOOOO OOO O OOOOOOOOO O O O O O
O   O   O           O O   O   O O O O O   O O       O     O O O   O     O O O O O   O O       O   O O
OOO O OOOOOOO OOO O O OOO OOO OOO O O O OOO O OOO OOO O O O O O OOOOOOOOO OOO OOOOO O OOOOOOO O OOOOO
O     O   O O   O O       O   O O         O O   O   O O O   O O   O O         O O   O       O O     O
OOOOO O OOO O O O OOO OOOOOOOOO OOOOO OOOOOOOOOOO OOOOO OOO O O OOO O OOOOOOO O O OOOOO OOOOOOOOO O O
O O     O O O O O   O         O O   O       O   O O     O O O   O O O       O O   O O           O O O
O O OOO O O O OOO OOO OOOOOOO O OOO OOOOO O O OOOOOOO OOO O O OOO O OOOOOOOOO OOO O OOOOOOO O OOO OOO
O   O   O O O   O O     O   O   O O O   O O O           O       O O       O   O       O O   O   O O O
O O O OOO O O OOOOOOO OOO O O OOO O OOO OOO O O OOO OOO OOOOOOOOO O OOOOOOOOO O OOOOO O O OOO O OOO O
O O O O   O O O O     O   O O               O O O O O         O   O     O O O O O     O O O   O O   O
O OOO OOO O OOO OOO OOO O O OOO OOOOOOOOO O OOO O O O OOOOOOO O OOO OOO O O O OOOOOOO O OOOOO OOOOO O
O O O     O   O   O   O O O O       O O   O   O O O O   O O O   O     O       O   O O   O O   O     O
O O O O OOO OOOOO O OOO O OOO OOO O O OOOOOOOOOOO OOOOOOO O OOOOOOO OOOOOOO OOO OOO O OOO O OOO OOOOO
O O   O O O O       O O O     O O O O     O   O O O O     O O         O       O   O O   O       O   O
OOOOO OOO O OOOOOOOOO OOOOOOOOO OOO O OOOOOOO O O O O OOO O O OOOOO OOO OOOOOOO OOO OOO OOOOO O O OOO
O       O     O O     O   O O O   O     O   O O   O   O         O     O O O       O         O O     O
O OOOOO OOO O O O O O O OOO O O O OOO O OOO O O OOO OOO O OOO O OOOOO OOO O OOO OOOOOOO O O OOO O O O
O   O       O   O O O O   O O   O     O   O       O   O O O O O O     O O O O O O   O   O O O   O O O
OOOOOOOOOOOOOOO OOOOO OOO O OOOOO OOO OOOOO O O OOO OOO OOO OOOOOOO OOO O O O OOO OOOOO OOOOOOOOOOO O
O     O O     O       O   O   O O O O       O O   O O O         O     O     O   O   O O O O O O     O
OOO OOO OOO OOO OOO OOO O O OOO OOO O O OOO O OOOOO O O OOOOOOO O OOOOOOO O O OOOOO O O O O O OOOOO O
O   O           O       O             O O O O     O O         O O O       O   O O         O         O
OOO O O OOOOOOO OOO O OOOOO OOO OOOOOOOOO O OOOOO OOOOOOOOOOO OOO O O OOOOO OOO OOOOOOOOO OOO OOO OOO
O     O O         O O O   O   O     O     O O O O O           O O O O O           O O   O O     O   O
O OOO OOOOO OOO OOO O O O O OOOOOOOOOOO OOOOO O O O OOOOO OOOOO OOOOO O O OOO OOOOO O O O OOO OOO O O
O O   O     O   O   O   O O   O     O           O     O       O       O O   O   O     O         O O O
O OOO O OOO OOO OOO OOOOOOO OOOOO O O OOO OOOOO O OOO OOOOOOOOOOO O O OOO OOOOOOO O OOO OOOOO OOO OOO
O O   O O   O O O O   O         O O   O   O     O O O O   O   O   O O O   O       O   O     O O     O
O OOO OOOOOOO O O O O O OOOOOOOOOOOOO O OOO OOOOO O O O OOO OOO O OOOOOOO O OOO OOOOO O OOO OOOOOOOOO
O O O     O O     O O O   O     O O   O O     O   O     O       O O O   O   O O O O O O O O O       O
O O O OOO O OOOOOOOOO O O OOO O O OOOOO O OOOOO O O OOOOO O OOO OOO O OOOOOOO O O O OOOOO OOO OOO OOO
O O     O O       O   O O O   O O       O O     O O     O O O     O       O O       O O       O     O
OOOOO O OOOOO OOO OOO OOOOOOOOO O OOO O O O OOO OOO OOOOOOOOO OOO O O OOOOO O OOOOO O OOO OOO OOO OOO
O O   O O O O O   O   O O O       O O O O   O   O O   O   O   O   O O O     O   O       O O     O O O
O OOOOOOO O O OOOOO O O O O OOO OOO OOO OOOOOOO O OOOOO OOOOOOOOO OOO O O O OOOOOOO OOO O O O OOOOO O
O O     O   O     O O     O   O   O           O O       O           O   O O O O       O   O O O     O
O OOOOO O OOO O OOOOOOOOOOOOO O O O OOO O O O O OOOOOOO OOOOOOO OOOOO O OOOOO O O O OOOOOOO O OOO OOO
O     O O     O       O   O   O O O O O O O O O O O     O   O   O   O O   O   O O O O O   O O   O O O
O O O O O O OOO OOOOOOO OOOOO OOOOOOO OOO OOOOO O O O OOO OOOOOOO O O OOO OOO OOO O O OOO OOOOO O O O
O O O O   O O     O   O   O   O   O     O O       O O     O     O O   O O O   O   O O         O     O
OOO O O OOOOOOOOO O OOOOO O OOO O O OOOOO O OOOOOOO O O OOOOOOO O OOO O OOOOO O OOO OOO O O OOOOOOOOO
O   O           O O O     O O   O   O O   O O       O O             O     O O O O     O O O O O   O O
O OOO OOOOOOOOO OOO O O OOOOOOOOOOO O O O OOO OOOOOOOOO OOOOOOO O OOO O O O O O O OOO OOO O O O OOO O
O   O   O O O     O   O   O O O         O     O O       O   O   O O   O O       O O O   O O   O     O
O OOOOO O O O O O O OOOOO O O O OOO OOOOOOOOO O O OOOOOOOOO OOO OOOOOOOOO OOOOO OOO O OOO OOOOO OOO O
O     O O     O O O O   O O     O O     O O     O   O   O     O       O O     O   O               O O
O OOO OOOOO OOOOOOO OOO O OOOOO O O O OOO O O O OOOOOOO OOO O O O O OOO O OOOOO OOO OOO OOOOOOO OOO O
O   O     O   O O       O O O   O O O O     O O O   O   O   O   O O O     O O     O O   O       O   O
O OOOOO OOOOOOO OOOOOOO OOO OOOOO O OOOOOOOOOOOOO OOO OOOOO OOO OOOOOOO OOO O OOO O O O OOOOOOOOOOOOO
O   O     O O       O     O   O   O     O     O O     O O   O     O     O O   O   O O O O           O
OOO O O OOO OOO OOOOO OOOOOOO OOO OOO O O OOO O OOO OOO OOOOOOOOO OOO O O OOO OOOOOOO O OOOOOOOOOOO O
O   O O O   O     O O   O       O O   O   O O O O O           O O   O O O O O   O     O   O       O O
O O O OOOOO O O OOO O OOO OOOOOOO OOO OOOOO OOO O O OOO OOOOOOO OOOOOOOOO O OOOOOOOOOOOOO OOO OOO O O
O O O       O O       O O O O   O         O           O O     O                   O     O       O   O
O OOOOO OOO OOOOOOOOO O O O OOO OOO OOOOO O OOOOOOO OOOOOOOOO OOOOO OOOOOOO O OOOOOOO OOOOOOOOO OOO O
O O   O   O O O   O   O       O   O O     O O O   O     O           O     O O O     O   O     O O   O
O OOO OOOOO O O O O OOO OOOOO O OOOOOOOOO O O O OOOOOOO OOOOOOOOOOO O O OOO OOO O OOO OOO OOOOOOOOO O
O       O O   O O           O     O   O O     O           O O O O O O O O   O O O O O   O O   O   O O
OOO OOOOO O O O O OOOOO OOOOO OOOOO OOO O O OOO O OOOOOOOOO O O O O O O O OOO O OOO OOO O O O OOO OOO
O         O O O O     O O           O     O O O O O       O         O O O   O O   O   O O   O O   O O
O OOO OOOOO OOOOO OOOOOOO OOOOOOOOO O OOO OOO OOOOOOOOO OOO OOO OOOOO O OOO O OOO OOO O OOO OOO OOO O
O   O O       O   O   O       O O     O       O O   O O   O O   O   O O   O     O O         O   O   O
O O O OOOOO O O O OOO OOO OOOOO OOOOO O OOOOO O OOO O O O O O OOO O O O OOOOOOO O O OOO OOOOOOO O OOO
O O O O     O   O     O   O O         O O O           O O O O     O   O       O O   O   O         O O
O OOO OOO OOOOO OOOOO O OOO O OOOOOOOOO O O O O OOO O O OOOOOOOOOOOOOOOOOOO OOO OOO O OOOOOOO O OOO O
O O     O   O     O   O   O   O           O O O   O O                         O     O         O    EO
OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
'''

def find_shortest_path(maze_str):
    # Split the maze into lines and remove empty lines
    maze_lines = [line for line in maze_str.strip().split('\n') if line.strip()]
    height = len(maze_lines)
    width = max(len(line) for line in maze_lines)

    # Create a grid and locate S and E
    grid = []
    start = None
    end = None
    for y, line in enumerate(maze_lines):
        row = list(line.ljust(width))
        grid.append(row)
        for x, char in enumerate(row):
            if char == 'S':
                start = (y, x)
            elif char == 'E':
                end = (y, x)

    if start is None or end is None:
        raise ValueError("Start ('S') or end ('E') position not found in the maze.")

    # Define movement directions corresponding to WASD
    moves = {
        'W': (-1, 0),
        'A': (0, -1),
        'S': (1, 0),
        'D': (0, 1),
    }

    # BFS to find the shortest path
    queue = deque()
    queue.append((start, []))  # position, path
    visited = set()
    visited.add(start)

    while queue:
        (y, x), path = queue.popleft()
        if (y, x) == end:
            return path  # Found the exit
        for move, (dy, dx) in moves.items():
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                if grid[ny][nx] in (' ', 'E') and (ny, nx) not in visited:
                    visited.add((ny, nx))
                    queue.append(((ny, nx), path + [move]))
    return None  # No path found

path = find_shortest_path(maze_str)
if path:
    print("Shortest path to the exit:")
    print(' -> '.join(path))
else:
    print("No path found from 'S' to 'E'.")