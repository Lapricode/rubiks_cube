import tkinter as tk
import math
import random
import os
from PIL import Image, ImageTk

class rubiks_cube():
    def __init__(self, root):
        self.root = root
        self.root.geometry("+0+0")
        self.root.title("Rubik's cube")
        self.root.iconbitmap(os.getcwd() + "/rubiks_cube_icon.ico")
        self.cube_background_width = (2 / 3) * self.root.winfo_screenwidth()
        self.cube_background_height = (5 / 8) * self.cube_background_width
        self.down_area_background_width = self.cube_background_width
        self.down_area_background_height = self.cube_background_height / 5
        self.menu_background_width = self.cube_background_width / 3
        self.menu_background_height = self.cube_background_height + self.down_area_background_height
        self.menu_background = tk.Frame(root, width = self.menu_background_width, height = self.menu_background_height, bg = "black", bd = 0, relief = "solid")
        self.menu_background.grid(row = 0, column = 0, rowspan = 2, sticky = tk.NSEW)
        self.cube_background = tk.Canvas(root, width = self.cube_background_width, height = self.cube_background_height, bg = "cyan", bd = 0, relief = "solid")
        self.cube_background.grid(row = 0, column = 1, sticky = tk.NSEW)
        self.down_area_background = tk.Canvas(root, width = self.down_area_background_width, height = self.down_area_background_height, bg = "yellow", bd = 0, relief = "solid")
        self.down_area_background.grid(row = 1, column = 1, sticky = tk.NSEW)
        
        # variables for visible cube
        self.square_side_length = 100
        self.square_side_lengths_matrix = [25, 50, 75, 100]
        self.borders_width = 5
        self.borders_widths_matrix = [0, 2, 5, 10]
        self.sides_distortion = 0.6
        self.sides_distortions_matrix = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        centre_offset =  3 / 2 * self.sides_distortion * self.square_side_length
        self.front_cube_side_centre_point = [self.cube_background_width / 2 - centre_offset / math.sqrt(2), self.cube_background_height / 2 + centre_offset / math.sqrt(2)]
        self.activefill_pieces_color = "black"
        self.hidden_sides_visibility = "off"
        self.axis_visibility = "off"
        
        # variables for hidden sides
        self.hidden_centre_xcor = 60
        self.hidden_centre_ycor = 80
        self.hidden_side_length = 20
        
        # variables for scramble
        self.moves_speed = 0.0
        self.moves_speeds_matrix = [0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
        self.scramble_moves = 10
        self.scramble_moves_matrix = [1, 3, 5, 10, 20, 30]
        
        # variables for instructions
        self.instructions_text = "In the picture above you can see the official cube notation that I am using in this\n\
program. Typing in your keyboard one of these letter-keys you can execute the\n\
corresponding move on the cube. Additionally, if you type a letter-key holding\n\
shift-key, you can execute the move in the opposite direction. The notation for\n\
the opposite direction moves uses the same letters but with an apostrophe next\n\
to them. For example, R' (R prime) means R move but in the opposite direction."

        self.reset_cube()

        self.reset_button = menu_button(self.menu_background, "reset", "Arial 25 bold", "white", "black", self.menu_background_width / 2 - 50, 40, self.reset_cube_event).button
        self.show_instructions_button = menu_button(self.menu_background, "info", "Arial 25 bold", "white", "black", self.menu_background_width / 2 + 50, 40, self.show_instructions).button
        
        # scramble cube menu
        scramble_cube_menu_cors = [self.menu_background_width / 2, 120]
        self.scramble_cube_menu_label = menu_label(self.menu_background, "Scramble cube:", "Times 30 bold", "yellow", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1]).label
        self.moves_speed_label = menu_label(self.menu_background, "moves speed (sec):", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 25, scramble_cube_menu_cors[1] + 60).label
        self.moves_speed_button = menu_button(self.menu_background, self.moves_speed, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 120, scramble_cube_menu_cors[1] + 60, self.change_game_settings).button
        self.moves_number_label = menu_label(self.menu_background, "moves number:", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 25, scramble_cube_menu_cors[1] + 100).label
        self.moves_number_button = menu_button(self.menu_background, self.scramble_moves, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 95, scramble_cube_menu_cors[1] + 100, self.change_game_settings).button
        self.scramble_button = menu_button(self.menu_background, "scramble", "Arial 25 bold", "white", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1] + 140, self.scramble_cube_event).button

        # cube graphics menu
        cube_graphics_menu_cors = [self.menu_background_width / 2, 340]
        self.cube_graphics_menu_label = menu_label(self.menu_background, "Cube graphics:", "Times 30 bold", "yellow", "black", cube_graphics_menu_cors[0], cube_graphics_menu_cors[1]).label
        self.cube_size_label = menu_label(self.menu_background, "cube size:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 30, cube_graphics_menu_cors[1] + 60).label
        self.cube_size_button = menu_button(self.menu_background, self.square_side_length, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 65, cube_graphics_menu_cors[1] + 60, self.change_game_settings).button
        self.sides_distortion_label = menu_label(self.menu_background, "sides distortion:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 30, cube_graphics_menu_cors[1] + 100).label
        self.sides_distortion_button = menu_button(self.menu_background, self.sides_distortion, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 100, cube_graphics_menu_cors[1] + 100, self.change_game_settings).button
        self.borders_width_label = menu_label(self.menu_background, "borders width:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 20, cube_graphics_menu_cors[1] + 140).label
        self.borders_width_button = menu_button(self.menu_background, self.borders_width, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 90, cube_graphics_menu_cors[1] + 140, self.change_game_settings).button
        self.hidden_sides_visibility_label = menu_label(self.menu_background, "hidden sides:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 30, cube_graphics_menu_cors[1] + 180).label
        self.hidden_sides_visibility_button = menu_button(self.menu_background, self.hidden_sides_visibility, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 85, cube_graphics_menu_cors[1] + 180, self.change_game_settings).button
        self.axis_visibility_label = menu_label(self.menu_background, "axis:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 20, cube_graphics_menu_cors[1] + 220).label
        self.axis_visibility_button = menu_button(self.menu_background, self.axis_visibility, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 40, cube_graphics_menu_cors[1] + 220, self.change_game_settings).button

        # bindings
        self.bindings_are_activated = True
        self.root.bind('<Left>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<Right>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<Up>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<Down>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<x>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<X>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<y>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<Y>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<z>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<Z>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<r>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<R>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<l>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<L>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<u>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<U>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<d>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<D>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<f>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<F>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<b>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<B>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<m>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<M>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<e>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<E>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<s>', lambda event: self.make_moves_sequence([], event))
        self.root.bind('<S>', lambda event: self.make_moves_sequence([], event))

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
    def make_moves_sequence(self, moves_seq, event = None):
        if moves_seq == []:
            move = ""
        else:
            move = moves_seq[0]
        if (event == None and move == "L") or (event != None and event.keysym == "l" and self.bindings_are_activated):
            self.rubiks_cube = self.left(self.rubiks_cube)
        elif (event == None and move == "L'") or (event != None and event.keysym == "L" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.left(self.rubiks_cube)
        elif (event == None and move == "R") or (event != None and event.keysym == "r" and self.bindings_are_activated):
            self.rubiks_cube = self.right(self.rubiks_cube)
        elif (event == None and move == "R'") or (event != None and event.keysym == "R" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.right(self.rubiks_cube)
        elif (event == None and move == "U") or (event != None and event.keysym == "u" and self.bindings_are_activated):
            self.rubiks_cube = self.up(self.rubiks_cube)
        elif (event == None and move == "U'") or (event != None and event.keysym == "U" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.up(self.rubiks_cube)
        elif (event == None and move == "D") or (event != None and event.keysym == "d" and self.bindings_are_activated):
            self.rubiks_cube = self.down(self.rubiks_cube)
        elif (event == None and move == "D'") or (event != None and event.keysym == "D" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.down(self.rubiks_cube)
        elif (event == None and move == "F") or (event != None and event.keysym == "f" and self.bindings_are_activated):
            self.rubiks_cube = self.front(self.rubiks_cube)
        elif (event == None and move == "F'") or (event != None and event.keysym == "F" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.front(self.rubiks_cube)
        elif (event == None and move == "B") or (event != None and event.keysym == "b" and self.bindings_are_activated):
            self.rubiks_cube = self.back(self.rubiks_cube)
        elif (event == None and move == "B'") or (event != None and event.keysym == "B" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.back(self.rubiks_cube)
        elif (event == None and move == "M") or (event != None and event.keysym == "m" and self.bindings_are_activated):
            self.rubiks_cube = self.midM(self.rubiks_cube)
        elif (event == None and move == "M'") or (event != None and event.keysym == "M" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.midM(self.rubiks_cube)
        elif (event == None and move == "E") or (event != None and event.keysym == "e" and self.bindings_are_activated):
            self.rubiks_cube = self.midE(self.rubiks_cube)
        elif (event == None and move == "E'") or (event != None and event.keysym == "E" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.midE(self.rubiks_cube)
        elif (event == None and move == "S") or (event != None and event.keysym == "s" and self.bindings_are_activated):
            self.rubiks_cube = self.midS(self.rubiks_cube)
        elif (event == None and move == "S'") or (event != None and event.keysym == "S" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.midS(self.rubiks_cube)
        elif (event == None and move == "x") or (event != None and (event.keysym == "x" or event.keysym == "Up") and self.bindings_are_activated):
            self.rubiks_cube = self.rotx(self.rubiks_cube)
        elif (event == None and move == "x'") or (event != None and (event.keysym == "X" or event.keysym == "Down") and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.rotx(self.rubiks_cube)
        elif (event == None and move == "y") or (event != None and (event.keysym == "y" or event.keysym == "Left") and self.bindings_are_activated):
            self.rubiks_cube = self.roty(self.rubiks_cube)
        elif (event == None and move == "y'") or (event != None and (event.keysym == "Y" or event.keysym == "Right") and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.roty(self.rubiks_cube)
        elif (event == None and move == "z") or (event != None and event.keysym == "z" and self.bindings_are_activated):
            self.rubiks_cube = self.rotz(self.rubiks_cube)
        elif (event == None and move == "z'") or (event != None and event.keysym == "Z" and self.bindings_are_activated):
            for i in range(3):
                self.rubiks_cube = self.rotz(self.rubiks_cube)
        elif event == None and move == "":
            pass
        if event == None:
            self.bindings_are_activated = False
            self.make_move_graphic()
            if moves_seq != []:
                self.cube_background.after(int(1000 * self.moves_speed), lambda: self.make_moves_sequence(moves_seq[1:]))
            else:
                self.bindings_are_activated = True
        if self.bindings_are_activated:
            self.make_move_graphic()
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
        self.down_area_background.delete("all")
        self.make_moves_sequence([])
    def reset_cube_event(self, event):
        if self.bindings_are_activated:
            self.reset_cube()
    def scramble_cube(self, moves_number):
        self.moves_seq = []
        # moves_matrix = ["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'", "x", "x'", "y", "y'", "z", "z'"]
        moves_matrix = ["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'"]
        for i in range(moves_number):
            self.moves_seq.append(random.choice(moves_matrix))
        self.down_area_background.delete("all")
        self.moves_seq_text = self.down_area_background.create_text(self.down_area_background_width / 2, 30, fill = "darkblue", text = self.moves_seq, font = "Times 20 italic bold")
        self.make_moves_sequence(self.moves_seq)
    def scramble_cube_event(self, event):
        if self.bindings_are_activated:
            self.scramble_cube(self.scramble_moves)
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
        elif event.widget == self.hidden_sides_visibility_button:
            self.hidden_sides_visibility = self.alternate_matrix_elements(["on", "off"], self.hidden_sides_visibility)
            self.hidden_sides_visibility_button.configure(text = self.hidden_sides_visibility)
        elif event.widget == self.axis_visibility_button:
            self.axis_visibility = self.alternate_matrix_elements(["on", "off"], self.axis_visibility)
            self.axis_visibility_button.configure(text = self.axis_visibility)
        centre_offset =  3 / 2 * self.sides_distortion * self.square_side_length
        self.front_cube_side_centre_point = [float(self.cube_background["width"]) / 2 - centre_offset / math.sqrt(2), float(self.cube_background["height"]) / 2 + centre_offset / math.sqrt(2)]
        self.make_move_graphic()
    def show_instructions(self, event = None):
        try:
            self.instructions_background.destroy()
        except AttributeError:
            pass
        self.instructions_background = tk.Canvas(self.root, width = self.cube_background_width, height = self.cube_background_height + self.down_area_background_height, bg = "yellow")
        self.instructions_background.grid(row = 0, column = 1, rowspan = 2, sticky = tk.NSEW)
        self.instructions_background.create_text(self.cube_background_width / 2, 40, text = "Instructions", font = "Arial 30 bold italic", fill = "darkblue")
        self.cube_notation_picture = Image.open(os.getcwd() + "/rubiks_cube_notation.jpg")
        reduction_factor = 3 / 4
        self.cube_notation_picture = self.cube_notation_picture.resize((int(reduction_factor * self.cube_background_width), int(reduction_factor * self.cube_background_width * self.cube_notation_picture.height / self.cube_notation_picture.width)), Image.ANTIALIAS)
        self.cube_notation_picture = ImageTk.PhotoImage(self.cube_notation_picture)
        self.instructions_background.create_image(self.cube_background_width / 2, self.cube_notation_picture.height() / 2 + 80, image = self.cube_notation_picture)
        self.instructions_background.create_text(self.cube_background_width / 2, self.cube_notation_picture.height() + 200, text = self.instructions_text, font = "Calibri 20 bold", fill = "darkblue")
        self.back_button = menu_button(self.instructions_background, "back", "Calibri 25 bold", "black", "yellow", self.cube_background_width / 2, self.cube_background_height + self.down_area_background_height - 60, self.hide_instructions).button
    def hide_instructions(self, event):
        self.instructions_background.destroy()
    def alternate_matrix_elements(self, matrix, index_element):
        return (matrix[1:] + [matrix[0]])[matrix.index(index_element)]
        
    def draw_cube_side(self, background, cube_face_oriented, borders_width, piece_left_side_length, piece_down_side_length, piece_left_side_angle, piece_down_side_angle, cube_face_down_left_point):
        cf = cube_face_oriented; cfdl = cube_face_down_left_point; ps1 = piece_left_side_length; ps2 = piece_down_side_length; pa1 = math.radians(piece_left_side_angle); pa2 = math.radians(piece_down_side_angle)
        cf_colors = [[["blue", "yellow", "orange", "white", "red", "green"][["b", "y", "o", "w", "r", "g"].index(cf[i][j])] for j in range(3)] for i in range(3)]
        cfdl2 = cfdl; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][0], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "down_left_piece")
        cfdl2 = [cfdl[0] + ps2 * math.cos(pa2), cfdl[1] - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][1], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "down_middle_piece")
        cfdl2 = [cfdl[0] + 2 * ps2 * math.cos(pa2), cfdl[1] - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][2], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "down_right_piece")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1), cfdl[1] - ps1 * math.sin(pa1)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][0], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "left_middle_piece")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1) + ps2 * math.cos(pa2), cfdl[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][1], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "centre_piece")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), cfdl[1] - ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][2], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "right_middle_piece")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1), cfdl[1] - 2 * ps1 * math.sin(pa1)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][0], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "up_left_piece")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1) + ps2 * math.cos(pa2), cfdl[1] - 2 * ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][1], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "up_middle_piece")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), cfdl[1] - 2 * ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][2], activefill = self.activefill_pieces_color, width = borders_width, outline = "black", tags = "up_right_piece")
    def make_move_graphic(self, event = None):
        self.cube_background.delete("all")
        # for visible_cube
        self.draw_cube_side(self.cube_background, self.rubiks_cube[5], self.borders_width, self.square_side_length, self.square_side_length, 90, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
        self.draw_cube_side(self.cube_background, self.rubiks_cube[3], self.borders_width, self.square_side_length * self.sides_distortion, self.square_side_length, 45, 0, [self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] - 3 * self.square_side_length / 2])
        self.draw_cube_side(self.cube_background, [[self.rubiks_cube[4][2-j][i] for j in range(3)] for i in range(3)], self.borders_width, self.square_side_length, self.square_side_length * self.sides_distortion, 90, 45, [self.front_cube_side_centre_point[0] + 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2])
        if self.axis_visibility == "on":
            self.cube_background.create_line(self.front_cube_side_centre_point[0] - 3 * self.square_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre_point[1] - 3 * self.square_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre_point[0] - 3 * self.square_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre_point[1] - 3 * self.square_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) - 50, width = 5, fill = "black", activefill = "white")
            self.cube_background.create_text(self.front_cube_side_centre_point[0] - 3 * self.square_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)) - 10, self.front_cube_side_centre_point[1] - 3 * self.square_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) - 50, text = "z", font = "Times 20 bold", fill = "black", activefill = "purple")
            self.cube_background.create_line(self.front_cube_side_centre_point[0] + 3 * self.square_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre_point[1] + 3 * self.square_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre_point[0] + 3 * self.square_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) + 50, self.front_cube_side_centre_point[1] + 3 * self.square_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), width = 5, fill = "black", activefill = "white")
            self.cube_background.create_text(self.front_cube_side_centre_point[0] + 3 * self.square_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) + 60, self.front_cube_side_centre_point[1] + 3 * self.square_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)) - 5, text = "y", font = "Times 20 bold", fill = "black", activefill = "purple")
            self.cube_background.create_line(self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2, self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2, self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2 - 50 / math.sqrt(2), self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2 + 50 / math.sqrt(2), width = 5, fill = "black", activefill = "white")
            self.cube_background.create_text(self.front_cube_side_centre_point[0] - 3 * self.square_side_length / 2 - 50 / math.sqrt(2), self.front_cube_side_centre_point[1] + 3 * self.square_side_length / 2 + 50 / math.sqrt(2) + 10, text = "x", font = "Times 20 bold", fill = "black", activefill = "purple")
        # for hidden_layers
        if self.hidden_sides_visibility == "on":
            self.draw_cube_side(self.cube_background, [[self.rubiks_cube[0][2-i][j] for j in range(3)] for i in range(3)], 0, self.hidden_side_length, self.hidden_side_length, 90, 0, [self.hidden_centre_xcor, self.hidden_centre_ycor])
            self.draw_cube_side(self.cube_background, [[self.rubiks_cube[2][2-j][2-i] for j in range(3)] for i in range(3)], 0, self.hidden_side_length, self.hidden_side_length * self.sides_distortion, 90, 45, [self.hidden_centre_xcor - 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2), self.hidden_centre_ycor + 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2)])
            self.draw_cube_side(self.cube_background, [[self.rubiks_cube[1][i][2-j] for j in range(3)] for i in range(3)], 0, self.hidden_side_length * self.sides_distortion, self.hidden_side_length, 45, 0, [self.hidden_centre_xcor - 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2), self.hidden_centre_ycor + 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2)])
        if self.hidden_sides_visibility == "on" and self.axis_visibility == "on":
            self.cube_background.create_line(self.hidden_centre_xcor, self.hidden_centre_ycor, self.hidden_centre_xcor, self.hidden_centre_ycor - 3 * self.hidden_side_length - 10, width = 3, fill = "black", activefill = "white")
            self.cube_background.create_text(self.hidden_centre_xcor - 10, self.hidden_centre_ycor - 3 * self.hidden_side_length - 10, text = "z", font = "Times 15 bold", fill = "black", activefill = "purple")
            self.cube_background.create_line(self.hidden_centre_xcor, self.hidden_centre_ycor, self.hidden_centre_xcor + 3 * self.hidden_side_length + 10, self.hidden_centre_ycor, width = 3, fill = "black", activefill = "white")
            self.cube_background.create_text(self.hidden_centre_xcor + 3 * self.hidden_side_length + 20, self.hidden_centre_ycor - 5, text = "y", font = "Times 15 bold", fill = "black", activefill = "purple")
            self.cube_background.create_line(self.hidden_centre_xcor, self.hidden_centre_ycor, self.hidden_centre_xcor - (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2), self.hidden_centre_ycor + (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2), width = 3, fill = "black", activefill = "white")
            self.cube_background.create_text(self.hidden_centre_xcor - (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2), self.hidden_centre_ycor + (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2) + 10, text = "x", font = "Times 15 bold", fill = "black", activefill = "purple")
            self.cube_background.create_line(self.hidden_centre_xcor, self.hidden_centre_ycor, self.hidden_centre_xcor, self.hidden_centre_ycor, width = 5, fill = "black", capstyle = "round", activefill = "white")

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