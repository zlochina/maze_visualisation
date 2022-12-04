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

def build_walls_array(m, n, maze_array):
    x = [0, 0, n, n, 0]
    y = [0, m, m, 0, 0]

    for coord_y in range(1, m+1):
        for coord_x in range(1, n+1):
            if 1 in maze_array[coord_y][coord_x]:
            
                # check for left neighbour
                if maze_array[coord_y][coord_x][1]:
                    x += [None, coord_x, coord_x - 1]
                    y += [None, m - coord_y, m - coord_y]
                # check for upper neighbour
                if maze_array[coord_y][coord_x][0]:
                    x += [None, coord_x, coord_x]
                    y += [None, m - coord_y, m - coord_y + 1]
    return (x, y)

# REFERENCE: https://en.wikipedia.org/wiki/Maze_generation_algorithm
def prim_algorithm(m, n, start_tuple = (1, 1), end_tuple = None):

    arr = np.zeros((m, n), dtype=np.short)
    numb_of_walls = m*n     # number of walls
    
    list_of_walls = []
    
    if end_tuple == None:
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

    #add_walls_to_list(list_of_walls, (end_tuple[1] - 1, end_tuple[0] - 1), m, n)
    #arr[end_tuple[1] - 1][end_tuple[0] - 1] = 1

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

# type_of_walls: 
# - 0, if env_type = walls_in_tiles
# - 1, if env_type = walls_between_tiles
def primitive_converter(maze_text, type_of_walls):
    '''This function converts text to matrix m+1 by n+1 with values from 0 up to 3
    where m, n - sizes of maze and value is computed like that: 
        value[m_i][n_i] += 1, when there is vertical wall joining [m_i, n_i] and [m_i + 1, n_i];
        value[m_i][n_i] += 2, when there is horizontal wall joining [m_i, n_i] and [m_i, n_i + 1]
        '''
    matrix = []
    maze_text_list = maze_text.split('\n')
    if type_of_walls:
        # thin walls
        
        row_tmp = maze_text_list[0]
        n_plus_one = len(row_tmp)
        m_plus_one = 1
        while len(row_tmp):
            array_tmp = []
            
            for char in row_tmp:
                array_tmp.append(1 if char == '|' else 0)

            row_tmp = maze_text_list[m_plus_one]            
            
            matrix.append(array_tmp)
            m_plus_one += 1
        
        array_tmp = [0 for _ in range(n_plus_one)]
        
        matrix.append(array_tmp)
        row_tmp = maze_text_list[m_plus_one]
        for i in range(m_plus_one):
            row_tmp = maze_text_list[m_plus_one + i]

            for j in range(len(row_tmp)):
                matrix[i][j] += 2 if row_tmp[j] == '-' else 0
    else:
        n = 0
        for m_i in range(len(maze_text_list)):
            array_tmp = []
            text_row = maze_text_list[m_i]
            n_tmp = len(text_row)
            for n_i in range(n_tmp):
                if text_row[n_i] == '#':
                    array_tmp.append(1)
                else:
                    array_tmp.append(0)
            
            if n_tmp > n:
                n = n_tmp
            
            matrix.append(array_tmp)

        # add zeros to empty space
        for m_i in range(len(maze_text_list)):
            for _ in range(n - len(matrix[m_i])):
                matrix[m_i].append(0)
    return matrix

# Thick walls only
def complex_converter(array_of_walls, m, n, type_of_walls):
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

    for m_i in range(m):
        for n_i in range(n):
            # filling matrix boundaries:
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
    
    if type_of_walls:
        # thin walls
        for m_i in range(m):
            for n_i in range(n):
                # filling matrix walls

                # case with vertical wall
                if array_of_walls[m_i][n_i] % 2 == 1:
                    matrix[m_i + 1][n_i][0] = 1
                # case with horizontal wall
                if array_of_walls[m_i][n_i] > 1:
                    matrix[m_i][n_i + 1][1] = 1
    else:
        # thick walls
        for m_i in range(m - 1):
            for n_i in range(n - 1):
                # filling matrix walls
                if array_of_walls[m_i][n_i]:
                    # add right and bottom wall
                    matrix[m_i + 1][n_i + 1] = [1, 1]
                    
                    # add upper wall
                    matrix[m_i][n_i + 1][1] = 1

                    # add left wall
                    matrix[m_i + 1][n_i][0] = 1

    return matrix
    


# Debugging
if __name__ == "__main__":
    """m = 9
    n = 9
    starting_point = (1, 1)
    array_of_walls = prim_algorithm(9, 9, (1, 1))
    print(array_of_walls)
    #maze_array = convert_walls(array_of_walls, m, n)
    #print(maze_array)
"""
    maze_text = """#####
#   #
#   #
#####"""
    #converted_maze = primitive_converter(maze_text, 0)
    #print(converted_maze)
    #converted_maze_2 = complex_converter(converted_maze, len(converted_maze), len(converted_maze[0]), 0)
    #print(converted_maze_2)    
    maze_text = """||||
|  |

---

---
"""
    converted_maze = primitive_converter(maze_text, 1)
    print(converted_maze)
    converted_maze_2 = complex_converter(converted_maze, len(converted_maze) - 1, len(converted_maze[0]) - 1, 1)
    print(converted_maze_2)
    