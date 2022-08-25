import tkinter as tk
import math
import random

class rubiks_cube():
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's cube")
        self.root.geometry("+0+0")
        self.cube_background_width = (3 / 4) * self.root.winfo_screenheight()
        self.cube_background_height = self.cube_background_width
        self.play_background_width = self.cube_background_width
        self.play_background_height = self.cube_background_height / 6
        self.menu_background_width = self.cube_background_width / 2
        self.menu_background_height = self.cube_background_height + self.play_background_height
        self.menu_background = tk.Frame(root, width = self.menu_background_width, height = self.menu_background_height, bg = "black", bd = 0, relief = "solid")
        self.menu_background.grid(row = 0, column = 0, rowspan = 2, sticky = tk.NSEW)
        self.cube_background = tk.Canvas(root, width = self.cube_background_width, height = self.cube_background_height, bg = "cyan", bd = 0, relief = "solid")
        self.cube_background.grid(row = 0, column = 1, sticky = tk.NSEW)
        self.play_background = tk.Canvas(root, width = self.play_background_width, height = self.play_background_height, bg = "yellow", bd = 0, relief = "solid")
        self.play_background.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.square_side_length = 100
        self.square_side_lengths_matrix = [25, 50, 75, 100, 125]
        self.borders_width = 5
        self.borders_widths_matrix = [0, 2, 5, 10, 20]
        self.sides_distortion = 0.4
        self.sides_distortions_matrix = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        centre_offset =  3 / 2 * self.sides_distortion * self.square_side_length
        self.front_cube_side_centre_point = [self.cube_background_width / 2 - centre_offset / math.sqrt(2), self.cube_background_height / 2 + centre_offset / math.sqrt(2)]
        self.moves_speed = 0
        self.moves_speeds_matrix = [0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
        self.scramble_moves = 10
        self.scramble_moves_matrix = [1, 3, 5, 10, 20]
        self.reset_cube()
        # scramble_cube(rubiks_cube, 20)

        self.reset_button = menu_button(self.menu_background, "reset", "Arial 25 bold", "white", "black", self.menu_background_width / 2, 50, self.reset_cube_event).button

        scramble_cube_menu_cors = [self.menu_background_width / 2, 120]
        self.scramble_cube_menu_label = menu_label(self.menu_background, "Scramble cube:", "Times 25 bold", "yellow", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1]).label
        self.moves_speed_label = menu_label(self.menu_background, "moves\nspeed (sec)", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 30, scramble_cube_menu_cors[1] + 60).label
        self.moves_speed_label2 = menu_label(self.menu_background, ":", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] + 50, scramble_cube_menu_cors[1] + 60).label
        self.moves_speed_button = menu_button(self.menu_background, self.moves_speed, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 80, scramble_cube_menu_cors[1] + 60, self.change_game_settings).button
        self.moves_number_label = menu_label(self.menu_background, "moves\nnumber", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 30, scramble_cube_menu_cors[1] + 120).label
        self.moves_number_label2 = menu_label(self.menu_background, ":", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] + 50, scramble_cube_menu_cors[1] + 120).label
        self.moves_number_button = menu_button(self.menu_background, self.scramble_moves, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 80, scramble_cube_menu_cors[1] + 120, self.change_game_settings).button
        self.scramble_button = menu_button(self.menu_background, "scramble", "Arial 25 bold", "white", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1] + 180, self.scramble_cube_event).button

        cube_graphics_menu_cors = [self.menu_background_width / 2, 380]
        self.cube_graphics_menu_label = menu_label(self.menu_background, "Cube graphics:", "Times 25 bold", "yellow", "black", cube_graphics_menu_cors[0], cube_graphics_menu_cors[1]).label
        self.cube_size_label = menu_label(self.menu_background, "cube size", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 40, cube_graphics_menu_cors[1] + 50).label
        self.cube_size_label2 = menu_label(self.menu_background, ":", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 50).label
        self.cube_size_button = menu_button(self.menu_background, self.square_side_length, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + 50, self.change_game_settings).button
        self.sides_distortion_label = menu_label(self.menu_background, "sides\ndistortion", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 40, cube_graphics_menu_cors[1] + 110).label
        self.sides_distortion_label2 = menu_label(self.menu_background, ":", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 110).label
        self.sides_distortion_button = menu_button(self.menu_background, self.sides_distortion, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + 110, self.change_game_settings).button
        self.borders_width_label = menu_label(self.menu_background, "borders\nwidth", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 40, cube_graphics_menu_cors[1] + 180).label
        self.borders_width_label2 = menu_label(self.menu_background, ":", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 180).label
        self.borders_width_button = menu_button(self.menu_background, self.borders_width, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + 180, self.change_game_settings).button

        self.bindings_are_activated = True
        self.root.bind('<Left>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<Right>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<Up>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<Down>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<x>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<X>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<y>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<Y>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<z>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<Z>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<r>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<R>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<l>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<L>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<u>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<U>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<d>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<D>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<f>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<F>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<b>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<B>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<m>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<M>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<e>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<E>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<s>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))
        self.root.bind('<S>', lambda event: self.make_move_graphic(event, self.rubiks_cube, []))

    def left(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[0][i][0] = [cube[1][x][2] for x in [2, 1, 0]][i]
            cube2[1][i][2] = [cube[5][x][0] for x in [2, 1, 0]][i]
            cube2[3][i][0] = [cube[0][x][0] for x in [0, 1, 2]][i]
            cube2[5][i][0] = [cube[3][x][0] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[2][i][j] = [[cube[2][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def right(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[3][i][2] = [cube[5][x][2] for x in [0, 1, 2]][i]
            cube2[5][i][2] = [cube[1][x][0] for x in [2, 1, 0]][i]
            cube2[0][i][2] = [cube[3][x][2] for x in [0, 1, 2]][i]
            cube2[1][i][0] = [cube[0][x][2] for x in [2, 1, 0]][i]
            for j in range(3):
                cube2[4][i][j] = [[cube[4][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def up(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[0][2][i] = [cube[2][x][2] for x in [2, 1, 0]][i]
            cube2[2][i][2] = [cube[5][0][x] for x in [0, 1, 2]][i]
            cube2[4][i][0] = [cube[0][2][x] for x in [0, 1, 2]][i]
            cube2[5][0][i] = [cube[4][x][0] for x in [2, 1, 0]][i]
            for j in range(3):
                cube2[3][i][j] = [[cube[3][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def down(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[0][0][i] = [cube[4][x][2] for x in [0, 1, 2]][i]
            cube2[2][i][0] = [cube[0][0][x] for x in [2, 1, 0]][i]
            cube2[4][i][2] = [cube[5][2][x] for x in [2, 1, 0]][i]
            cube2[5][2][i] = [cube[2][x][0] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[1][i][j] = [[cube[1][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def front(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[1][2][i] = [cube[4][2][x] for x in [0, 1, 2]][i]
            cube2[2][2][i] = [cube[1][2][x] for x in [0, 1, 2]][i]
            cube2[3][2][i] = [cube[2][2][x] for x in [0, 1, 2]][i]
            cube2[4][2][i] = [cube[3][2][x] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[5][i][j] = [[cube[5][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def back(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[1][0][i] = [cube[2][0][x] for x in [0, 1, 2]][i]
            cube2[2][0][i] = [cube[3][0][x] for x in [0, 1, 2]][i]
            cube2[3][0][i] = [cube[4][0][x] for x in [0, 1, 2]][i]
            cube2[4][0][i] = [cube[1][0][x] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[0][i][j] = [[cube[0][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def midM(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[0][i][1] = [cube[1][x][1] for x in [2, 1, 0]][i]
            cube2[1][i][1] = [cube[5][x][1] for x in [2, 1, 0]][i]
            cube2[3][i][1] = [cube[0][x][1] for x in [0, 1, 2]][i]
            cube2[5][i][1] = [cube[3][x][1] for x in [0, 1, 2]][i]
        return cube2
    def midE(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[0][1][i] = [cube[4][x][1] for x in [0, 1, 2]][i]
            cube2[2][i][1] = [cube[0][1][x] for x in [2, 1, 0]][i]
            cube2[4][i][1] = [cube[5][1][x] for x in [2, 1, 0]][i]
            cube2[5][1][i] = [cube[2][x][1] for x in [0, 1, 2]][i]
        return cube2
    def midS(self, cube):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for i in range(3):
            cube2[1][1][i] = [cube[4][1][x] for x in [0, 1, 2]][i]
            cube2[2][1][i] = [cube[1][1][x] for x in [0, 1, 2]][i]
            cube2[3][1][i] = [cube[2][1][x] for x in [0, 1, 2]][i]
            cube2[4][1][i] = [cube[3][1][x] for x in [0, 1, 2]][i]
        return cube2
    def rotx(self, cube):
        cube2 = self.right(cube)
        for i in range(3):
            cube2 = self.left(cube2)
            cube2 = self.midM(cube2)
        return cube2
    def roty(self, cube):
        cube2 = self.up(cube)
        for i in range(3):
            cube2 = self.down(cube2)
            cube2 = self.midE(cube2)
        return cube2
    def rotz(self, cube):
        cube2 = self.front(cube)
        cube2 = self.midS(cube2)
        for i in range(3):
            cube2 = self.back(cube2)
        return cube2
    def make_moves_sequence(self, cube, moves_seq):
        cube2 = [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
        for move in moves_seq:
            if move == "L":
                cube2 = self.left(cube2)
            elif move == "L'":
                for i in range(3):
                    cube2 = self.left(cube2)
            elif move == "R":
                cube2 = self.right(cube2)
            elif move == "R'":
                for i in range(3):
                    cube2 = self.right(cube2)
            elif move == "U":
                cube2 = self.up(cube2)
            elif move == "U'":
                for i in range(3):
                    cube2 = self.up(cube2)
            elif move == "D":
                cube2 = self.down(cube2)
            elif move == "D'":
                for i in range(3):
                    cube2 = self.down(cube2)
            elif move == "F":
                cube2 = self.front(cube2)
            elif move == "F'":
                for i in range(3):
                    cube2 = self.front(cube2)
            elif move == "B":
                cube2 = self.back(cube2)
            elif move == "B'":
                for i in range(3):
                    cube2 = self.back(cube2)
            elif move == "M":
                cube2 = self.midM(cube2)
            elif move == "M'":
                for i in range(3):
                    cube2 = self.midM(cube2)
            elif move == "E":
                cube2 = self.midE(cube2)
            elif move == "E'":
                for i in range(3):
                    cube2 = self.midE(cube2)
            elif move == "S":
                cube2 = self.midS(cube2)
            elif move == "S'":
                for i in range(3):
                    cube2 = self.midS(cube2)
            elif move == "x":
                cube2 = self.rotx(cube2)
            elif move == "x'":
                for i in range(3):
                    cube2 = self.rotx(cube2)
            elif move == "y":
                cube2 = self.roty(cube2)
            elif move == "y'":
                for i in range(3):
                    cube2 = self.roty(cube2)
            elif move == "z":
                cube2 = self.rotz(cube2)
            elif move == "z'":
                for i in range(3):
                    cube2 = self.rotz(cube2)
            elif move == "":
                pass
        return cube2
    def print_rubiks_cube(self, cube):
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

    def reset_cube(self):
        self.rubiks_cube = [[[["b", "y", "o", "w", "r", "g"][x] for z in range(3)] for y in range(3)] for x in range(6)]
        self.play_background.delete("all")
        self.make_move_graphic(None, self.rubiks_cube, [])
    def reset_cube_event(self, event):
        if self.bindings_are_activated: self.reset_cube()
    def scramble_cube(self, cube, moves_number):
        self.moves_seq = []
        # moves_matrix = ["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'", "x", "x'", "y", "y'", "z", "z'"]
        moves_matrix = ["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'"]
        for i in range(moves_number):
            self.moves_seq.append(random.choice(moves_matrix))
        self.play_background.delete("all")
        self.moves_seq_text = self.play_background.create_text(float(self.play_background["width"]) / 2, 30, fill = "darkblue", text = self.moves_seq, font = "Times 20 italic bold")
        self.make_move_graphic(None, cube, [""] + self.moves_seq)
    def scramble_cube_event(self, event):
        if self.bindings_are_activated:
            self.scramble_cube(self.rubiks_cube, self.scramble_moves)
    def change_game_settings(self, event):
        if event.widget == self.moves_speed_button:
            self.moves_speed = self.alternate_matrix_elements(self.moves_speeds_matrix, self.moves_speed)
            self.moves_speed_button.configure(text = self.moves_speed)
        elif event.widget == self.moves_number_button:
            self.scramble_moves = self.alternate_matrix_elements(self.scramble_moves_matrix, self.scramble_moves)
            self.moves_number_button.configure(text = self.scramble_moves)
        elif event.widget == self.cube_size_button:
            self.square_side_length = self.alternate_matrix_elements(self.square_side_lengths_matrix, self.square_side_length)
            self.cube_size_button.configure(text = self.square_side_length)
        elif event.widget == self.sides_distortion_button:
            self.sides_distortion = self.alternate_matrix_elements(self.sides_distortions_matrix, self.sides_distortion)
            self.sides_distortion_button.configure(text = self.sides_distortion)
        elif event.widget == self.borders_width_button:
            self.borders_width = self.alternate_matrix_elements(self.borders_widths_matrix, self.borders_width)
            self.borders_width_button.configure(text = self.borders_width)
        centre_offset =  3 / 2 * self.sides_distortion * self.square_side_length
        self.front_cube_side_centre_point = [float(self.cube_background["width"]) / 2 - centre_offset / math.sqrt(2), float(self.cube_background["height"]) / 2 + centre_offset / math.sqrt(2)]
        self.make_move_graphic(None, self.rubiks_cube, [])
    def alternate_matrix_elements(self, matrix, index_element):
        return (matrix[1:] + [matrix[0]])[matrix.index(index_element)]

    def draw_cube_side(self, background, cube_face_oriented, borders_width, piece_left_side_length, piece_down_side_length, piece_left_side_angle, piece_down_side_angle, cube_face_down_left_point):
        cf = cube_face_oriented; cfdl = cube_face_down_left_point; ps1 = piece_left_side_length; ps2 = piece_down_side_length; pa1 = math.radians(piece_left_side_angle); pa2 = math.radians(piece_down_side_angle)
        cf_colors = [[["blue", "yellow", "orange", "white", "red", "green"][["b", "y", "o", "w", "r", "g"].index(cf[i][j])] for j in range(3)] for i in range(3)]
        cfdl2 = cfdl; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][0], width = borders_width, outline = "black", tags = "down_left_piece")
        cfdl2 = [cfdl[0] + ps2 * math.cos(pa2), cfdl[1] - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][1], width = borders_width, outline = "black", tags = "down_middle_piece")
        cfdl2 = [cfdl[0] + 2 * ps2 * math.cos(pa2), cfdl[1] - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][2], width = borders_width, outline = "black", tags = "down_right_piece")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1), cfdl[1] - ps1 * math.sin(pa1)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][0], width = borders_width, outline = "black", tags = "left_middle_piece")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1) + ps2 * math.cos(pa2), cfdl[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][1], width = borders_width, outline = "black", tags = "centre_piece")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), cfdl[1] - ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][2], width = borders_width, outline = "black", tags = "right_middle_piece")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1), cfdl[1] - 2 * ps1 * math.sin(pa1)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][0], width = borders_width, outline = "black", tags = "up_left_piece")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1) + ps2 * math.cos(pa2), cfdl[1] - 2 * ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][1], width = borders_width, outline = "black", tags = "up_middle_piece")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), cfdl[1] - 2 * ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][2], width = borders_width, outline = "black", tags = "up_right_piece")
    def make_move_graphic(self, event, cube, moves_seq):
        if event == None:
            self.cube_background.delete("all")
            self.bindings_are_activated = False
            if moves_seq == []:
                # in order: front_cube_side, up_cube_side, right_cube_side
                self.draw_cube_side(self.cube_background, self.rubiks_cube[5], self.borders_width, self.square_side_length, self.square_side_length, 90, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
                self.draw_cube_side(self.cube_background, self.rubiks_cube[3], self.borders_width, self.square_side_length * self.sides_distortion, self.square_side_length, 45, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] - 3 * self.square_side_length / 2])
                self.draw_cube_side(self.cube_background, [[self.rubiks_cube[4][2-j][i] for j in range(3)] for i in range(3)], self.borders_width, self.square_side_length, self.square_side_length * self.sides_distortion, 90, 45, [self.front_cube_side_centre_point[0] + 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
                self.bindings_are_activated = True
            else:
                move = []
                move.append(moves_seq[0])
                self.rubiks_cube = self.make_moves_sequence(cube, move)
                self.draw_cube_side(self.cube_background, self.rubiks_cube[5], self.borders_width, self.square_side_length, self.square_side_length, 90, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
                self.draw_cube_side(self.cube_background, self.rubiks_cube[3], self.borders_width, self.square_side_length * self.sides_distortion, self.square_side_length, 45, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] - 3 * self.square_side_length / 2])
                self.draw_cube_side(self.cube_background, [[self.rubiks_cube[4][2-j][i] for j in range(3)] for i in range(3)], self.borders_width, self.square_side_length, self.square_side_length * self.sides_distortion, 90, 45, [self.front_cube_side_centre_point[0] + 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
                self.cube_background.after(int(1000 * self.moves_speed), lambda: self.make_move_graphic(None, self.rubiks_cube, moves_seq[1:]))
        elif event != None and self.bindings_are_activated:
            self.cube_background.delete("all")
            if event.keysym == "Left":
                self.rubiks_cube = self.make_moves_sequence(cube, ["y"])
            elif event.keysym == "Right":
                self.rubiks_cube = self.make_moves_sequence(cube, ["y'"])
            elif event.keysym == "Up":
                self.rubiks_cube = self.make_moves_sequence(cube, ["x"])
            elif event.keysym == "Down":
                self.rubiks_cube = self.make_moves_sequence(cube, ["x'"])
            elif event.keysym == "x":
                self.rubiks_cube = self.make_moves_sequence(cube, ["x"])
            elif event.keysym == "X":
                self.rubiks_cube = self.make_moves_sequence(cube, ["x'"])
            elif event.keysym == "y":
                self.rubiks_cube = self.make_moves_sequence(cube, ["y"])
            elif event.keysym == "Y":
                self.rubiks_cube = self.make_moves_sequence(cube, ["y'"])
            elif event.keysym == "z":
                self.rubiks_cube = self.make_moves_sequence(cube, ["z"])
            elif event.keysym == "Z":
                self.rubiks_cube = self.make_moves_sequence(cube, ["z'"])
            elif event.keysym == "r":
                self.rubiks_cube = self.make_moves_sequence(cube, ["R"])
            elif event.keysym == "R":
                self.rubiks_cube = self.make_moves_sequence(cube, ["R'"])
            elif event.keysym == "l":
                self.rubiks_cube = self.make_moves_sequence(cube, ["L"])
            elif event.keysym == "L":
                self.rubiks_cube = self.make_moves_sequence(cube, ["L'"])
            elif event.keysym == "u":
                self.rubiks_cube = self.make_moves_sequence(cube, ["U"])
            elif event.keysym == "U":
                self.rubiks_cube = self.make_moves_sequence(cube, ["U'"])
            elif event.keysym == "d":
                self.rubiks_cube = self.make_moves_sequence(cube, ["D"])
            elif event.keysym == "D":
                self.rubiks_cube = self.make_moves_sequence(cube, ["D'"])
            elif event.keysym == "f":
                self.rubiks_cube = self.make_moves_sequence(cube, ["F"])
            elif event.keysym == "F":
                self.rubiks_cube = self.make_moves_sequence(cube, ["F'"])
            elif event.keysym == "b":
                self.rubiks_cube = self.make_moves_sequence(cube, ["B"])
            elif event.keysym == "B":
                self.rubiks_cube = self.make_moves_sequence(cube, ["B'"])
            elif event.keysym == "m":
                self.rubiks_cube = self.make_moves_sequence(cube, ["M"])
            elif event.keysym == "M":
                self.rubiks_cube = self.make_moves_sequence(cube, ["M'"])
            elif event.keysym == "e":
                self.rubiks_cube = self.make_moves_sequence(cube, ["E"])
            elif event.keysym == "E":
                self.rubiks_cube = self.make_moves_sequence(cube, ["E'"])
            elif event.keysym == "s":
                self.rubiks_cube = self.make_moves_sequence(cube, ["S"])
            elif event.keysym == "S":
                self.rubiks_cube = self.make_moves_sequence(cube, ["S'"])
            self.draw_cube_side(self.cube_background, self.rubiks_cube[5], self.borders_width, self.square_side_length, self.square_side_length, 90, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
            self.draw_cube_side(self.cube_background, self.rubiks_cube[3], self.borders_width, self.square_side_length * self.sides_distortion, self.square_side_length, 45, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] - 3 * self.square_side_length / 2])
            self.draw_cube_side(self.cube_background, [[self.rubiks_cube[4][2-j][i] for j in range(3)] for i in range(3)], self.borders_width, self.square_side_length, self.square_side_length * self.sides_distortion, 90, 45, [self.front_cube_side_centre_point[0] + 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])

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

root = tk.Tk()
rubiks_cube_root = rubiks_cube(root)
root.mainloop()