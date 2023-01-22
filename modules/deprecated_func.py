import numpy as np


def maze_generator(m, n, thin_walls=True):
    matrix = []

    # add dimensionality as to every elements is responsible for point,
    # not for the full tile
    m += 1
    n += 1

    # 3 dim array m x n x 2
    for i in range(m):
        matrix.append([])
        for _ in range(n):
            matrix[i].append([])

    # adding thin walls
    if thin_walls:
        for m_i in range(m):
            for n_i in range(n):
                # filling matrix:
                #   1) first number array is connection between this point and upper point;
                #   2) second number in array is coonection between this point and left point
                if m_i == 0 and n_i == 0:
                    matrix[m_i][n_i] = [0, 0]
                elif m_i == m - 1 and n_i == n - 1:
                    matrix[m_i][n_i] = [1, 1]
                elif m_i == 0 or m_i == m - 1:
                    matrix[m_i][n_i] = [0, 1]
                elif n_i == 0 or n_i == n - 1:
                    matrix[m_i][n_i] = [1, 0]
                else:
                    matrix[m_i][n_i] = [0, 0]

    return matrix


# REFERENCE: https://en.wikipedia.org/wiki/Maze_generation_algorithm
def prim_algorithm(m, n, start_tuple=(1, 1), end_tuple=None):

    arr = np.zeros((m, n), dtype=np.short)
    numb_of_walls = m * n  # number of walls

    list_of_walls = []

    if end_tuple is None:
        end_tuple = (n, m)

    def add_walls_to_list(list_of_walls, pos_coord, m, n):
        x, y = pos_coord[1], pos_coord[0]
        # add x-axis neigbours
        if x - 1 != -1:
            list_of_walls.append((x - 1, y))
        if x + 1 != n:
            list_of_walls.append((x + 1, y))

        # add y-axis neigbours
        if y - 1 != -1:
            list_of_walls.append((x, y - 1))
        if y + 1 != m:
            list_of_walls.append((x, y + 1))

    add_walls_to_list(list_of_walls, (start_tuple[1] - 1, start_tuple[0] - 1), m, n)

    arr[start_tuple[1] - 1][start_tuple[0] - 1] = 1

    while len(list_of_walls) > 0:
        rand_pick_num = np.random.choice(range(len(list_of_walls)), 1)[0]
        rand_pick = list_of_walls[rand_pick_num]
        x, y = rand_pick[0], rand_pick[1]
        sum = 0
        if x - 1 != -1:
            sum += arr[y][x - 1]
        if x + 1 != n:
            sum += arr[y][x + 1]
        if y - 1 != -1:
            sum += arr[y - 1][x]
        if y + 1 != m:
            sum += arr[y + 1][x]

        if sum == 1:
            arr[y][x] = 1
            numb_of_walls -= 1
            add_walls_to_list(list_of_walls, (y, x), m, n)
        list_of_walls.remove((rand_pick))

    return arr
