import tkinter as tk
import math
import random

def left(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[0][i][0] = [cube[1][x][2] for x in [2, 1, 0]][i]
        cube2[1][i][2] = [cube[5][x][0] for x in [2, 1, 0]][i]
        cube2[3][i][0] = [cube[0][x][0] for x in [0, 1, 2]][i]
        cube2[5][i][0] = [cube[3][x][0] for x in [0, 1, 2]][i]
        for j in range(3):
            cube2[2][i][j] = [[cube[2][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
    return cube2
def right(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[3][i][2] = [cube[5][x][2] for x in [0, 1, 2]][i]
        cube2[5][i][2] = [cube[1][x][0] for x in [2, 1, 0]][i]
        cube2[0][i][2] = [cube[3][x][2] for x in [0, 1, 2]][i]
        cube2[1][i][0] = [cube[0][x][2] for x in [2, 1, 0]][i]
        for j in range(3):
            cube2[4][i][j] = [[cube[4][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
    return cube2
def up(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[0][2][i] = [cube[2][x][2] for x in [2, 1, 0]][i]
        cube2[2][i][2] = [cube[5][0][x] for x in [0, 1, 2]][i]
        cube2[4][i][0] = [cube[0][2][x] for x in [0, 1, 2]][i]
        cube2[5][0][i] = [cube[4][x][0] for x in [2, 1, 0]][i]
        for j in range(3):
            cube2[3][i][j] = [[cube[3][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
    return cube2
def down(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[0][0][i] = [cube[4][x][2] for x in [0, 1, 2]][i]
        cube2[2][i][0] = [cube[0][0][x] for x in [2, 1, 0]][i]
        cube2[4][i][2] = [cube[5][2][x] for x in [2, 1, 0]][i]
        cube2[5][2][i] = [cube[2][x][0] for x in [0, 1, 2]][i]
        for j in range(3):
            cube2[1][i][j] = [[cube[1][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
    return cube2
def front(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[1][2][i] = [cube[4][2][x] for x in [0, 1, 2]][i]
        cube2[2][2][i] = [cube[1][2][x] for x in [0, 1, 2]][i]
        cube2[3][2][i] = [cube[2][2][x] for x in [0, 1, 2]][i]
        cube2[4][2][i] = [cube[3][2][x] for x in [0, 1, 2]][i]
        for j in range(3):
            cube2[5][i][j] = [[cube[5][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
    return cube2
def back(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[1][0][i] = [cube[2][0][x] for x in [0, 1, 2]][i]
        cube2[2][0][i] = [cube[3][0][x] for x in [0, 1, 2]][i]
        cube2[3][0][i] = [cube[4][0][x] for x in [0, 1, 2]][i]
        cube2[4][0][i] = [cube[1][0][x] for x in [0, 1, 2]][i]
        for j in range(3):
            cube2[0][i][j] = [[cube[0][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
    return cube2
def midM(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[0][i][1] = [cube[1][x][1] for x in [2, 1, 0]][i]
        cube2[1][i][1] = [cube[5][x][1] for x in [2, 1, 0]][i]
        cube2[3][i][1] = [cube[0][x][1] for x in [0, 1, 2]][i]
        cube2[5][i][1] = [cube[3][x][1] for x in [0, 1, 2]][i]
    return cube2
def midE(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[0][1][i] = [cube[4][x][1] for x in [0, 1, 2]][i]
        cube2[2][i][1] = [cube[0][1][x] for x in [2, 1, 0]][i]
        cube2[4][i][1] = [cube[5][1][x] for x in [2, 1, 0]][i]
        cube2[5][1][i] = [cube[2][x][1] for x in [0, 1, 2]][i]
    return cube2
def midS(cube):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for i in range(3):
        cube2[1][1][i] = [cube[4][1][x] for x in [0, 1, 2]][i]
        cube2[2][1][i] = [cube[1][1][x] for x in [0, 1, 2]][i]
        cube2[3][1][i] = [cube[2][1][x] for x in [0, 1, 2]][i]
        cube2[4][1][i] = [cube[3][1][x] for x in [0, 1, 2]][i]
    return cube2
def rotx(cube):
    cube2 = right(cube)
    for i in range(3):
        cube2 = left(cube2)
        cube2 = midM(cube2)
    return cube2
def roty(cube):
    cube2 = up(cube)
    for i in range(3):
        cube2 = down(cube2)
        cube2 = midE(cube2)
    return cube2
def rotz(cube):
    cube2 = front(cube)
    cube2 = midS(cube2)
    for i in range(3):
        cube2 = back(cube2)
    return cube2
def make_moves_sequence(cube, moves_seq):
    cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    for move in moves_seq:
        if move == "L":
            cube2 = left(cube2)
        elif move == "L'":
            for i in range(3):
                cube2 = left(cube2)
        elif move == "R":
            cube2 = right(cube2)
        elif move == "R'":
            for i in range(3):
                cube2 = right(cube2)
        elif move == "U":
            cube2 = up(cube2)
        elif move == "U'":
            for i in range(3):
                cube2 = up(cube2)
        elif move == "D":
            cube2 = down(cube2)
        elif move == "D'":
            for i in range(3):
                cube2 = down(cube2)
        elif move == "F":
            cube2 = front(cube2)
        elif move == "F'":
            for i in range(3):
                cube2 = front(cube2)
        elif move == "B":
            cube2 = back(cube2)
        elif move == "B'":
            for i in range(3):
                cube2 = back(cube2)
        elif move == "M":
            cube2 = midM(cube2)
        elif move == "M'":
            for i in range(3):
                cube2 = midM(cube2)
        elif move == "E":
            cube2 = midE(cube2)
        elif move == "E'":
            for i in range(3):
                cube2 = midE(cube2)
        elif move == "S":
            cube2 = midS(cube2)
        elif move == "S'":
            for i in range(3):
                cube2 = midS(cube2)
        elif move == "x":
            cube2 = rotx(cube2)
        elif move == "x'":
            for i in range(3):
                cube2 = rotx(cube2)
        elif move == "y":
            cube2 = roty(cube2)
        elif move == "y'":
            for i in range(3):
                cube2 = roty(cube2)
        elif move == "z":
            cube2 = rotz(cube2)
        elif move == "z'":
            for i in range(3):
                cube2 = rotz(cube2)
        elif move == "":
            pass
    return cube2
def print_rubiks_cube(cube):
    for i in range(3):
        print("\n" + 14 * " ", end = "")
        for piece in cube[0][i]:
            print(piece, end = " ")
    for i in range(3):
        print("\n", end = "")
        for j in range(4):
            for k in range(3):
                print(cube[j+1][i][k], end = " ")
            print(" ", end = "")
    for i in range(3):
        print("\n" + 14 * " ", end = "")
        for piece in cube[-1][i]:
            print(piece, end = " ")

def reset_cube():
    global rubiks_cube
    rubiks_cube = [[[["b", "y", "o", "w", "r", "g"][x] for z in range(3)] for y in range(3)] for x in range(6)]
    make_move_graphic(None, [], rubiks_cube)
def reset_cube_event(event):
    if bindings_are_activated: reset_cube()
def scramble_cube(cube, scramble_moves_number):
    global cube_background, moves_seq_text
    try:
        cube_background.delete(moves_seq_text)
    except Exception:
        pass
    moves_seq = []
    # moves_matrix = ["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'", "x", "x'", "y", "y'", "z", "z'"]
    moves_matrix = ["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'"]
    for i in range(scramble_moves_number):
        moves_seq.append(random.choice(moves_matrix))
    print("\n")
    print(moves_seq)
    moves_seq_text = cube_background.create_text(float(cube_background["width"]) / 2, 30, fill = "darkblue", font = "Times 20 italic bold", text = moves_seq)
    make_move_graphic(None, [""] + moves_seq, cube)
def scramble_cube_event(event):
    global rubiks_cube
    if bindings_are_activated: scramble_cube(rubiks_cube, 20)
def draw_rubiks_cube_event(event):
    global rubiks_cube, square_side_length, sides_distortion, borders_width, front_cube_side_centre_point, moves_speed
    global cube_background
    if event.widget == sides_distortion_button:
        sides_distortion = alternate_matrix_elements([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], sides_distortion)
        sides_distortion_button.configure(text = sides_distortion)
    elif event.widget == borders_width_button:
        borders_width = alternate_matrix_elements([0, 2, 5, 10, 20], borders_width)
        borders_width_button.configure(text = borders_width)
    elif event.widget == cube_size_button:
        square_side_length = alternate_matrix_elements([25, 50, 75, 100, 125], square_side_length)
        cube_size_button.configure(text = square_side_length)
    elif event.widget == moves_speed_button:
        moves_speed = alternate_matrix_elements([0, 0.1, 0.5, 1.0, 2.0, 5.0], moves_speed)
        moves_speed_button.configure(text = moves_speed)
    centre_offset =  3 / 2 * sides_distortion * square_side_length
    front_cube_side_centre_point = [float(cube_background["width"]) / 2 - centre_offset / math.sqrt(2), float(cube_background["height"]) / 2 + centre_offset / math.sqrt(2)]
    make_move_graphic(None, [], rubiks_cube)

def draw_front_cube_side(background, front_cube_side, square_side_length, borders_width, front_cube_side_centre_point):
    fs = front_cube_side; fc = front_cube_side_centre_point; sl = square_side_length
    global fs_up_left_piece, fs_up_middle_piece, fs_up_right_piece, fs_left_middle_piece, fs_centre_piece, fs_right_middle_piece, fs_down_left_piece, fs_down_middle_piece, fs_down_right_piece
    try:
        background.delete(fs_up_left_piece); background.delete(fs_up_middle_piece); background.delete(fs_up_right_piece)
        background.delete(fs_left_middle_piece); background.delete(fs_centre_piece); background.delete(fs_right_middle_piece)
        background.delete(fs_down_left_piece); background.delete(fs_down_middle_piece); background.delete(fs_down_right_piece)
    except Exception:
        pass
    fs_centre_piece = background.create_rectangle(fc[0] - sl / 2, fc[1] - sl / 2, fc[0] + sl / 2, fc[1] + sl / 2, fill = get_color(fs[1][1]), width = borders_width, outline = "black")
    fs_up_left_piece = background.create_rectangle(fc[0] - 3 * sl / 2, fc[1] - 3 * sl / 2, fc[0] - sl / 2, fc[1] - sl / 2, fill = get_color(fs[0][0]), width = borders_width, outline = "black")
    fs_up_middle_piece = background.create_rectangle(fc[0] - sl / 2, fc[1] - 3 * sl / 2, fc[0] + sl / 2, fc[1] - sl / 2, fill = get_color(fs[0][1]), width = borders_width, outline = "black")
    fs_up_right_piece = background.create_rectangle(fc[0] + sl / 2, fc[1] - 3 * sl / 2, fc[0] + 3 * sl / 2, fc[1] - sl / 2, fill = get_color(fs[0][2]), width = borders_width, outline = "black")
    fs_left_middle_piece = background.create_rectangle(fc[0] - 3 * sl / 2, fc[1] - sl / 2, fc[0] - sl / 2, fc[1] + sl / 2, fill = get_color(fs[1][0]), width = borders_width, outline = "black")
    fs_right_middle_piece = background.create_rectangle(fc[0] + sl / 2, fc[1] - sl / 2, fc[0] + 3 * sl / 2, fc[1] + sl / 2, fill = get_color(fs[1][2]), width = borders_width, outline = "black")
    fs_down_left_piece = background.create_rectangle(fc[0] - 3 * sl / 2, fc[1] + sl / 2, fc[0] - sl / 2, fc[1] + 3 * sl / 2, fill = get_color(fs[2][0]), width = borders_width, outline = "black")
    fs_down_middle_piece = background.create_rectangle(fc[0] - sl / 2, fc[1] + sl / 2, fc[0] + sl / 2, fc[1] + 3 * sl / 2, fill = get_color(fs[2][1]), width = borders_width, outline = "black")
    fs_down_right_piece = background.create_rectangle(fc[0] + sl / 2, fc[1] + sl / 2, fc[0] + 3 * sl / 2, fc[1] + 3 * sl / 2, fill = get_color(fs[2][2]), width = borders_width, outline = "black")
def draw_up_cube_side(background, up_cube_side, square_side_length, sides_distortion, borders_width, up_cube_side_down_left_point):
    us = up_cube_side; udl = up_cube_side_down_left_point; ps1 = square_side_length * sides_distortion; ps2 = square_side_length; pa1 = math.radians(45); pa2 = math.radians(0)
    global us_up_left_piece, us_up_middle_piece, us_up_right_piece, us_left_middle_piece, us_centre_piece, us_right_middle_piece, us_down_left_piece, us_down_middle_piece, us_down_right_piece
    try:
        background.delete(us_up_left_piece); background.delete(us_up_middle_piece); background.delete(us_up_right_piece)
        background.delete(us_left_middle_piece); background.delete(us_centre_piece); background.delete(us_right_middle_piece)
        background.delete(us_down_left_piece); background.delete(us_down_middle_piece); background.delete(us_down_right_piece)
    except Exception:
        pass
    udl2 = udl; us_down_left_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[2][0]), width = borders_width, outline = "black")
    udl2 = [udl[0] + ps2 * math.cos(pa2), udl[1] - ps2 * math.sin(pa2)]; us_down_middle_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[2][1]), width = borders_width, outline = "black")
    udl2 = [udl[0] + 2 * ps2 * math.cos(pa2), udl[1] - 2 * ps2 * math.sin(pa2)]; us_down_right_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[2][2]), width = borders_width, outline = "black")
    udl2 = [udl[0] + ps1 * math.cos(pa1), udl[1] - ps1 * math.sin(pa1)]; us_left_middle_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[1][0]), width = borders_width, outline = "black")
    udl2 = [udl[0] + ps1 * math.cos(pa1) + ps2 * math.cos(pa2), udl[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; us_centre_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[1][1]), width = borders_width, outline = "black")
    udl2 = [udl[0] + ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), udl[1] - ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; us_right_middle_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[1][2]), width = borders_width, outline = "black")
    udl2 = [udl[0] + 2 * ps1 * math.cos(pa1), udl[1] - 2 * ps1 * math.sin(pa1)]; us_up_left_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[0][0]), width = borders_width, outline = "black")
    udl2 = [udl[0] + 2 * ps1 * math.cos(pa1) + ps2 * math.cos(pa2), udl[1] - 2 * ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; us_up_middle_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[0][1]), width = borders_width, outline = "black")
    udl2 = [udl[0] + 2 * ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), udl[1] - 2 * ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; us_up_right_piece = background.create_polygon([udl2[0], udl2[1], udl2[0] + ps2 * math.cos(pa2), udl2[1] - ps2 * math.sin(pa2), udl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), udl2[0] + ps1 * math.cos(pa1), udl2[1] - ps1 * math.sin(pa1)], fill = get_color(us[0][2]), width = borders_width, outline = "black")
def draw_right_cube_side(background, right_cube_side, square_side_length, sides_distortion, borders_width, right_cube_side_down_left_point):
    rs = right_cube_side; rdl = right_cube_side_down_left_point; ps1 = square_side_length; ps2 = square_side_length * sides_distortion; pa1 = math.radians(90); pa2 = math.radians(45)
    global rs_up_left_piece, rs_up_middle_piece, rs_up_right_piece, rs_left_middle_piece, rs_centre_piece, rs_right_middle_piece, rs_down_left_piece, rs_down_middle_piece, rs_down_right_piece
    try:
        background.delete(rs_up_left_piece); background.delete(rs_up_middle_piece); background.delete(rs_up_right_piece)
        background.delete(rs_left_middle_piece); background.delete(rs_centre_piece); background.delete(rs_right_middle_piece)
        background.delete(rs_down_left_piece); background.delete(rs_down_middle_piece); background.delete(rs_down_right_piece)
    except Exception:
        pass
    rdl2 = rdl; rs_down_left_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[2][2]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + ps2 * math.cos(pa2), rdl[1] - ps2 * math.sin(pa2)]; rs_down_middle_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[1][2]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + 2 * ps2 * math.cos(pa2), rdl[1] - 2 * ps2 * math.sin(pa2)]; rs_down_right_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[0][2]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + ps1 * math.cos(pa1), rdl[1] - ps1 * math.sin(pa1)]; rs_left_middle_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[2][1]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + ps1 * math.cos(pa1) + ps2 * math.cos(pa2), rdl[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; rs_centre_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[1][1]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), rdl[1] - ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; rs_right_middle_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[0][1]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + 2 * ps1 * math.cos(pa1), rdl[1] - 2 * ps1 * math.sin(pa1)]; rs_up_left_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[2][0]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + 2 * ps1 * math.cos(pa1) + ps2 * math.cos(pa2), rdl[1] - 2 * ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; rs_up_middle_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[1][0]), width = borders_width, outline = "black")
    rdl2 = [rdl[0] + 2 * ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), rdl[1] - 2 * ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; rs_up_right_piece = background.create_polygon([rdl2[0], rdl2[1], rdl2[0] + ps2 * math.cos(pa2), rdl2[1] - ps2 * math.sin(pa2), rdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), rdl2[0] + ps1 * math.cos(pa1), rdl2[1] - ps1 * math.sin(pa1)], fill = get_color(rs[0][0]), width = borders_width, outline = "black")
def get_color(first_letter):
    color = ["blue", "yellow", "orange", "white", "red", "green"][["b", "y", "o", "w", "r", "g"].index(first_letter)]
    return color
def make_move_graphic(event, moves_seq, cube):
    global rubiks_cube, square_side_length, sides_distortion, borders_width, front_cube_side_centre_point, moves_speed
    global cube_background, bindings_are_activated
    if event == None:
        bindings_are_activated = False
        if moves_seq == []:
            draw_front_cube_side(cube_background, cube[5], square_side_length, borders_width, front_cube_side_centre_point)
            draw_up_cube_side(cube_background, cube[3], square_side_length, sides_distortion, borders_width, [front_cube_side_centre_point[0] - 3 * square_side_length / 2, front_cube_side_centre_point[1] - 3 * square_side_length / 2])
            draw_right_cube_side(cube_background, cube[4], square_side_length, sides_distortion, borders_width, [front_cube_side_centre_point[0] + 3 * square_side_length / 2, front_cube_side_centre_point[1] + 3 * square_side_length / 2])
            bindings_are_activated = True
        else:
            move = []
            move.append(moves_seq[0])
            rubiks_cube = make_moves_sequence(cube, move)
            draw_front_cube_side(cube_background, rubiks_cube[5], square_side_length, borders_width, front_cube_side_centre_point)
            draw_up_cube_side(cube_background, rubiks_cube[3], square_side_length, sides_distortion, borders_width, [front_cube_side_centre_point[0] - 3 * square_side_length / 2, front_cube_side_centre_point[1] - 3 * square_side_length / 2])
            draw_right_cube_side(cube_background, rubiks_cube[4], square_side_length, sides_distortion, borders_width, [front_cube_side_centre_point[0] + 3 * square_side_length / 2, front_cube_side_centre_point[1] + 3 * square_side_length / 2])
            cube_background.after(int(1000 * moves_speed), lambda: make_move_graphic(None, moves_seq[1:], rubiks_cube))
    elif event != None and bindings_are_activated:
        if event.keysym == "Left":
            rubiks_cube = make_moves_sequence(cube, ["y"])
        elif event.keysym == "Right":
            rubiks_cube = make_moves_sequence(cube, ["y'"])
        elif event.keysym == "Up":
            rubiks_cube = make_moves_sequence(cube, ["x"])
        elif event.keysym == "Down":
            rubiks_cube = make_moves_sequence(cube, ["x'"])
        elif event.keysym == "r":
            rubiks_cube = make_moves_sequence(cube, ["R"])
        elif event.keysym == "R":
            rubiks_cube = make_moves_sequence(cube, ["R'"])
        elif event.keysym == "l":
            rubiks_cube = make_moves_sequence(cube, ["L"])
        elif event.keysym == "L":
            rubiks_cube = make_moves_sequence(cube, ["L'"])
        elif event.keysym == "u":
            rubiks_cube = make_moves_sequence(cube, ["U"])
        elif event.keysym == "U":
            rubiks_cube = make_moves_sequence(cube, ["U'"])
        elif event.keysym == "d":
            rubiks_cube = make_moves_sequence(cube, ["D"])
        elif event.keysym == "D":
            rubiks_cube = make_moves_sequence(cube, ["D'"])
        elif event.keysym == "f":
            rubiks_cube = make_moves_sequence(cube, ["F"])
        elif event.keysym == "F":
            rubiks_cube = make_moves_sequence(cube, ["F'"])
        elif event.keysym == "b":
            rubiks_cube = make_moves_sequence(cube, ["B"])
        elif event.keysym == "B":
            rubiks_cube = make_moves_sequence(cube, ["B'"])
        elif event.keysym == "m":
            rubiks_cube = make_moves_sequence(cube, ["M"])
        elif event.keysym == "M":
            rubiks_cube = make_moves_sequence(cube, ["M'"])
        elif event.keysym == "e":
            rubiks_cube = make_moves_sequence(cube, ["E"])
        elif event.keysym == "E":
            rubiks_cube = make_moves_sequence(cube, ["E'"])
        elif event.keysym == "s":
            rubiks_cube = make_moves_sequence(cube, ["S"])
        elif event.keysym == "S":
            rubiks_cube = make_moves_sequence(cube, ["S'"])
        draw_front_cube_side(cube_background, rubiks_cube[5], square_side_length, borders_width, front_cube_side_centre_point)
        draw_up_cube_side(cube_background, rubiks_cube[3], square_side_length, sides_distortion, borders_width, [front_cube_side_centre_point[0] - 3 * square_side_length / 2, front_cube_side_centre_point[1] - 3 * square_side_length / 2])
        draw_right_cube_side(cube_background, rubiks_cube[4], square_side_length, sides_distortion, borders_width, [front_cube_side_centre_point[0] + 3 * square_side_length / 2, front_cube_side_centre_point[1] + 3 * square_side_length / 2])
    
class menu_button():
    def __init__(self, background, button_text, button_font, button_fg, button_bg, button_xcor, button_ycor, button_func):
        self.button = tk.Label(background, text = button_text, font = button_font, fg = button_fg, bg = button_bg)
        self.button.place(x = button_xcor, y = button_ycor, anchor = "center")
        self.button.bind("<Enter>", lambda event, button = self.button: button.configure(font = "Arial {} bold".format(int(button["font"].split(" ")[1]) + 5)))
        self.button.bind("<Leave>", lambda event, button = self.button: button.configure(font = button_font))
        self.button.bind("<Button-1>", lambda event: button_func(event))
class menu_label():
    def __init__(self, background, label_text, label_font, label_fg, label_bg, label_xcor, label_ycor):
        self.label = tk.Label(background, text = label_text, font = label_font, fg = label_fg, bg = label_bg)
        self.label.place(x = label_xcor, y = label_ycor, anchor = "center")
def alternate_matrix_elements(matrix, index_element):
        return (matrix[1:] + [matrix[0]])[matrix.index(index_element)]

root = tk.Tk()
root.title("Rubik's cube")
root.geometry("+0+0")
cube_background_width = (4 / 5) * root.winfo_screenheight()
cube_background_height = cube_background_width
menu_background_width = cube_background_width / 3
menu_background_height = cube_background_height
menu_background = tk.Frame(root, width = menu_background_width, height = menu_background_height, bg = "black", bd = 0, relief = "solid")
menu_background.grid(row = 0, column = 0, sticky = tk.NSEW)
cube_background = tk.Canvas(root, width = cube_background_width, height = cube_background_height, bg = "cyan", bd = 0, relief = "solid")
cube_background.grid(row = 0, column = 1, sticky = tk.NSEW)

square_side_length = 100
borders_width = 5
sides_distortion = 0.4
centre_offset =  3 / 2 * sides_distortion * square_side_length
front_cube_side_centre_point = [cube_background_width / 2 - centre_offset / math.sqrt(2), cube_background_height / 2 + centre_offset / math.sqrt(2)]
moves_speed = 0
rubiks_cube = [[[["b", "y", "o", "w", "r", "g"][x] for z in range(3)] for y in range(3)] for x in range(6)]
reset_cube()
# scramble_cube(rubiks_cube, 20)

bindings_are_activated = True
root.bind('<Left>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<Right>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<Up>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<Down>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<r>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<R>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<l>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<L>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<u>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<U>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<d>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<D>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<f>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<F>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<b>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<B>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<m>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<M>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<e>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<E>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<s>', lambda event: make_move_graphic(event, [], rubiks_cube))
root.bind('<S>', lambda event: make_move_graphic(event, [], rubiks_cube))

reset_button = menu_button(menu_background, "reset", "Arial 25 bold", "white", "black", menu_background_width / 2, 50, reset_cube_event).button

scramble_cube_menu_cors = [menu_background_width / 2, 120]
scramble_cube_menu_label = menu_label(menu_background, "Scramble cube:", "Times 25 bold", "yellow", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1]).label
moves_speed_label = menu_label(menu_background, "moves\nspeed (sec)", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 30, scramble_cube_menu_cors[1] + 60).label
moves_speed_label2 = menu_label(menu_background, ":", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] + 50, scramble_cube_menu_cors[1] + 60).label
moves_speed_button = menu_button(menu_background, moves_speed, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 80, scramble_cube_menu_cors[1] + 60, draw_rubiks_cube_event).button
scramble_button = menu_button(menu_background, "scramble", "Arial 25 bold", "white", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1] + 120, scramble_cube_event).button

cube_graphics_menu_cors = [menu_background_width / 2, 320]
cube_graphics_menu_label = menu_label(menu_background, "Cube graphics:", "Times 25 bold", "yellow", "black", cube_graphics_menu_cors[0], cube_graphics_menu_cors[1]).label
cube_size_label = menu_label(menu_background, "cube size", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 40, cube_graphics_menu_cors[1] + 50).label
cube_size_label2 = menu_label(menu_background, ":", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 50).label
cube_size_button = menu_button(menu_background, square_side_length, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + 50, draw_rubiks_cube_event).button
sides_distortion_label = menu_label(menu_background, "sides\ndistortion", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 40, cube_graphics_menu_cors[1] + 110).label
sides_distortion_label2 = menu_label(menu_background, ":", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 110).label
sides_distortion_button = menu_button(menu_background, sides_distortion, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + 110, draw_rubiks_cube_event).button
borders_width_label = menu_label(menu_background, "borders\nwidth", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 40, cube_graphics_menu_cors[1] + 180).label
borders_width_label2 = menu_label(menu_background, ":", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 180).label
borders_width_button = menu_button(menu_background, borders_width, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + 180, draw_rubiks_cube_event).button

root.mainloop()