import numpy as np


def build_walls_array(m, n, maze_array):
    x = [0, 0, n, n, 0]
    y = [0, m, m, 0, 0]

    for coord_y in range(1, m + 1):
        for coord_x in range(1, n + 1):
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


# type_of_walls:
# - 0, if env_type = walls_in_tiles
# - 1, if env_type = walls_between_tiles
def primitive_converter(maze_text, type_of_walls):
    """This function converts text to matrix m+1 by n+1 with values
    from 0 up to 3
    where m, n - sizes of maze and value is computed like that:
        value[m_i][n_i] += 1, when there is vertical wall joining [m_i, n_i]
            and [m_i + 1, n_i];
        value[m_i][n_i] += 2, when there is horizontal wall joining [m_i, n_i]
            and [m_i, n_i + 1]
    """
    matrix = []
    maze_text_list = maze_text.split("\n")
    if type_of_walls:
        # thin walls

        row_tmp = maze_text_list[0]
        n_plus_one = len(row_tmp)
        m_plus_one = 1
        while len(row_tmp):
            array_tmp = []

            for char in row_tmp:
                array_tmp.append(1 if char == "|" else 0)

            row_tmp = maze_text_list[m_plus_one]

            matrix.append(array_tmp)
            m_plus_one += 1

        array_tmp = [0 for _ in range(n_plus_one)]

        matrix.append(array_tmp)
        row_tmp = maze_text_list[m_plus_one]
        for i in range(m_plus_one):
            row_tmp = maze_text_list[m_plus_one + i]

            for j in range(len(row_tmp)):
                matrix[i][j] += 2 if row_tmp[j] == "-" else 0
    else:
        n = 0
        for m_i in range(len(maze_text_list)):
            array_tmp = []
            text_row = maze_text_list[m_i]
            n_tmp = len(text_row)
            for n_i in range(n_tmp):
                if text_row[n_i] == "#":
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
            #   1) first number array is connection between
            #      this point and upper point;
            #   2) second number in array is coonection between
            #      this point and left point

            if m_i == 0 and n_i == 0:
                matrix[m_i][n_i] = [0, 0]
            elif m_i == m - 1 and n_i == 0:
                matrix[m_i][n_i] = [1, 0]
            elif m_i == 0 and n_i == n - 1:
                matrix[m_i][n_i] = [0, 1]
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
                if array_of_walls[m_i][n_i] // 2 == 1:
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


def bitmap_converter(image):
    img = np.array(image)[::-1]
    black_arr = np.array([0, 0, 0])
    white_arr = np.array([255, 255, 255])
    start_point = np.array([0, 0, 255])
    end_point = np.array([255, 0, 0])
    m, n = len(img), len(img[0])
    matrix = []
    start_p_coord = (-1, -1)
    end_p_coord = (-1, -1)

    for _ in range(n):
        matrix.append([])

    for i in range(m):
        for j in range(n):
            tile_tmp = img[i][j]
            bool_1 = (tile_tmp == black_arr).all()

            matrix[i].append(1) if bool_1 else matrix[i].append(0)

            if not bool_1 and not (tile_tmp == white_arr).all():
                if (tile_tmp == start_point).all():
                    start_p_coord = (i, j)
                elif (tile_tmp == end_point).all():
                    end_p_coord = (i, j)

    return matrix, (start_p_coord, end_p_coord)


# type_of_walls:
# - 0, if env_type = walls_in_tiles
# - 1, if env_type = walls_between_tiles
# TODO update to be like complex_converter
def reverse_complex_converter(array_of_walls, m, n, type_of_walls):
    """
    - function to convert complex representation of maze to primitive one
    - only works for converting from walls_in_tiles to walls_between_tiles
    - as otherwise seems illogical to do
    """
    matrix = []
    for _ in range(m + 1):
        matrix.append([])
        for _ in range(n + 1):
            matrix[-1].append(0)

    if type_of_walls:
        raise NameError("ReverseConvertingError")

    for i in range(m + 1):
        for j in range(n + 1):
            if array_of_walls[i][j][0]:
                matrix[i - 1][j] += 1

            if array_of_walls[i][j][1]:
                matrix[i][j - 1] += 2

    return matrix


# type_of_walls:
# - 0, if env_type = walls_in_tiles
# - 1, if env_type = walls_between_tiles
def reverse_primitive_converter(walls, type_of_walls):
    """
    - function to convert from primitive representation of maze boundaries
      to the text representation of maze boundaries
    """
    txt = ""
    m, n = len(walls), len(walls[0])

    if type_of_walls:
        txt_to_add = ""
        for m_i in range(m):
            txt_tmp = ""
            for n_i in range(n):
                if walls[m_i][n_i] & 1 and not m_i == m - 1:
                    txt += "|"
                elif not m_i == m - 1:
                    txt += " "

                if walls[m_i][n_i] & 2 and not n_i == n - 1:
                    txt_to_add += txt_tmp + "-"
                    txt_tmp = ""
                elif not n_i == n - 1:
                    txt_tmp += " "

            if not m_i == m - 1:
                txt += "\n"

            txt_to_add += "\n"
        return txt + "\n" + txt_to_add
    else:
        for m_i in range(m):
            txt_tmp = ""
            for n_i in range(n):
                if walls[m_i][n_i]:
                    txt += txt_tmp + "#"
                    txt_tmp = ""
                else:
                    txt_tmp += " "
            txt += "\n"
        return txt
    raise NameError("ReverseConvertingError: unexpected issue")


def reverse_bitmap_converter(walls):
    """
    - function converting primitive representation of maze boundaries
      to .bmp content, which is to save after the function
    """
    m, n = len(walls), len(walls[0])
    matrix = []
    black_arr = (0, 0, 0)
    white_arr = (255, 255, 255)
    # start_point = (0, 0, 255)
    # end_point = (255, 0, 0)

    for m_i in range(m):
        matrix.append([])
        for n_i in range(n):
            if walls[m_i][n_i]:
                matrix[m_i].append(black_arr)
            else:
                matrix[m_i].append(white_arr)
    return np.array(matrix, dtype=np.uint8)


# Debugging
if __name__ == "__main__":
    """m = 9
    n = 9
    starting_point = (1, 1)
    array_of_walls = prim_algorithm(9, 9, (1, 1))
    print(array_of_walls)
    #maze_array = convert_walls(array_of_walls, m, n)
    #print(maze_array)"""
    maze_text = """#####
#   #
#   #
#####"""
    # converted_maze = primitive_converter(maze_text, 0)
    # print(converted_maze)
    # converted_maze_2 = complex_converter(converted_maze, len(converted_maze),
    # len(converted_maze[0]), 0)
    # print(converted_maze_2)
    maze_text = """||||
|  |

---

---
"""
    converted_maze = primitive_converter(maze_text, 1)
    print(converted_maze)
    converted_maze_2 = complex_converter(
        converted_maze, len(converted_maze) - 1, len(converted_maze[0]) - 1, 1
    )
    print(converted_maze_2)
