import tkinter as tk
import math
import random
import os
import time
import pygame
from PIL import Image, ImageTk
from rubik_solver import utils

class rubiks_cube():
    def __init__(self, root):
        pygame.init()
        self.root = root
        self.root.geometry("+0+0")
        self.root.title("Rubik's cube")
        self.root.iconbitmap(os.getcwd() + "/rubiks_cube_icon.ico")
        self.cube_background_width = (2 / 3) * self.root.winfo_screenwidth()
        self.cube_background_height = (3 / 4) * self.root.winfo_screenheight() - 50
        self.down_area_background_width = self.cube_background_width
        self.down_area_background_height = self.cube_background_height / 5 + 50
        self.menu_background_width = self.cube_background_width / 3
        self.menu_background_height = self.cube_background_height + self.down_area_background_height
        self.menu_background = tk.Frame(self.root, width = self.menu_background_width, height = self.menu_background_height, bg = "black", bd = 0, relief = "solid")
        self.menu_background.grid(row = 0, column = 0, rowspan = 2, sticky = tk.NSEW)
        self.cube_background = tk.Canvas(self.root, width = self.cube_background_width, height = self.cube_background_height, bg = "cyan", bd = 0, relief = "solid")
        self.cube_background.grid(row = 0, column = 1, sticky = tk.NSEW)
        self.down_area_background = tk.Canvas(self.root, width = self.down_area_background_width, height = self.down_area_background_height, bg = "yellow", bd = 0, relief = "solid")
        self.down_area_background.grid(row = 1, column = 1, sticky = tk.NSEW)
        
        # variables for visible cube
        self.cube_colors = ["blue", "yellow", "orange", "white", "red", "green"]
        self.cube_dimensions = "3d"
        self.cube_dimensions_matrix = ["2d", "3d"]
        self.piece_side_length = 100
        self.borders_width = 1
        self.borders_widths_matrix = [0, 1, 2, 3]
        self.sides_distortion = 0.6
        self.sides_distortions_matrix = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        self.hidden_sides_visibility = "on"
        self.axis_visibility = "on"
        self.scramble_pattern_visibility = "on"
        self.scrambled_pattern_centre_x = self.cube_background_width - 100
        self.scrambled_pattern_centre_y = 80
        self.visible_cube_centre_x = self.cube_background_width / 2
        self.visible_cube_centre_y = self.cube_background_height / 2

        # variables for hidden sides
        self.hidden_cube_centre_x = 60
        self.hidden_cube_centre_y = 80
        self.hidden_side_length = 20
        
        # variables for moves scramble
        self.scramble_moves_speed = 0.0
        self.moves_speeds_matrix = [0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
        self.random_scramble_moves = 10
        self.random_scramble_moves_matrix = [0, 1, 5, 10, 25, 50, 100]
        self.max_scramble_moves = 100
        
        # variables for draw scramble
        self.chosen_draw_color = "blue"

        # variables for solve
        self.solve_moves_speed = 0.0

        # variables for instructions and guidelines
        self.cube_notation_text = "In the picture above you can see the official cube notation that I am using in this program. Typing in your keyboard\n\
one of these letter-keys you can execute the corresponding move on the cube. If you type a letter-key holding shift-\n\
key, you can execute the move in the opposite direction. Additionally, you can make all the moves using only your\n\
mouse (left click and drag for layer moves and right click and drag for rotations).\n\
The notation for the opposite direction moves uses the exact same letters but with an apostrophe next to them. For\n\
example, R' (R prime) means R move but in the opposite direction. Finally, you may also meet the case where a letter\n\
is followed by the number 2, which means that you have to execute the specified move two times in a row. For\n\
example, the notation U2 (in this writing you can consider it as one move), is equivalent to U, U.\n\
Image source: https://jperm.net/3x3/moves ."
        self.reset_text = "You may press the ⓘ (it appears at the upper left corner of the window) to understand how to read the 3x3 Rubik's cube\n\
notation and how to enter the moves into the program in order to be executed. You can change the observation view of the\n\
cube pressing the numbers 4, 6, 8, 2 and also reset it to default (top white side, front green side, right red side) pressing 5.\n\
Additionally, you can move the cube around inside the window and zoom-in or zoom-out using the mousewheel.\n\
Scramble the cube typing moves or pressing the \"random scramble\" button and then solve it yourself or let the computer\n\
solve it pressing the \"solve\" button. An other very important feature of the program is that you have the opportunity to\n\
draw a (valid of course) scrambled cube pattern (pressing the \"draw pattern\" button) and see the solution on your screen."
        self.moves_scramble_text = f"You can make {self.max_scramble_moves} scramble moves maximum. Whenever you are ready press the \"solve\" button or try to solve the cube yourself pressing the button below."
        self.draw_scramble_text = "Choose the proper colors and paint the cube. Move around the cube pressing the \"view\" numbers 4, 6, 8, 2\n\
and 5. Whenever you 're ready press the \"solve\" button to see the solution of the cube pattern you made."
        self.cube_is_solved_text = "You can make new scramble moves or draw a pattern pressing the buttons \"random scramble\" and \"draw\n\
pattern\" respectively. Alternatively you can make the same scramble pressing the button below."
        self.wrong_pattern_text = "This cube pattern cannot be derived from a solved cube. You can fix the scramble pressing the button below."
        self.replay_moves_text = "You can use the buttons above\nto replay the solve moves. It also\nworks if you press \"0\", \"1\", \"3\"\nand \"double 0\" respectively."
        
        # other variables
        self.game_state = "moves_scramble"
        self.previous_game_state = "moves_scramble"
        self.mouse_move_info = None
        self.replay_mode_is_activated = False
        self.moves_pointer = 0
        self.sound_is_activated = True
        
        # menus
        self.reset_button = menu_button(self.menu_background, "reset", "Arial 20 bold", "white", "black", self.menu_background_width / 2, 40, self.reset_game).button
        self.show_instructions_button = menu_button(self.menu_background, "ⓘ", "Arial 20 bold", "white", "black", 25, 25, self.show_instructions).button
        self.sound_button = menu_button(self.menu_background, "🔊", "Arial 20 bold", "white", "black", self.menu_background_width - 25, 20, self.enable_disable_sound).button
        menu_label(self.menu_background, "Created by Printzios Lampros.", "Times 15 bold", "white", "black", self.menu_background_width / 2, self.menu_background_height - 10).label

        # cube graphics menu
        cube_graphics_menu_cors = [self.menu_background_width / 2, 100]
        first_element_yoffset = 50
        self.cube_graphics_menu_label = menu_label(self.menu_background, "Cube graphics:", "Times 30 bold", "yellow", "black", cube_graphics_menu_cors[0], cube_graphics_menu_cors[1]).label
        self.borders_width_label = menu_label(self.menu_background, "borders width:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 20, cube_graphics_menu_cors[1] + first_element_yoffset).label
        self.borders_width_button = menu_button(self.menu_background, self.borders_width, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 90, cube_graphics_menu_cors[1] + first_element_yoffset, self.change_game_settings_cube_graphics).button
        self.sides_distortion_label = menu_label(self.menu_background, "sides distortion:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 30, cube_graphics_menu_cors[1] + first_element_yoffset + 40).label
        self.sides_distortion_button = menu_button(self.menu_background, self.sides_distortion, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 100, cube_graphics_menu_cors[1] + first_element_yoffset + 40, self.change_game_settings_cube_graphics).button
        self.hidden_sides_visibility_label = menu_label(self.menu_background, "hidden sides:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 30, cube_graphics_menu_cors[1] + first_element_yoffset + 80).label
        self.hidden_sides_visibility_button = menu_button(self.menu_background, self.hidden_sides_visibility, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 80, cube_graphics_menu_cors[1] + first_element_yoffset + 80, self.change_game_settings_cube_graphics).button
        self.axis_visibility_label = menu_label(self.menu_background, "3d axis:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 30, cube_graphics_menu_cors[1] + first_element_yoffset + 120).label
        self.axis_visibility_button = menu_button(self.menu_background, self.axis_visibility, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 45, cube_graphics_menu_cors[1] + first_element_yoffset + 120, self.change_game_settings_cube_graphics).button
        self.scramble_pattern_visibility_label = menu_label(self.menu_background, "scramble pattern:", "Arial 18 bold", "red", "black", cube_graphics_menu_cors[0] - 25, cube_graphics_menu_cors[1] + first_element_yoffset + 160).label
        self.scramble_pattern_visibility_button = menu_button(self.menu_background, self.scramble_pattern_visibility, "Arial 20 bold", "white", "black", cube_graphics_menu_cors[0] + 105, cube_graphics_menu_cors[1] + first_element_yoffset + 160, self.change_game_settings_cube_graphics).button
        self.cube_dimensions_button = menu_button(self.cube_background, self.cube_dimensions, "Arial 25 bold", "darkblue", "cyan", 50, self.cube_background_height - 40, self.change_game_settings_cube_graphics).button

        # scramble cube menu
        scramble_cube_menu_cors = [self.menu_background_width / 2, 380]
        first_element_yoffset = 50
        self.scramble_cube_menu_label = menu_label(self.menu_background, "Scramble cube:", "Times 30 bold", "yellow", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1]).label
        self.scramble_moves_speed_label = menu_label(self.menu_background, "time/move (sec):", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 25, scramble_cube_menu_cors[1] + first_element_yoffset).label
        self.scramble_moves_speed_button = menu_button(self.menu_background, self.scramble_moves_speed, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 100, scramble_cube_menu_cors[1] + first_element_yoffset, self.change_game_settings_cube_graphics).button
        self.moves_number_label = menu_label(self.menu_background, "moves number:", "Arial 18 bold", "red", "black", scramble_cube_menu_cors[0] - 25, scramble_cube_menu_cors[1] + first_element_yoffset + 40).label
        self.moves_number_button = menu_button(self.menu_background, self.random_scramble_moves, "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0] + 95, scramble_cube_menu_cors[1] + first_element_yoffset + 40, self.change_game_settings_cube_graphics).button
        self.scramble_cube_button = menu_button(self.menu_background, "random scramble", "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1] + first_element_yoffset + 80, self.moves_scramble_cube).button
        self.draw_scramble_pattern_button = menu_button(self.menu_background, "draw pattern", "Arial 20 bold", "white", "black", scramble_cube_menu_cors[0], scramble_cube_menu_cors[1] + first_element_yoffset + 120, self.draw_scramble_cube).button

        # solve cube
        solve_cube_menu_cors = [self.menu_background_width / 2, 620]
        first_element_yoffset = 50
        self.solve_cube_menu_label = menu_label(self.menu_background, "Solve cube:", "Times 30 bold", "yellow", "black", solve_cube_menu_cors[0], solve_cube_menu_cors[1]).label
        self.solve_moves_speed_label = menu_label(self.menu_background, "time/move (sec):", "Arial 18 bold", "red", "black", solve_cube_menu_cors[0] - 25, solve_cube_menu_cors[1] + first_element_yoffset).label
        self.solve_moves_speed_button = menu_button(self.menu_background, self.solve_moves_speed, "Arial 20 bold", "white", "black", solve_cube_menu_cors[0] + 100, solve_cube_menu_cors[1] + first_element_yoffset, self.change_game_settings_cube_graphics).button
        self.auto_solve_cube_button = menu_button(self.menu_background, "solve", "Arial 20 bold", "white", "black", solve_cube_menu_cors[0], solve_cube_menu_cors[1] + first_element_yoffset + 40, lambda event: self.auto_solve_cube("choose_method", None, None, event)).button

        # bindings
        self.buttons_bindings_are_activated = True
        self.moves_bindings_are_activated = True
        self.cube_background.bind("<Double-Button-2>", lambda event: self.reset_cube_position(event))
        self.cube_background.bind("<Button-2>", lambda event: self.cube_zoom_transfer_mouse_events(event))
        self.cube_background.bind("<B2-Motion>", lambda event: self.cube_zoom_transfer_mouse_events(event))
        self.cube_background.bind("<MouseWheel>", lambda event: self.cube_zoom_transfer_mouse_events(event))
        self.cube_background.bind("<ButtonRelease-1>", lambda event: self.cube_moves_mouse_events(None, event))
        self.cube_background.bind("<Button-3>", lambda event: self.cube_rotations_mouse_events(event))
        self.cube_background.bind("<ButtonRelease-3>", lambda event: self.cube_rotations_mouse_events(event))
        self.root.bind("<Key-r>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["R"], True, event))
        self.root.bind("<Key-R>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["R'"], True, event))
        self.root.bind("<Key-l>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["L"], True, event))
        self.root.bind("<Key-L>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["L'"], True, event))
        self.root.bind("<Key-u>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["U"], True, event))
        self.root.bind("<Key-U>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["U'"], True, event))
        self.root.bind("<Key-d>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["D"], True, event))
        self.root.bind("<Key-D>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["D'"], True, event))
        self.root.bind("<Key-f>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["F"], True, event))
        self.root.bind("<Key-F>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["F'"], True, event))
        self.root.bind("<Key-b>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["B"], True, event))
        self.root.bind("<Key-B>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["B'"], True, event))
        self.root.bind("<Key-m>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["M"], True, event))
        self.root.bind("<Key-M>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["M'"], True, event))
        self.root.bind("<Key-e>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["E"], True, event))
        self.root.bind("<Key-E>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["E'"], True, event))
        self.root.bind("<Key-s>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["S"], True, event))
        self.root.bind("<Key-S>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["S'"], True, event))
        self.root.bind("<Key-x>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["x"], True, event))
        self.root.bind("<Key-X>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["x'"], True, event))
        self.root.bind("<Key-y>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["y"], True, event))
        self.root.bind("<Key-Y>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["y'"], True, event))
        self.root.bind("<Key-z>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["z"], True, event))
        self.root.bind("<Key-Z>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["z'"], True, event))
        self.root.bind("<Key-Left>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["y"], True, event))
        self.root.bind("<Key-Right>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["y'"], True, event))
        self.root.bind("<Key-Up>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["x"], True, event))
        self.root.bind("<Down>", lambda event: self.make_moves_sequence(self.rubiks_cube, ["x'"], True, event))
        self.root.bind("<Key-4>", lambda event: self.change_cube_view(self.rubiks_cube, "y", event))
        self.root.bind("<Key-6>", lambda event: self.change_cube_view(self.rubiks_cube, "y'", event))
        self.root.bind("<Key-8>", lambda event: self.change_cube_view(self.rubiks_cube, "x", event))
        self.root.bind("<Key-2>", lambda event: self.change_cube_view(self.rubiks_cube, "x'", event))
        self.root.bind("<Key-5>", lambda event: self.reset_cube_view(event))
        self.root.bind("<Key-1>", lambda event: self.show_previous_next_solve_move("previous", event))
        self.root.bind("<Key-3>", lambda event: self.show_previous_next_solve_move("next", event))
        self.root.bind("<Key-0>", lambda event: self.show_previous_next_solve_move("start", event))
        self.root.bind("<Double-Key-0>", lambda event: self.show_previous_next_solve_move("end", event))

        self.reset_game()

    def left(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[0][i][0] = [cube[1][x][2] for x in [2, 1, 0]][i]
            cube2[1][i][2] = [cube[5][x][0] for x in [2, 1, 0]][i]
            cube2[3][i][0] = [cube[0][x][0] for x in [0, 1, 2]][i]
            cube2[5][i][0] = [cube[3][x][0] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[2][i][j] = [[cube[2][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def right(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[3][i][2] = [cube[5][x][2] for x in [0, 1, 2]][i]
            cube2[5][i][2] = [cube[1][x][0] for x in [2, 1, 0]][i]
            cube2[0][i][2] = [cube[3][x][2] for x in [0, 1, 2]][i]
            cube2[1][i][0] = [cube[0][x][2] for x in [2, 1, 0]][i]
            for j in range(3):
                cube2[4][i][j] = [[cube[4][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def up(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[0][2][i] = [cube[2][x][2] for x in [2, 1, 0]][i]
            cube2[2][i][2] = [cube[5][0][x] for x in [0, 1, 2]][i]
            cube2[4][i][0] = [cube[0][2][x] for x in [0, 1, 2]][i]
            cube2[5][0][i] = [cube[4][x][0] for x in [2, 1, 0]][i]
            for j in range(3):
                cube2[3][i][j] = [[cube[3][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def down(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[0][0][i] = [cube[4][x][2] for x in [0, 1, 2]][i]
            cube2[2][i][0] = [cube[0][0][x] for x in [2, 1, 0]][i]
            cube2[4][i][2] = [cube[5][2][x] for x in [2, 1, 0]][i]
            cube2[5][2][i] = [cube[2][x][0] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[1][i][j] = [[cube[1][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def front(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[1][2][i] = [cube[4][2][x] for x in [0, 1, 2]][i]
            cube2[2][2][i] = [cube[1][2][x] for x in [0, 1, 2]][i]
            cube2[3][2][i] = [cube[2][2][x] for x in [0, 1, 2]][i]
            cube2[4][2][i] = [cube[3][2][x] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[5][i][j] = [[cube[5][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def back(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[1][0][i] = [cube[2][0][x] for x in [0, 1, 2]][i]
            cube2[2][0][i] = [cube[3][0][x] for x in [0, 1, 2]][i]
            cube2[3][0][i] = [cube[4][0][x] for x in [0, 1, 2]][i]
            cube2[4][0][i] = [cube[1][0][x] for x in [0, 1, 2]][i]
            for j in range(3):
                cube2[0][i][j] = [[cube[0][x][y] for y in range(3)] for x in range(3)][-j + 2][i]
        return cube2
    def midM(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[0][i][1] = [cube[1][x][1] for x in [2, 1, 0]][i]
            cube2[1][i][1] = [cube[5][x][1] for x in [2, 1, 0]][i]
            cube2[3][i][1] = [cube[0][x][1] for x in [0, 1, 2]][i]
            cube2[5][i][1] = [cube[3][x][1] for x in [0, 1, 2]][i]
        return cube2
    def midE(self, cube):
        cube2 = self.copy_cube(cube)
        for i in range(3):
            cube2[0][1][i] = [cube[4][x][1] for x in [0, 1, 2]][i]
            cube2[2][i][1] = [cube[0][1][x] for x in [2, 1, 0]][i]
            cube2[4][i][1] = [cube[5][1][x] for x in [2, 1, 0]][i]
            cube2[5][1][i] = [cube[2][x][1] for x in [0, 1, 2]][i]
        return cube2
    def midS(self, cube):
        cube2 = self.copy_cube(cube)
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
    def print_cube(self, cube):
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
    def get_colors_rubik_solver_library(self, cube):
        cube_colors = ""
        for i in [3, 2, 5, 4, 0, 1]:
            for j in range(3):
                for k in range(3):
                    if i in [3, 5]:
                        cube_colors += cube[i][j][k]
                    if i in [0, 1]:
                        cube_colors += cube[i][2-j][2-k]
                    if i == 2:
                        cube_colors += cube[i][k][2-j]
                    if i == 4:
                        cube_colors += cube[i][2-k][j]
        return cube_colors
    def copy_cube(self, cube):
        return [[[cube[x][y][z] for z in range(3)] for y in range(3)] for x in range(6)]
    def alternate_matrix_elements(self, matrix, index_element):
        return (matrix[1:] + [matrix[0]])[matrix.index(index_element)]
    def play_sound(self, sound_file, sound_type):
        if sound_type == "music":
            if self.sound_is_activated:
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.load(os.getcwd() + "/game_sounds/" + sound_file + ".mp3")
                pygame.mixer.music.play(-1)
        elif sound_type == "sound":
            if self.sound_is_activated:
                self.sound = pygame.mixer.Sound(os.getcwd() + "/game_sounds/" + sound_file + ".wav")
                self.sound.play()

    def change_game_settings_cube_graphics(self, event):
        if event.widget == self.scramble_moves_speed_button:
            self.scramble_moves_speed = self.alternate_matrix_elements(self.moves_speeds_matrix, self.scramble_moves_speed)
            self.scramble_moves_speed_button.configure(text = self.scramble_moves_speed)
            if self.game_state == "moves_scramble":
                self.moves_speed = self.scramble_moves_speed
        elif event.widget == self.moves_number_button:
            self.random_scramble_moves = self.alternate_matrix_elements(self.random_scramble_moves_matrix, self.random_scramble_moves)
            self.moves_number_button.configure(text = self.random_scramble_moves)
        elif event.widget == self.scramble_pattern_visibility_button:
            self.scramble_pattern_visibility = self.alternate_matrix_elements(["on", "off"], self.scramble_pattern_visibility)
            self.scramble_pattern_visibility_button.configure(text = self.scramble_pattern_visibility)
        elif event.widget == self.solve_moves_speed_button:
            self.solve_moves_speed = self.alternate_matrix_elements(self.moves_speeds_matrix, self.solve_moves_speed)
            self.solve_moves_speed_button.configure(text = self.solve_moves_speed)
            if self.game_state == "auto_solve":
                self.moves_speed = self.solve_moves_speed
        elif event.widget == self.cube_dimensions_button:
            self.cube_dimensions = self.alternate_matrix_elements(self.cube_dimensions_matrix, self.cube_dimensions)
            self.cube_dimensions_button.configure(text = self.cube_dimensions)
            if self.cube_dimensions == "3d":
                self.piece_side_length = 2 * self.piece_side_length
            elif self.cube_dimensions == "2d":
                self.piece_side_length = 1 / 2 * self.piece_side_length
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
        self.make_cube_graphics(self.rubiks_cube, None)
    def cube_zoom_transfer_mouse_events(self, event):
        if event.type == "38":       # MouseWheel event
            if event.delta == -120 and self.piece_side_length > 10:
                self.piece_side_length -= 5
            elif event.delta == 120 and self.piece_side_length < 200:
                self.piece_side_length += 5
        elif event.type == "4":      # Button-2 event
            self.lastx = event.x
            self.lasty = event.y
        elif event.type == "6":      # B2-Motion event
            self.visible_cube_centre_x = self.visible_cube_centre_x + event.x - self.lastx
            self.visible_cube_centre_y = self.visible_cube_centre_y + event.y - self.lasty
            self.lastx = event.x
            self.lasty = event.y
        self.make_cube_graphics(self.rubiks_cube, None)
    def cube_moves_mouse_events(self, piece_info, event):
        if self.cube_dimensions == "3d":
            if event.type == "4":        # Button-1 event
                self.lastx2 = event.x
                self.lasty2 = event.y
                self.mouse_move_info = piece_info
            elif event.type == "5" and self.mouse_move_info != None:        # ButtonRelease-1 event
                index1 = [True, False].index(abs(event.x - self.lastx2) >= abs(event.y - self.lasty2))
                index2 = [True, False].index(event.x >= self.lastx2)
                index3 = [True, False].index(event.y >= self.lasty2)
                if int(self.mouse_move_info[0]) == 5:
                    self.make_moves_sequence(self.rubiks_cube, [[[["U'"], ["U"]], [["E"], ["E'"]], [["D"], ["D'"]]][int(self.mouse_move_info[1])][index2], \
                                                                [[["L"], ["L'"]], [["M"], ["M'"]], [["R'"], ["R"]]][int(self.mouse_move_info[2])][index3]][index1], True, event)
                elif int(self.mouse_move_info[0]) == 3:
                    self.make_moves_sequence(self.rubiks_cube, [[[["B'"], ["B"]], [["S"], ["S'"]], [["F"], ["F'"]]][int(self.mouse_move_info[1])][index2], \
                                                                [[["L"], ["L'"]], [["M"], ["M'"]], [["R'"], ["R"]]][int(self.mouse_move_info[2])][index3]][index1], True, event)
                elif int(self.mouse_move_info[0]) == 4:
                    self.make_moves_sequence(self.rubiks_cube, [[[["U'"], ["U"]], [["E"], ["E'"]], [["D"], ["D'"]]][int(self.mouse_move_info[1])][index2], \
                                                                [[["F"], ["F'"]], [["S"], ["S'"]], [["B'"], ["B"]]][int(self.mouse_move_info[2])][index3]][index1], True, event)
                self.mouse_move_info = None
    def cube_rotations_mouse_events(self, event):
        if self.cube_dimensions == "3d":
            if event.type == "4":        # Button-3 event
                self.lastx3 = event.x
                self.lasty3 = event.y
            elif event.type == "5":      # ButtonRelease-3 event
                index1 = [True, False].index(abs(event.x - self.lastx3) >= abs(event.y - self.lasty3))
                index2 = [True, False].index(event.x >= self.lastx3)
                index3 = [True, False].index(event.y >= self.lasty3)
                if self.game_state == "draw_scramble":
                    self.change_cube_view(self.rubiks_cube, [["y'", "y"][index2], ["x'", "x"][index3]][index1], event)
                else:
                    self.make_moves_sequence(self.rubiks_cube, [[["y'"], ["y"]][index2], [["x'"], ["x"]][index3]][index1], True, event)
    def reset_cube_position(self, event):
        self.visible_cube_centre_x = self.cube_background_width / 2
        self.visible_cube_centre_y = self.cube_background_height / 2
        self.make_cube_graphics(self.rubiks_cube, None)
    def enable_disable_sound(self, event):
        if self.sound_is_activated:
            self.sound_button.configure(text = "🔇")
        else:
            self.sound_button.configure(text = "🔊")
        self.sound_is_activated = not self.sound_is_activated
    def show_instructions(self, event = None):
        try: self.instructions_background.destroy()
        except AttributeError: pass
        self.instructions_background = tk.Canvas(self.root, width = self.cube_background_width, height = self.cube_background_height + self.down_area_background_height, bg = "yellow")
        self.instructions_background.grid(row = 0, column = 1, rowspan = 2, sticky = tk.NSEW)
        self.instructions_background.create_text(self.cube_background_width / 2, 40, text = "Cube notation", font = "Arial 30 bold italic", fill = "darkblue")
        self.cube_notation_picture = Image.open(os.getcwd() + "/rubiks_cube_notation.jpg")
        reduction_factor = 3 / 4
        self.cube_notation_picture = self.cube_notation_picture.resize((int(reduction_factor * self.cube_background_width), int(reduction_factor * self.cube_background_width * self.cube_notation_picture.height / self.cube_notation_picture.width)), Image.ANTIALIAS)
        self.cube_notation_picture = ImageTk.PhotoImage(self.cube_notation_picture)
        self.instructions_background.create_image(self.cube_background_width / 2, self.cube_notation_picture.height() / 2 + 80, image = self.cube_notation_picture)
        self.instructions_background.create_text(20, self.cube_notation_picture.height() + 120, text = self.cube_notation_text, font = "Calibri 15 bold", fill = "darkblue", anchor = tk.NW)
        self.back_button = menu_button(self.instructions_background, "back", "Calibri 25 bold", "black", "yellow", self.cube_background_width / 2, self.cube_background_height + self.down_area_background_height - 40, self.hide_instructions).button
    def hide_instructions(self, event):
        self.instructions_background.destroy()
    def reset_game(self, event = None):
        if self.buttons_bindings_are_activated:
            self.buttons_bindings_are_activated = True
            self.moves_bindings_are_activated = True
            self.replay_mode_is_activated = False
            self.destroy_down_area_buttons()
            self.game_state = "moves_scramble"
            self.previous_game_state = "moves_scramble"
            self.down_area_background.delete("all")
            self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2, text = self.reset_text, font = "Arial 12 bold", fill = "brown")
            self.rubiks_cube = [[[["b", "y", "o", "w", "r", "g"][x] for z in range(3)] for y in range(3)] for x in range(6)]
            self.moves_scrambled_rubiks_cube = self.copy_cube(self.rubiks_cube)
            self.draw_scrambled_rubiks_cube = [[[["c", "c", "c", "c", "c", "c"][x] for z in range(3)] for y in range(3)] for x in range(6)]
            self.random_scramble_moves_seq = []
            self.self_solve_moves_seq = []
            self.auto_solve_moves_seq = []
            self.replay_moves_seq = []
            self.adjust_cube_view_moves = []
            self.moves_speed = self.scramble_moves_speed
            self.reset_cube_view()
    def moves_scramble_cube(self, event = None):
        if self.buttons_bindings_are_activated:
            self.buttons_bindings_are_activated = False
            self.moves_bindings_are_activated = False
            self.replay_mode_is_activated = False
            self.previous_game_state = self.game_state
            self.game_state = "moves_scramble"
            self.moves_speed = self.scramble_moves_speed
            scramble_moves_before = len(self.random_scramble_moves_seq)
            if event != None:
                while len(self.random_scramble_moves_seq) < self.max_scramble_moves and len(self.random_scramble_moves_seq) != scramble_moves_before + self.random_scramble_moves:
                    self.random_scramble_moves_seq.append(random.choice(["L", "L'", "R", "R'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'"]))
                    self.random_scramble_moves_seq = self.improve_moves_sequence(self.random_scramble_moves_seq)
            self.write_moves_scramble_text()
            self.rubiks_cube = [[[["b", "y", "o", "w", "r", "g"][x] for z in range(3)] for y in range(3)] for x in range(6)]
            self.make_moves_sequence(self.rubiks_cube, [""] + self.random_scramble_moves_seq, True)
    def write_moves_scramble_text(self):
        self.destroy_down_area_buttons()
        self.self_solve_try_yourself_button = menu_button(self.down_area_background, "try yourself", "Arial 10 bold", "red", "yellow", self.down_area_background_width / 2, self.down_area_background_height - 15, self.self_solve_cube).button
        self.down_area_background.delete("all")
        self.down_area_background.create_text(self.down_area_background_width / 2, 20, text = "Scramble ({} moves in total):".format(len(self.random_scramble_moves_seq)), font = "Calibri 18 bold", fill = "black")
        row_chars = 35
        for index1 in range(len(self.random_scramble_moves_seq) // row_chars + 1):
            index2 = [len(self.random_scramble_moves_seq), row_chars * index1 + row_chars][[True, False].index(len(self.random_scramble_moves_seq) // row_chars == 0)]
            self.down_area_background.create_text(self.down_area_background_width / 2, 50 + 20 * index1, text = self.random_scramble_moves_seq[(row_chars * index1) : index2], font = "Arial 14 italic bold", fill = "darkblue")
        self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height - 40, text = self.moves_scramble_text, font = "Arial 10 bold", fill = "brown")
    def draw_scramble_cube(self, event = None):
        if self.buttons_bindings_are_activated:
            self.destroy_down_area_buttons()
            self.buttons_bindings_are_activated = True
            self.moves_bindings_are_activated = False
            self.replay_mode_is_activated = False
            self.previous_game_state = self.game_state
            self.game_state = "draw_scramble"
            self.rubiks_cube = self.copy_cube(self.draw_scrambled_rubiks_cube)
            self.down_area_background.delete("all")
            self.down_area_background.create_text(self.down_area_background_width / 2, 40, text = self.draw_scramble_text, font = "Arial 14 bold", fill = "brown")
            rect_side = 70
            edge_offset = 150
            centre_x_offset = ((self.down_area_background_width - 2 * edge_offset) - 6 * rect_side) / 10
            centre_y_offset = 30
            rect_x_offset = -80
            for k in range(6):
                self.down_area_background.create_rectangle([edge_offset + (rect_side + 2 * centre_x_offset) * k + rect_x_offset, self.down_area_background_height / 2 - rect_side / 2 + centre_y_offset, edge_offset + (rect_side + 2 * centre_x_offset) * k + rect_side + rect_x_offset, self.down_area_background_height / 2 + rect_side / 2 + centre_y_offset], fill = self.cube_colors[k], activefill = "black", width = 5, outline = "black", tags = self.cube_colors[k])
            self.down_area_background.tag_bind(self.cube_colors[0], "<Button-1>", lambda event: self.change_draw_color(self.cube_colors[0], event))
            self.down_area_background.tag_bind(self.cube_colors[1], "<Button-1>", lambda event: self.change_draw_color(self.cube_colors[1], event))
            self.down_area_background.tag_bind(self.cube_colors[2], "<Button-1>", lambda event: self.change_draw_color(self.cube_colors[2], event))
            self.down_area_background.tag_bind(self.cube_colors[3], "<Button-1>", lambda event: self.change_draw_color(self.cube_colors[3], event))
            self.down_area_background.tag_bind(self.cube_colors[4], "<Button-1>", lambda event: self.change_draw_color(self.cube_colors[4], event))
            self.down_area_background.tag_bind(self.cube_colors[5], "<Button-1>", lambda event: self.change_draw_color(self.cube_colors[5], event))
            self.clear_cube_draw_button = menu_button(self.down_area_background, "clear cube", "Arial 12 bold", "red", "yellow", self.down_area_background_width - 110, self.down_area_background_height / 2 + centre_y_offset - 15, self.clear_fill_cube_draw).button
            self.fill_cube_draw_button = menu_button(self.down_area_background, "fill cube", "Arial 12 bold", "red", "yellow", self.down_area_background_width - 110, self.down_area_background_height / 2 + centre_y_offset + 15, self.clear_fill_cube_draw).button
            self.change_draw_color(self.chosen_draw_color)
            self.make_cube_graphics(self.rubiks_cube, None)
    def clear_fill_cube_draw(self, event):
        if event.widget == self.clear_cube_draw_button:
            self.draw_scrambled_rubiks_cube = [[[["c", "c", "c", "c", "c", "c"][x] for z in range(3)] for y in range(3)] for x in range(6)]
        elif event.widget == self.fill_cube_draw_button:
            self.draw_scrambled_rubiks_cube = [[[["b", "y", "o", "w", "r", "g"][x] for z in range(3)] for y in range(3)] for x in range(6)]
        self.rubiks_cube = self.copy_cube(self.draw_scrambled_rubiks_cube)
        self.make_cube_graphics(self.rubiks_cube, None)
    def change_draw_color(self, color_chosen, event = None):
        self.chosen_draw_color = color_chosen
        for color in self.cube_colors:
            color_box = self.down_area_background.find_withtag(color)
            self.down_area_background.itemconfigure(color_box, width = 5)
        if event == None:
            color_box = self.down_area_background.find_withtag(self.chosen_draw_color)
        else:
            color_box = event.widget.find_closest(event.x, event.y)
        self.down_area_background.itemconfigure(color_box, width = 10)
        self.make_cube_graphics(self.rubiks_cube, None)
    def same_scramble_cube(self, event):
        if self.buttons_bindings_are_activated:
            self.destroy_down_area_buttons()
            if self.previous_game_state in ["moves_scramble", "self_solve"]:
                self.moves_scramble_cube()
            elif self.previous_game_state == "draw_scramble":
                self.draw_scramble_cube()
    def self_solve_cube(self, event):
        if self.buttons_bindings_are_activated:
            self.destroy_down_area_buttons()
            self.go_to_replay_previous_move_button = menu_button(self.down_area_background, "🡄", "Arial 14 bold", "blue", "yellow", 80, 20, lambda event: self.show_previous_next_solve_move("previous", event)).button
            self.go_to_replay_next_move_button = menu_button(self.down_area_background, "🡆", "Arial 14 bold", "blue", "yellow", 130, 20, lambda event: self.show_previous_next_solve_move("next", event)).button
            self.go_to_replay_start_button = menu_button(self.down_area_background, "⏮", "Arial 14 bold", "blue", "yellow", 30, 20, lambda event: self.show_previous_next_solve_move("start", event)).button
            self.go_to_replay_end_button = menu_button(self.down_area_background, "⏭", "Arial 14 bold", "blue", "yellow", 180, 20, lambda event: self.show_previous_next_solve_move("end", event)).button
            self.self_solve_try_again_button = menu_button(self.down_area_background, "try again", "Arial 10 bold", "red", "yellow", self.down_area_background_width - 80, 20, self.self_solve_cube).button
            self.previous_game_state = self.game_state
            self.game_state = "self_solve"
            self.buttons_bindings_are_activated = True
            self.moves_bindings_are_activated = True
            self.replay_mode_is_activated = False
            self.self_solve_moves_seq = []
            self.start_timer_self_solving = time.time()
            self.down_area_background.delete("all")
            self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2, text = "Clock just started ticking!", font = "Calibri 20 bold", fill = "purple")
            self.down_area_background.create_text(self.down_area_background_width / 2, 20, text = "Self solve ({} moves in total):".format(len(self.self_solve_moves_seq)), font = "Calibri 18 bold", fill = "black")
            self.rubiks_cube = self.copy_cube(self.moves_scrambled_rubiks_cube)
            self.make_cube_graphics(self.rubiks_cube, None)
    def auto_solve_cube(self, solve_mode_stage, solve_method_choose, start_color_choose, event):
        if solve_mode_stage == "choose_method":
            if self.buttons_bindings_are_activated and self.game_state not in ["self_solve", "auto_solve"]:
                self.destroy_down_area_buttons()
                self.down_area_background.delete("all")
                self.moves_bindings_are_activated = False
                self.replay_mode_is_activated = False
                if self.cube_is_solved(self.rubiks_cube):
                    if self.game_state != "auto_solve":
                        self.previous_game_state = self.game_state
                    self.down_area_background.create_text(self.down_area_background_width / 2, 40, text = "The cube is already solved!", font = "Arial 20 bold", fill = "brown")
                    self.down_area_background.create_text(self.down_area_background_width / 2, 90, text = self.cube_is_solved_text, font = "Arial 14 bold", fill = "brown")
                    self.down_area_background.create_text(90, self.down_area_background_height - 45, text = "Scramble:", font = "Arial 8 bold", fill = "black", anchor = tk.NW)
                    if self.previous_game_state == "moves_scramble" or self.previous_game_state == "self_solve":
                        row_chars = 25
                        for index1 in range(len(self.random_scramble_moves_seq) // row_chars + 1):
                            index2 = [len(self.random_scramble_moves_seq), row_chars * index1 + row_chars][[True, False].index(len(self.random_scramble_moves_seq) // row_chars == 0)]
                            self.down_area_background.create_text(160, self.down_area_background_height - 45 + 10 * index1, text = self.random_scramble_moves_seq[(row_chars * index1) : index2], font = "Arial 8 italic bold", fill = "black", anchor = tk.NW)
                    elif self.previous_game_state == "draw_scramble":
                        self.down_area_background.create_text(160, self.down_area_background_height - 45, text = "You can see the scrambled cube pattern enabling the cube graphics option \"scramble pattern\".", font = "Arial 8 italic bold", fill = "black", anchor = tk.NW)
                    self.same_scramble_cube_button = menu_button(self.down_area_background, "same scramble", "Arial 10 bold", "red", "yellow", self.down_area_background_width - 120, self.down_area_background_height - 30, self.same_scramble_cube).button
                else:
                    self.previous_game_state = self.game_state
                    self.game_state = "auto_solve"
                    self.make_cube_graphics(self.rubiks_cube, None)
                    self.down_area_background.create_text(self.down_area_background_width / 2, 30, text = "Select the solving method you want to be used:", font = "Arial 20 bold", fill = "brown")
                    self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2 - 10, text = "Beginner's method (simple and slow, many moves needed)", font = "Arial 18 bold", fill = "red", activefill = "blue", tags = "Beginner")
                    self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2 + 25, text = "CFOP method (advanced and fast, used in speedcubing)", font = "Arial 18 bold", fill = "red", activefill = "blue", tags = "CFOP")
                    self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2 + 60, text = "Kociemba's algorithm (the fastest way, 20 moves in average)", font = "Arial 18 bold", fill = "red", activefill = "blue", tags = "Kociemba")
                    self.down_area_background.tag_bind("Beginner", "<Button-1>", lambda event: self.auto_solve_cube("choose_color", "Beginner", None, event))
                    self.down_area_background.tag_bind("CFOP", "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", "CFOP", None, event))
                    self.down_area_background.tag_bind("Kociemba", "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", "Kociemba", None, event))
        elif solve_mode_stage == "choose_color":
            self.destroy_down_area_buttons()
            self.down_area_background.delete("all")
            rect_side = 90
            edge_offset = 140
            centre_x_offset = ((self.down_area_background_width - 2 * edge_offset) - 6 * rect_side) / 10
            centre_y_offset = 20
            self.down_area_background.create_text(self.down_area_background_width / 2, 30, text = "Choose the cube side you want to be solved first:", font = "Arial 20 bold", fill = "brown")
            for k in range(6):
                self.down_area_background.create_rectangle([edge_offset + (rect_side + 2 * centre_x_offset) * k, self.down_area_background_height / 2 - rect_side / 2 + centre_y_offset, edge_offset + (rect_side + 2 * centre_x_offset) * k + rect_side, self.down_area_background_height / 2 + rect_side / 2 + centre_y_offset], fill = self.cube_colors[k], activefill = "black", width = 5, outline = "black", tags = self.cube_colors[k])
            self.down_area_background.tag_bind(self.cube_colors[0], "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", solve_method_choose, self.cube_colors[0][0], event))
            self.down_area_background.tag_bind(self.cube_colors[1], "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", solve_method_choose, self.cube_colors[1][0], event))
            self.down_area_background.tag_bind(self.cube_colors[2], "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", solve_method_choose, self.cube_colors[2][0], event))
            self.down_area_background.tag_bind(self.cube_colors[3], "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", solve_method_choose, self.cube_colors[3][0], event))
            self.down_area_background.tag_bind(self.cube_colors[4], "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", solve_method_choose, self.cube_colors[4][0], event))
            self.down_area_background.tag_bind(self.cube_colors[5], "<Button-1>", lambda event: self.auto_solve_cube("solve_cube", solve_method_choose, self.cube_colors[5][0], event))
        elif solve_mode_stage == "solve_cube":
            try:
                if self.buttons_bindings_are_activated:
                    self.buttons_bindings_are_activated = False
                    self.moves_bindings_are_activated = False
                    self.moves_speed = self.solve_moves_speed
                    if solve_method_choose == "Beginner":
                        rubiks_cube2 = self.copy_cube(self.rubiks_cube)
                        initial_solved_color = start_color_choose
                        edges = [["101", "001"], ["112", "210"], ["121", "521"], ["110", "412"], \
                                ["012", "401"], ["201", "010"], ["510", "221"], ["421", "512"], \
                                ["301", "021"], ["310", "212"], ["321", "501"], ["312", "410"]]  # in order: down edges, middle edges, up edges
                        corners = [["122", "220", "520"], ["120", "522", "422"], ["100", "402", "002"], ["102", "000", "200"], \
                                ["320", "222", "500"], ["322", "502", "420"], ["302", "400", "022"], ["300", "020", "202"]]  # in order: down corners, up corners
                        final_solved_color = ["b", "r", "y", "g", "o", "w"][(["b", "r", "y", "g", "o", "w"].index(initial_solved_color) + 3) % 6]
                        middle_centres = [["r", "w", "o", "y"], ["g", "w", "b", "y"], ["b", "o", "g", "r"]][["b", "r", "y", "g", "o", "w"].index(initial_solved_color) % 3]
                        if initial_solved_color in ["g", "o", "w"]:
                            middle_centres.reverse()
                        # putting the proper centre facing down
                        solve_moves = []
                        solve_moves2 = []
                        centres = [side[1][1] for side in rubiks_cube2]
                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [["x"], [], ["z'"], ["x", "x"], ["z"], ["x'"]][centres.index(initial_solved_color)], False)
                        solve_moves.append([["x"], [], ["z'"], ["x", "x"], ["z"], ["x'"]][centres.index(initial_solved_color)])
                        # making the down cross
                        cross_pieces_solved = []
                        edges_examined = [edges[k] for k in range(len(edges)-1, -1, -1)]
                        for counter in range(4):
                            for edge in edges_examined:
                                edge_colors = [rubiks_cube2[int(edge[0][0])][int(edge[0][1])][int(edge[0][2])], \
                                            rubiks_cube2[int(edge[1][0])][int(edge[1][1])][int(edge[1][2])]]
                                if initial_solved_color in edge_colors:
                                    not_cross_color = edge_colors[1 - edge_colors.index(initial_solved_color)]
                                    if not_cross_color not in cross_pieces_solved:
                                        edge_layer = edges.index(edge) // 4
                                        if edge_layer == 0 and edge_colors[0] == initial_solved_color and edge_colors[1] == rubiks_cube2[int(edge[1][0])][1][1]:
                                            # edge already in the correct position
                                            cross_pieces_solved.append(not_cross_color)
                                        else:
                                            # put edge in front up middle position
                                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], ["y" + (abs([0, 2, 2][edge_layer] - int(edge[0][2])) // 2) * "'"], ["y", "y"]][2 - int(edge[0][1])] + [["F", "F"], ["F'", "U'", "F", "U"], []][edge_layer], False)
                                            solve_moves.append([[], ["y" + (abs([0, 2, 2][edge_layer] - int(edge[0][2])) // 2) * "'"], ["y", "y"]][2 - int(edge[0][1])] + [["F", "F"], ["F'", "U'", "F", "U"], []][edge_layer])
                                            # put edge in the correct position
                                            offset = middle_centres.index(rubiks_cube2[5][1][1]) - middle_centres.index(not_cross_color)
                                            edge_orientation = edge_colors.index(initial_solved_color)
                                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[["F'", "F'"], ["U", "L", "L"], ["U", "U", "B", "B"], ["U'", "R", "R"]], \
                                                                                                [["U'", "M'", "U", "M"], ["F'", "L", "F"], ["U", "M", "U", "M'"], ["F", "R'", "F'"]]][edge_orientation][offset], False)
                                            solve_moves.append([[["F'", "F'"], ["U", "L", "L"], ["U", "U", "B", "B"], ["U'", "R", "R"]], \
                                                        [["U'", "M'", "U", "M"], ["F'", "L", "F"], ["U", "M", "U", "M'"], ["F", "R'", "F'"]]][edge_orientation][offset])
                                            cross_pieces_solved.append(not_cross_color)
                                            break
                        solve_moves2.append([move for k in range(len(solve_moves)) for move in solve_moves[k]])
                        # solving the down side corners
                        solve_moves = []
                        down_corners_solved = []
                        corners_examined = [corners[k] for k in range(len(corners)-1, -1, -1)]
                        for counter in range(4):
                            for corner in corners_examined:
                                corner_colors = [rubiks_cube2[int(corner[0][0])][int(corner[0][1])][int(corner[0][2])], \
                                                rubiks_cube2[int(corner[1][0])][int(corner[1][1])][int(corner[1][2])], \
                                                rubiks_cube2[int(corner[2][0])][int(corner[2][1])][int(corner[2][2])]]
                                if initial_solved_color in corner_colors:
                                    other_corner_colors = [corner_colors[corner_colors.index(initial_solved_color) - 1], corner_colors[corner_colors.index(initial_solved_color) - 2]]
                                    if other_corner_colors not in down_corners_solved and [other_corner_colors[1], other_corner_colors[0]] not in down_corners_solved:
                                        corner_layer = corners.index(corner) // 4
                                        if corner_layer == 0 and corner_colors[0] == initial_solved_color and corner_colors[1] == rubiks_cube2[int(corner[1][0])][1][1] and corner_colors[2] == rubiks_cube2[int(corner[2][0])][1][1]:
                                            # corner already in the correct position
                                            down_corners_solved.append(other_corner_colors)
                                        else:
                                            # put corner in front up right position
                                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[["y"], ["y", "y"]][corner_layer], [["y", "y"], [], ["y"], ["y'"]][int(int(corner[0][1]) / 2 + 2 * corner_layer)], [["y'"], []][corner_layer]][int((int(corner[0][1]) + int(corner[0][2])) / 2)] + [["R", "U", "R'", "U'"], []][corner_layer], False)
                                            solve_moves.append([[["y"], ["y", "y"]][corner_layer], [["y", "y"], [], ["y"], ["y'"]][int(int(corner[0][1]) / 2 + 2 * corner_layer)], [["y'"], []][corner_layer]][int((int(corner[0][1]) + int(corner[0][2])) / 2)] + [["R", "U", "R'", "U'"], []][corner_layer])
                                            # put corner in the correct position
                                            offset = [2, [1, 3][[True, False].index(rubiks_cube2[5][1][1] in other_corner_colors)], 0][[rubiks_cube2[5][1][1] in other_corner_colors, rubiks_cube2[4][1][1] in other_corner_colors].count(True)]
                                            corner_orientation = [rubiks_cube2[3][2][2] == initial_solved_color, rubiks_cube2[5][0][2] == initial_solved_color, rubiks_cube2[4][2][0] == initial_solved_color].index(True)
                                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[["R", "U'", "U'", "R'", "U'", "R", "U", "R'"], ["U", "L'", "U", "L", "U", "U", "L'", "U'", "L"], ["L", "U", "L'", "U", "L", "U'", "L'"], ["U'", "R'", "U", "U", "R", "U", "R'", "U'", "R"]], \
                                                                                                [["U", "R", "U'", "R'"], ["U", "L'", "U'", "L"], ["L", "U", "U", "L'"], ["B", "U'", "B'"]], \
                                                                                                [["R", "U", "R'"], ["L'", "U", "L"], ["U", "U", "L", "U", "L'"], ["U'", "U'", "R'", "U", "R"]]][corner_orientation][offset], False)
                                            solve_moves.append([[["R", "U'", "U'", "R'", "U'", "R", "U", "R'"], ["U", "L'", "U", "L", "U", "U", "L'", "U'", "L"], ["L", "U", "L'", "U", "L", "U'", "L'"], ["U'", "R'", "U", "U", "R", "U", "R'", "U'", "R"]], \
                                                                [["U", "R", "U'", "R'"], ["U", "L'", "U'", "L"], ["L", "U", "U", "L'"], ["B", "U'", "B'"]], \
                                                                [["R", "U", "R'"], ["L'", "U", "L"], ["U", "U", "L", "U", "L'"], ["U'", "U'", "R'", "U", "R"]]][corner_orientation][offset])
                                            down_corners_solved.append(other_corner_colors)
                                            break
                        solve_moves2.append([move for k in range(len(solve_moves)) for move in solve_moves[k]])
                        # solving the middle edges
                        solve_moves = []
                        middle_edges_solved = []
                        edges_examined = [edges[k] for k in range(len(edges)-1, 3, -1)]
                        for counter in range(4):
                            for edge in edges_examined:
                                edge_colors = [rubiks_cube2[int(edge[0][0])][int(edge[0][1])][int(edge[0][2])], \
                                            rubiks_cube2[int(edge[1][0])][int(edge[1][1])][int(edge[1][2])]]
                                if final_solved_color not in edge_colors and edge_colors not in middle_edges_solved and [edge_colors[1], edge_colors[0]] not in middle_edges_solved:
                                    edge_layer = edges[4:].index(edge) // 4
                                    if edge_layer == 0 and edge_colors[0] == rubiks_cube2[int(edge[0][0])][1][1] and edge_colors[1] == rubiks_cube2[int(edge[1][0])][1][1]:
                                        middle_edges_solved.append(edge_colors)
                                    else:
                                        # put edge in front up middle position
                                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], ["y" + ((2 - int(edge[0][2])) // 2) * "'"], ["y", "y"]][2 - int(edge[0][1])] + [["F'", "U", "F", "U", "R", "U'", "R'", "U'"], []][edge_layer], False)
                                        solve_moves.append([[], ["y" + ((2 - int(edge[0][2])) // 2) * "'"], ["y", "y"]][2 - int(edge[0][1])] + [["F'", "U", "F", "U", "R", "U'", "R'", "U'"], []][edge_layer])
                                        # put edge in the correct position
                                        offset = middle_centres.index(rubiks_cube2[5][1][1]) - middle_centres.index(edge_colors[1])
                                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], ["y'", "U"], ["y", "y", "U", "U"], ["y", "U'"]][offset], False)
                                        solve_moves.append([[], ["y'", "U"], ["y", "y", "U", "U"], ["y", "U'"]][offset])
                                        edge_orientation = [True, False].index(edge_colors[0] == rubiks_cube2[4][1][1])
                                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [["U", "R", "U'", "R'", "U'", "F'", "U", "F"], ["U'", "L'", "U", "L", "U", "F", "U'", "F'"]][edge_orientation], False)
                                        solve_moves.append([["U", "R", "U'", "R'", "U'", "F'", "U", "F"], ["U'", "L'", "U", "L", "U", "F", "U'", "F'"]][edge_orientation])
                                        middle_edges_solved.append(edge_colors)
                                        break
                        solve_moves2.append([move for k in range(len(solve_moves)) for move in solve_moves[k]])
                        # making the up cross and orienting it
                        solve_moves = []
                        edges_examined = [edge for edge in edges[8:]]
                        up_edges_colors = [rubiks_cube2[int(edge[0][0])][int(edge[0][1])][int(edge[0][2])] for edge in edges_examined]
                        up_case = int(up_edges_colors.count(final_solved_color) // 2)
                        angle_line_case = [0, 1][[True, False].index((up_edges_colors[0] == final_solved_color) ^ (up_edges_colors[2] == final_solved_color))]
                        check_up_left_back_edge_color = [rubiks_cube2[3][0][1], rubiks_cube2[3][1][0]]
                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [["F", "R", "U", "R'", "U'", "S", "R", "U", "R'", "U'", "S'", "F'"], \
                                                                            [[["U", "U"], [["U'"], ["U"]][[True, False].index(check_up_left_back_edge_color[0] == final_solved_color)], []][check_up_left_back_edge_color.count(final_solved_color)] + ["F", "U", "R", "U'", "R'", "F'"], \
                                                                            [["U"], []][[True, False].index(check_up_left_back_edge_color[0] == final_solved_color)] + ["F", "R", "U", "R'", "U'", "F'"]][angle_line_case], []][up_case], False)
                        solve_moves.append([["F", "R", "U", "R'", "U'", "S", "R", "U", "R'", "U'", "S'", "F'"], \
                                            [[["U", "U"], [["U'"], ["U"]][[True, False].index(check_up_left_back_edge_color[0] == final_solved_color)], []][check_up_left_back_edge_color.count(final_solved_color)] + ["F", "U", "R", "U'", "R'", "F'"], \
                                            [["U"], []][[True, False].index(check_up_left_back_edge_color[0] == final_solved_color)] + ["F", "R", "U", "R'", "U'", "F'"]][angle_line_case], []][up_case])
                        not_cross_colors = [rubiks_cube2[int(edge[1][0])][int(edge[1][1])][int(edge[1][2])] for edge in edges_examined]
                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [["U", "U"], ["U'"], [], ["U"]][not_cross_colors.index(rubiks_cube2[5][1][1])], False)
                        solve_moves.append([["U", "U"], ["U'"], [], ["U"]][not_cross_colors.index(rubiks_cube2[5][1][1])])
                        right_edge_offset = abs(middle_centres.index(rubiks_cube2[4][1][1]) - middle_centres.index(rubiks_cube2[4][1][0]))
                        left_edge_offset = abs(middle_centres.index(rubiks_cube2[2][1][1]) - middle_centres.index(rubiks_cube2[2][1][2]))
                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[[], ["y'", "R", "U", "R'", "U", "R", "U'", "U'", "R'", "U"]][left_edge_offset % 2], \
                                                                            [["y", "y", "R", "U", "R'", "U", "R", "U'", "U'", "R'", "U"], ["R", "R", "U'", "R'", "U'", "R", "U", "R", "U", "R", "U'", "R"]][left_edge_offset // 2], \
                                                                            [["R'", "U", "R'", "U'", "R'", "U'", "R'", "U", "R", "U", "R", "R"], ["R", "U", "R'", "U'", "R'", "F", "R", "R", "U'", "R'", "U'", "R", "U", "R'", "F'"]][[0, 0, 1, 0][left_edge_offset]]][[0, 1, 2, 1][right_edge_offset]], False)
                        solve_moves.append([[[], ["y'", "R", "U", "R'", "U", "R", "U'", "U'", "R'", "U"]][left_edge_offset % 2], \
                                            [["y", "y", "R", "U", "R'", "U", "R", "U'", "U'", "R'", "U"], ["R", "R", "U'", "R'", "U'", "R", "U", "R", "U", "R", "U'", "R"]][left_edge_offset // 2], \
                                            [["R'", "U", "R'", "U'", "R'", "U'", "R'", "U", "R", "U", "R", "R"], ["R", "U", "R'", "U'", "R'", "F", "R", "R", "U'", "R'", "U'", "R", "U", "R'", "F'"], []][[0, 0, 1, 0][left_edge_offset]]][[0, 1, 2, 1][right_edge_offset]])
                        solve_moves2.append([move for k in range(len(solve_moves)) for move in solve_moves[k]])
                        # solving the up side corners
                        solve_moves = []
                        up_corners_in_right_position = []
                        corners_examined = corners[4:]
                        for corner in corners_examined:
                            corner_colors = [rubiks_cube2[int(corner[0][0])][int(corner[0][1])][int(corner[0][2])], \
                                            rubiks_cube2[int(corner[1][0])][int(corner[1][1])][int(corner[1][2])], \
                                            rubiks_cube2[int(corner[2][0])][int(corner[2][1])][int(corner[2][2])]]
                            corner_centres_colors = [rubiks_cube2[int(corner[0][0])][1][1], rubiks_cube2[int(corner[1][0])][1][1], rubiks_cube2[int(corner[2][0])][1][1]]
                            if (corner_colors[0] in corner_centres_colors) and (corner_colors[1] in corner_centres_colors) and (corner_colors[2] in corner_centres_colors):
                                up_corners_in_right_position.append(corner)
                        if len(up_corners_in_right_position) == 0:
                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, ["U", "R", "U'", "L'", "U", "R'", "U'", "L"], False)
                            solve_moves.append(["U", "R", "U'", "L'", "U", "R'", "U'", "L"])
                            for corner in corners_examined:
                                corner_colors = [rubiks_cube2[int(corner[0][0])][int(corner[0][1])][int(corner[0][2])], \
                                                rubiks_cube2[int(corner[1][0])][int(corner[1][1])][int(corner[1][2])], \
                                                rubiks_cube2[int(corner[2][0])][int(corner[2][1])][int(corner[2][2])]]
                                corner_centres_colors = [rubiks_cube2[int(corner[0][0])][1][1], rubiks_cube2[int(corner[1][0])][1][1], rubiks_cube2[int(corner[2][0])][1][1]]
                                if (corner_colors[0] in corner_centres_colors) and (corner_colors[1] in corner_centres_colors) and (corner_colors[2] in corner_centres_colors):
                                    corner_in_right_position = corner
                                    break
                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], ["y"], ["y", "y"], ["y'"]][["322", "302", "300", "320"].index(corner_in_right_position[0])], False)
                            solve_moves.append([[], ["y"], ["y", "y"], ["y'"]][["322", "302", "300", "320"].index(corner_in_right_position[0])])
                        elif len(up_corners_in_right_position) == 1:
                            corner_in_right_position = up_corners_in_right_position[0]
                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], ["y"], ["y", "y"], ["y'"]][["322", "302", "300", "320"].index(corner_in_right_position[0])], False)
                            solve_moves.append([[], ["y"], ["y", "y"], ["y'"]][["322", "302", "300", "320"].index(corner_in_right_position[0])])
                        right_back_corner_centres_colors = [rubiks_cube2[3][1][1], rubiks_cube2[4][1][1], rubiks_cube2[0][1][1]]
                        if len(up_corners_in_right_position) != 4:
                            position_index = [True, False].index((rubiks_cube2[3][2][0] in right_back_corner_centres_colors) and (rubiks_cube2[5][0][0] in right_back_corner_centres_colors) and (rubiks_cube2[2][2][2] in right_back_corner_centres_colors))
                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [["U", "R", "U'", "L'", "U", "R'", "U'", "L"], ["L'", "U", "R", "U'", "L", "U", "R'", "U'"]][position_index], False)
                            solve_moves.append([["U", "R", "U'", "L'", "U", "R'", "U'", "L"], ["L'", "U", "R", "U'", "L", "U", "R'", "U'"]][position_index])
                        for k in range(4):
                            orientation_index = [rubiks_cube2[3][2][2], rubiks_cube2[5][0][2], rubiks_cube2[4][2][0]].index(final_solved_color)
                            rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], 4 * ["R'", "D'", "R", "D"], 2 * ["R'", "D'", "R", "D"]][orientation_index] + ["U'"], False)
                            solve_moves.append([[], 4 * ["R'", "D'", "R", "D"], 2 * ["R'", "D'", "R", "D"]][orientation_index] + ["U'"])
                        up_side_offset = middle_centres.index(rubiks_cube2[5][1][1]) - middle_centres.index(rubiks_cube2[5][0][1])
                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [[], ["U"], ["U", "U"], ["U'"]][up_side_offset], False)
                        solve_moves.append([[], ["U"], ["U", "U"], ["U'"]][up_side_offset])
                        solve_moves2.append([move for k in range(len(solve_moves)) for move in solve_moves[k]])
                        # write beginner solution
                        if self.cube_is_solved(rubiks_cube2):
                            self.down_area_background.delete("all")
                            solving_notes = ["Solving {} cross".format(self.cube_colors[["b", "y", "o", "w", "r", "g"].index(initial_solved_color)]), \
                                            "Solving down corners", "Solving middle edges", \
                                            "Solving {} cross".format(self.cube_colors[["b", "y", "o", "w", "r", "g"].index(final_solved_color)]), \
                                            "Solving up corners"]
                            row_chars = 50
                            line_offset = 0
                            for k in range(len(solve_moves2)):
                                solve_moves2[k] = self.improve_moves_sequence(solve_moves2[k])
                                self.down_area_background.create_text(10, 40 + 15 * (k + line_offset), text = solving_notes[k] + " ({} moves):".format(len(solve_moves2[k])), font = "Arial 10 bold", fill = "purple", anchor = tk.NW)
                                for index1 in range(len(solve_moves2[k]) // row_chars + 1):
                                    index2 = [len(solve_moves2[k]), row_chars * index1 + row_chars][[True, False].index(len(solve_moves2[k]) // row_chars == 0)]
                                    self.down_area_background.create_text(250, 40 + 15 * (k + index1 + line_offset), text = solve_moves2[k][(row_chars * index1) : index2], font = "Arial 10 italic bold", fill = "darkblue", anchor = tk.NW)
                                if len(solve_moves2[k]) // row_chars != 0:
                                    line_offset += 1
                            self.auto_solve_moves_seq = solve_moves2[0] + solve_moves2[1] + solve_moves2[2] + solve_moves2[3] + solve_moves2[4]
                        else:
                            raise
                    elif solve_method_choose in ["CFOP", "Kociemba"]:
                        solve_moves = []
                        centres = [side[1][1] for side in self.rubiks_cube]
                        rubiks_cube2 = self.make_moves_sequence(self.rubiks_cube, [["x"], [], ["z'"], ["x", "x"], ["z"], ["x'"]][centres.index("w")], False)
                        solve_moves.append(["x", "", "z'", "x2", "z", "x'"][centres.index("w")])
                        centres = [side[1][1] for side in rubiks_cube2]
                        rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [["y'"], [], [], [], ["y", "y"], ["y"]][centres.index("b")], False)
                        solve_moves.append(["y'", "", "", "", "y2", "y"][centres.index("b")])
                        cube_colors = self.get_colors_rubik_solver_library(rubiks_cube2)
                        solve_moves = solve_moves + utils.solve(cube_colors, solve_method_choose)
                        solve_moves = [[str(move), str(move).lower()][[True, False][str(move)[0] not in ["X", "Y", "Z"]]] for move in solve_moves if move != ""]
                        solve_moves = self.improve_moves_sequence(solve_moves)
                        if solve_method_choose == "CFOP":
                            rubiks_cube2 = self.copy_cube(self.rubiks_cube)
                            solve_moves2 = [[], [], [], []]
                            CFOP_stage = 0
                            for move in solve_moves:
                                # white Cross check
                                white_Cross_pieces_solved = [rubiks_cube2[1][1][1] == "w", rubiks_cube2[1][2][1] == "w", rubiks_cube2[1][1][0] == "w", rubiks_cube2[1][0][1] == "w", rubiks_cube2[1][1][2] == "w", \
                                                            rubiks_cube2[5][1][1] == rubiks_cube2[5][2][1], rubiks_cube2[2][1][1] == rubiks_cube2[2][1][0], rubiks_cube2[0][1][1] == rubiks_cube2[0][0][1], rubiks_cube2[4][1][1] == rubiks_cube2[4][1][2]]
                                solved_Cross = white_Cross_pieces_solved.count(True) == len(white_Cross_pieces_solved)
                                # F2L check
                                F2L_pieces_solved = [[rubiks_cube2[5][1][0], rubiks_cube2[5][2][0], rubiks_cube2[5][1][2], rubiks_cube2[5][2][2]].count(rubiks_cube2[5][1][1]) == 4, \
                                                    [rubiks_cube2[4][2][1], rubiks_cube2[4][2][2], rubiks_cube2[4][0][1], rubiks_cube2[4][0][2]].count(rubiks_cube2[4][1][1]) == 4, \
                                                    [rubiks_cube2[0][1][2], rubiks_cube2[0][0][2], rubiks_cube2[0][1][0], rubiks_cube2[0][0][0]].count(rubiks_cube2[0][1][1]) == 4, \
                                                    [rubiks_cube2[2][0][1], rubiks_cube2[2][0][0], rubiks_cube2[2][2][1], rubiks_cube2[2][2][0]].count(rubiks_cube2[2][1][1]) == 4]
                                solved_F2L = solved_Cross and F2L_pieces_solved.count(True) == len(F2L_pieces_solved)
                                # OLL check
                                OLL_pieces_solved = [rubiks_cube2[3][i][j] for j in range(3) for i in range(3)]
                                solved_OLL = solved_F2L and OLL_pieces_solved.count("y") == len(OLL_pieces_solved)
                                CFOP_stages_check = [solved_Cross, solved_F2L, solved_OLL]
                                if CFOP_stages_check.count(True) > CFOP_stage:
                                    CFOP_stage = CFOP_stages_check.count(True)
                                    solve_moves2[CFOP_stage].append(move)
                                else:
                                    solve_moves2[CFOP_stage].append(move)
                                rubiks_cube2 = self.make_moves_sequence(rubiks_cube2, [move], False)
                        elif solve_method_choose == "Kociemba":
                            rubiks_cube2 = self.make_moves_sequence(self.rubiks_cube, solve_moves, False)
                        # write CFOP and Kociemba solutions
                        if self.cube_is_solved(rubiks_cube2):
                            self.down_area_background.delete("all")
                            if solve_method_choose == "CFOP":
                                solving_notes = ["Cross - white cross", "F2L - First 2 Layers", "OLL - Orient Last Layer", "PLL - Permute Last Layer"]
                                row_chars = 30
                                line_offset = 0
                                for k in range(len(solve_moves2)):
                                    solve_moves2[k] = self.improve_moves_sequence(solve_moves2[k])
                                    self.down_area_background.create_text(10, 40 + 15 * (k + line_offset), text = solving_notes[k] + " ({} moves):".format(len(solve_moves2[k])), font = "Arial 10 bold", fill = "purple", anchor = tk.NW)
                                    for index1 in range(len(solve_moves2[k]) // row_chars + 1):
                                        index2 = [len(solve_moves2[k]), row_chars * index1 + row_chars][[True, False].index(len(solve_moves2[k]) // row_chars == 0)]
                                        self.down_area_background.create_text(270, 40 + 15 * (k + index1 + line_offset), text = solve_moves2[k][(row_chars * index1) : index2], font = "Arial 10 italic bold", fill = "darkblue", anchor = tk.NW)
                                    if len(solve_moves2[k]) // row_chars != 0:
                                        line_offset += 1
                            if solve_method_choose == "Kociemba":
                                self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2, text = solve_moves, font = "Arial 20 italic bold", fill = "darkblue")
                            self.auto_solve_moves_seq = solve_moves[:]
                        else:
                            raise
                    # write scramble moves and show solution
                    self.down_area_background.create_text(self.down_area_background_width / 2, 20, text = f"{solve_method_choose} solve ({len(self.auto_solve_moves_seq)} moves in total):", font = "Calibri 18 bold", fill = "black")
                    self.down_area_background.create_text(10, self.down_area_background_height - 23, text = "Scramble:", font = "Arial 8 bold", fill = "black", anchor = tk.NW)
                    if self.previous_game_state in ["moves_scramble", "self_solve"]:
                        row_chars = 50
                        for index1 in range(len(self.random_scramble_moves_seq) // row_chars + 1):
                            index2 = [len(self.random_scramble_moves_seq), row_chars * index1 + row_chars][[True, False].index(len(self.random_scramble_moves_seq) // row_chars == 0)]
                            self.down_area_background.create_text(80, self.down_area_background_height - 23 + 10 * index1, text = self.random_scramble_moves_seq[(row_chars * index1) : index2], font = "Arial 8 italic bold", fill = "black", anchor = tk.NW)
                    elif self.previous_game_state == "draw_scramble":
                        self.down_area_background.create_text(80, self.down_area_background_height - 23, text = "You can see the scrambled cube pattern enabling the cube graphics option \"scramble pattern\".", font = "Arial 8 italic bold", fill = "black", anchor = tk.NW)
                    self.same_scramble_cube_button = menu_button(self.down_area_background, "same scramble", "Arial 10 bold", "red", "yellow", self.down_area_background_width - 120, 20, self.same_scramble_cube).button
                    self.go_to_replay_previous_move_button = menu_button(self.down_area_background, "🡄", "Arial 14 bold", "blue", "yellow", 80, 20, lambda event: self.show_previous_next_solve_move("previous", event)).button
                    self.go_to_replay_next_move_button = menu_button(self.down_area_background, "🡆", "Arial 14 bold", "blue", "yellow", 130, 20, lambda event: self.show_previous_next_solve_move("next", event)).button
                    self.go_to_replay_start_button = menu_button(self.down_area_background, "⏮", "Arial 14 bold", "blue", "yellow", 30, 20, lambda event: self.show_previous_next_solve_move("start", event)).button
                    self.go_to_replay_end_button = menu_button(self.down_area_background, "⏭", "Arial 14 bold", "blue", "yellow", 180, 20, lambda event: self.show_previous_next_solve_move("end", event)).button
                    self.make_moves_sequence(self.rubiks_cube, [""] + self.auto_solve_moves_seq, True)
            except:
                self.buttons_bindings_are_activated = True
                self.down_area_background.delete("all")
                self.down_area_background.create_text(self.down_area_background_width / 2, 40, text = "This cube pattern is not valid!", font = "Arial 20 bold", fill = "brown")
                self.down_area_background.create_text(self.down_area_background_width / 2, 90, text = self.wrong_pattern_text, font = "Arial 14 bold", fill = "brown")
                self.down_area_background.create_text(90, self.down_area_background_height - 45, text = "Scramble:", font = "Arial 8 bold", fill = "black", anchor = tk.NW)
                self.down_area_background.create_text(160, self.down_area_background_height - 45, text = "You can see the scrambled cube pattern enabling the cube graphics option \"scramble pattern\".", font = "Arial 8 italic bold", fill = "black", anchor = tk.NW)
                self.same_scramble_cube_button = menu_button(self.down_area_background, "fix scramble", "Arial 10 bold", "red", "yellow", self.down_area_background_width - 200, self.down_area_background_height - 30, self.same_scramble_cube).button
    def cube_is_solved(self, cube):
        try:
            cube = self.make_moves_sequence(cube, [["x"], [], ["z'"], ["x", "x"], ["z"], ["x'"]][[side[1][1] for side in cube].index("y")], False)
            cube = self.make_moves_sequence(cube, [["y", "y"], [], ["y'"], [], ["y"], []][[side[1][1] for side in cube].index("g")], False)
            for i in range(len(cube)):
                for j in range(3):
                    for k in range(3):
                        if cube[i][j][k] != cube[i][1][1] or cube[i][1][1] != ["b", "y", "o", "w", "r", "g"][i]:
                            return False
            if self.game_state in ["self_solve", "auto_solve"]:
                self.play_sound("solved_cube_sound", "sound")
            return True
        except: 
            return False
    def improve_moves_sequence(self, moves_seq):
        if len(moves_seq) == 1:
            return moves_seq
        improved_moves_seq = []
        improvements_done = False
        loops_counter = 0
        while loops_counter != len(moves_seq):
            if improved_moves_seq == []:
                improved_moves_seq.append(moves_seq[loops_counter])
            else:
                moves_k0_k1 = [improved_moves_seq[-1], moves_seq[loops_counter]]
                if moves_k0_k1[0][0] == moves_k0_k1[1][0]:
                    moves_k0_k1_lengths = [len(moves_k0_k1[0]), len(moves_k0_k1[1])]
                    improved_moves_seq.pop()
                    if moves_k0_k1_lengths.count(1) == 2:
                        improved_moves_seq.append(moves_k0_k1[0][0] + "2")
                    elif moves_k0_k1_lengths.count(2) == 1 and moves_k0_k1[moves_k0_k1_lengths.index(2)][1] == "2":
                        improved_moves_seq.append(moves_k0_k1[1 - moves_k0_k1_lengths.index(2)] + "'")
                    elif moves_k0_k1_lengths.count(2) == 2:
                        if moves_k0_k1[0][1] == "'" and moves_k0_k1[1][1] == "'":
                            improved_moves_seq.append(moves_k0_k1[0][0] + "2")
                        elif [moves_k0_k1[0][1], moves_k0_k1[1][1]] in [["'", "2"], ["2", "'"]]:
                            improved_moves_seq.append(moves_k0_k1[0][0])
                    improvements_done = True
                else:
                    improved_moves_seq.append(moves_k0_k1[1])
            loops_counter += 1
        if improvements_done:
            return self.improve_moves_sequence(improved_moves_seq)
        else:
            return improved_moves_seq
    def show_previous_next_solve_move(self, direction, event):
        if self.buttons_bindings_are_activated and self.replay_mode_is_activated and self.game_state in ["self_solve", "auto_solve"]:
            move = ""
            if direction in ["start", "end"]:
                self.rubiks_cube = self.copy_cube([[self.moves_scrambled_rubiks_cube, self.draw_scrambled_rubiks_cube][[True, False].index(self.previous_game_state in ["moves_scramble", "self_solve"])], \
                                                    self.make_moves_sequence(self.rubiks_cube, self.replay_moves_seq[self.moves_pointer:], False)][["start", "end"].index(direction)])
                self.moves_pointer = [0, len(self.replay_moves_seq)][["start", "end"].index(direction)]
            elif direction == "previous" and self.moves_pointer > 0:
                self.moves_pointer -= 1
                move = self.replay_moves_seq[self.moves_pointer]
                move = [move[0] + "'", move[0], move[0] + "2"][[move[0], "'", "2"].index(move[-1])]
            elif direction == "next" and self.moves_pointer < len(self.replay_moves_seq):
                move = self.replay_moves_seq[self.moves_pointer]
                self.moves_pointer += 1
            self.make_moves_sequence(self.rubiks_cube, [move], True)
            self.make_cube_graphics(self.rubiks_cube, move)
    def make_moves_sequence(self, cube, moves_seq, make_changes_to_main_cube, event = None):
        if len(moves_seq) == 0:
            move = ""
        else:
            move = moves_seq[0]
        if ((event == None) or (event != None and self.moves_bindings_are_activated)) and move != "":
            choose_move = ["L", "R", "U", "D", "F", "B", "M", "E", "S", "x", "y", "z"].index(move[0])
            function_choose = [self.left, self.right, self.up, self.down, self.front, self.back, self.midM, self.midE, self.midS, self.rotx, self.roty, self.rotz][choose_move]
            for k in range([1, 2, 3][[move[0], "2", "'"].index(move[-1])]):
                cube = function_choose(cube)
            if make_changes_to_main_cube:
                self.play_sound("make_move_sound", "sound")
        if make_changes_to_main_cube:
            self.rubiks_cube = cube
            if event == None and not self.replay_mode_is_activated:
                self.buttons_bindings_are_activated = False
                self.moves_bindings_are_activated = False
                if len(moves_seq) != 0:
                    self.cube_background.after(int(1000 * self.moves_speed), lambda: self.make_moves_sequence(self.rubiks_cube, moves_seq[1:], True))
                elif len(moves_seq) == 0:
                    self.buttons_bindings_are_activated = True
                    if self.game_state == "moves_scramble":
                        self.moves_scrambled_rubiks_cube = self.copy_cube(self.rubiks_cube)
                        self.moves_bindings_are_activated = True
                        if len(self.random_scramble_moves_seq) == self.max_scramble_moves:
                            self.moves_bindings_are_activated = False
                    elif self.game_state == "auto_solve" and not self.replay_mode_is_activated:
                        self.replay_moves_seq = self.auto_solve_moves_seq
                        self.moves_pointer = len(self.replay_moves_seq)
                        self.replay_mode_is_activated = True
                        self.moves_bindings_are_activated = False
                self.make_cube_graphics(self.rubiks_cube, move)
            if self.buttons_bindings_are_activated and self.moves_bindings_are_activated and not self.replay_mode_is_activated:
                if self.game_state == "moves_scramble":
                    self.moves_scrambled_rubiks_cube = self.copy_cube(self.rubiks_cube)
                    if move != "":
                        if len(self.random_scramble_moves_seq) != self.max_scramble_moves:
                            self.random_scramble_moves_seq = self.improve_moves_sequence(self.random_scramble_moves_seq + [move])
                        if len(self.random_scramble_moves_seq) == self.max_scramble_moves:
                            self.moves_bindings_are_activated = False
                    self.write_moves_scramble_text()
                    self.make_cube_graphics(self.rubiks_cube, move)
                elif self.game_state == "self_solve":
                    self.self_solve_moves_seq = self.self_solve_moves_seq + [move]
                    self.down_area_background.delete("all")
                    self.down_area_background.create_text(self.down_area_background_width / 2, 20, text = "Self solve ({} moves in total):".format(len(self.self_solve_moves_seq)), font = "Calibri 18 bold", fill = "black")
                    row_chars = 50
                    for index1 in range(len(self.self_solve_moves_seq) // row_chars + 1):
                        index2 = [len(self.self_solve_moves_seq), row_chars * index1 + row_chars][[True, False].index(len(self.self_solve_moves_seq) // row_chars == 0)]
                        self.down_area_background.create_text(self.down_area_background_width / 2, 50 + 15 * index1, text = self.self_solve_moves_seq[(row_chars * index1) : index2], font = "Arial 10 italic bold", fill = "darkblue")
                    if self.cube_is_solved(self.rubiks_cube):
                        self.stop_timer_self_solving = time.time()
                        self.time_self_solving = self.stop_timer_self_solving - self.start_timer_self_solving
                        self.down_area_background.delete("all")
                        self.down_area_background.create_text(20, self.down_area_background_height / 2 - 40, text = self.replay_moves_text, font = "Arial 10 bold", fill = "brown", anchor = tk.NW)
                        self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2 - 40, text = "Congratulations, you solved the cube!!!", font = "Calibri 20 bold", fill = "purple")
                        self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2 - 10, text = "Moves needed: {}".format(len(self.self_solve_moves_seq)), font = "Calibri 20 bold", fill = "purple")
                        self.down_area_background.create_text(self.down_area_background_width / 2, self.down_area_background_height / 2 + 20, text = "Solving time: {} minutes and {} seconds".format(int(self.time_self_solving) // 60, int(self.time_self_solving) % 60), font = "Calibri 20 bold", fill = "purple")
                        self.down_area_background.create_text(10, self.down_area_background_height - 23, text = "Scramble:", font = "Arial 8 bold", fill = "black", anchor = tk.NW)
                        for index1 in range(len(self.random_scramble_moves_seq) // row_chars + 1):
                            index2 = [len(self.random_scramble_moves_seq), row_chars * index1 + row_chars][[True, False].index(len(self.random_scramble_moves_seq) // row_chars == 0)]
                            self.down_area_background.create_text(80, self.down_area_background_height - 23 + 10 * index1, text = self.random_scramble_moves_seq[(row_chars * index1) : index2], font = "Arial 8 italic bold", fill = "black", anchor = tk.NW)
                        self.replay_moves_seq = self.self_solve_moves_seq
                        self.moves_pointer = len(self.replay_moves_seq)
                        self.replay_mode_is_activated = True
                        self.moves_bindings_are_activated = False
                    self.make_cube_graphics(self.rubiks_cube, move)
        else:
            if len(moves_seq) != 0:
                return self.make_moves_sequence(cube, moves_seq[1:], False)
            elif len(moves_seq) == 0:
                return cube
    def change_cube_view(self, cube, move, event):
        try: self.reset_cube_view_button.destroy()
        except AttributeError: pass
        self.reset_cube_view_button = menu_button(self.cube_background, "reset cube view", "Arial 12 bold", "red", "cyan", self.cube_background_width / 2, 18, self.reset_cube_view).button
        self.adjust_cube_view_moves.append(move)
        self.make_cube_graphics(cube, None)
    def reset_cube_view(self, event = None):
        try: self.reset_cube_view_button.destroy()
        except AttributeError: pass
        self.adjust_cube_view_moves = []
        self.make_cube_graphics(self.rubiks_cube, None)
    def draw_cube_side(self, background, tags_are_binded, cube_side_info, cube_face_oriented, borders_width, piece_left_side_length, piece_down_side_length, piece_left_side_angle, piece_down_side_angle, cube_face_down_left_point):
        cf = cube_face_oriented; cfdl = cube_face_down_left_point; ps1 = piece_left_side_length; ps2 = piece_down_side_length; pa1 = math.radians(piece_left_side_angle); pa2 = math.radians(piece_down_side_angle)
        cf_colors = [[(self.cube_colors + ["cyan"])[["b", "y", "o", "w", "r", "g", "c"].index(cf[i][j])] for j in range(3)] for i in range(3)]
        cfdl2 = cfdl; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][0], activefill = self.highlight_cube_piece(cf_colors[2][0]), width = borders_width, outline = "black", tags = f"down_left_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + ps2 * math.cos(pa2), cfdl[1] - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][1], activefill = self.highlight_cube_piece(cf_colors[2][1]), width = borders_width, outline = "black", tags = f"down_middle_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + 2 * ps2 * math.cos(pa2), cfdl[1] - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[2][2], activefill = self.highlight_cube_piece(cf_colors[2][2]), width = borders_width, outline = "black", tags = f"down_right_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1), cfdl[1] - ps1 * math.sin(pa1)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][0], activefill = self.highlight_cube_piece(cf_colors[1][0]), width = borders_width, outline = "black", tags = f"left_middle_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1) + ps2 * math.cos(pa2), cfdl[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][1], activefill = self.highlight_cube_piece(cf_colors[1][1]), width = borders_width, outline = "black", tags = f"centre_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), cfdl[1] - ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[1][2], activefill = self.highlight_cube_piece(cf_colors[1][2]), width = borders_width, outline = "black", tags = f"right_middle_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1), cfdl[1] - 2 * ps1 * math.sin(pa1)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][0], activefill = self.highlight_cube_piece(cf_colors[0][0]), width = borders_width, outline = "black", tags = f"up_left_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1) + ps2 * math.cos(pa2), cfdl[1] - 2 * ps1 * math.sin(pa1) - ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][1], activefill = self.highlight_cube_piece(cf_colors[0][1]), width = borders_width, outline = "black", tags = f"up_middle_piece_{cube_side_info}")
        cfdl2 = [cfdl[0] + 2 * ps1 * math.cos(pa1) + 2 * ps2 * math.cos(pa2), cfdl[1] - 2 * ps1 * math.sin(pa1) - 2 * ps2 * math.sin(pa2)]; background.create_polygon([cfdl2[0], cfdl2[1], cfdl2[0] + ps2 * math.cos(pa2), cfdl2[1] - ps2 * math.sin(pa2), cfdl2[0] + ps2 * math.cos(pa2) + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1) - ps2 * math.sin(pa2), cfdl2[0] + ps1 * math.cos(pa1), cfdl2[1] - ps1 * math.sin(pa1)], fill = cf_colors[0][2], activefill = self.highlight_cube_piece(cf_colors[0][2]), width = borders_width, outline = "black", tags = f"up_right_piece_{cube_side_info}")
        background.tag_unbind(f"down_left_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"down_middle_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"down_right_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"left_middle_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"centre_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"right_middle_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"up_left_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"up_middle_piece_{cube_side_info}", "<Button-1>")
        background.tag_unbind(f"up_right_piece_{cube_side_info}", "<Button-1>")
        if self.game_state == "draw_scramble" and tags_are_binded:
            background.tag_bind(f"down_left_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}20", event))
            background.tag_bind(f"down_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}21", event))
            background.tag_bind(f"down_right_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}22", event))
            background.tag_bind(f"left_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}10", event))
            background.tag_bind(f"centre_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}11", event))
            background.tag_bind(f"right_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}12", event))
            background.tag_bind(f"up_left_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}00", event))
            background.tag_bind(f"up_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}01", event))
            background.tag_bind(f"up_right_piece_{cube_side_info}", "<Button-1>", lambda event: self.draw_scramble_piece_pressed(background, f"{cube_side_info}02", event))
        elif self.game_state != "draw_scramble" and tags_are_binded:
            background.tag_bind(f"down_left_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}20", event))
            background.tag_bind(f"down_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}21", event))
            background.tag_bind(f"down_right_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}22", event))
            background.tag_bind(f"left_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}10", event))
            background.tag_bind(f"centre_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}11", event))
            background.tag_bind(f"right_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}12", event))
            background.tag_bind(f"up_left_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}00", event))
            background.tag_bind(f"up_middle_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}01", event))
            background.tag_bind(f"up_right_piece_{cube_side_info}", "<Button-1>", lambda event: self.cube_moves_mouse_events(f"{cube_side_info}02", event))
    def draw_scramble_piece_pressed(self, background, cube_side_info, event):
        adjust_cube_view_moves_copy = self.adjust_cube_view_moves[:]
        self.reset_cube_view()
        self.rubiks_cube = self.make_moves_sequence(self.rubiks_cube, adjust_cube_view_moves_copy, False)
        piece = event.widget.find_closest(event.x, event.y)
        background.itemconfigure(piece, fill = self.chosen_draw_color)
        piece_loc_0, piece_loc_1, piece_loc_2 = int(cube_side_info[0]), int(cube_side_info[1]), int(cube_side_info[2])
        if piece_loc_0 == 4 and self.cube_dimensions == "3d":
            piece_loc_1_copy = piece_loc_1
            piece_loc_1 = 2 - piece_loc_2
            piece_loc_2 = piece_loc_1_copy
        self.rubiks_cube[piece_loc_0][piece_loc_1][piece_loc_2] = self.chosen_draw_color[0]
        self.draw_scrambled_rubiks_cube = self.copy_cube(self.rubiks_cube)
        self.play_sound("draw_cube_sound", "sound")
        self.make_cube_graphics(self.rubiks_cube, None)
    def highlight_cube_piece(self, color):
        if self.game_state != "draw_scramble":
            return ["#0000aa", "#cccc00", "#cd8500", "#cccccc", "#aa0000", "#00aa00", "cyan"][(self.cube_colors + ["cyan"]).index(color)]
        else:
            return self.chosen_draw_color
    def make_cube_graphics(self, main_cube, move):
        if self.game_state in ["moves_scramble", "self_solve"] or (self.game_state == "auto_solve" and self.previous_game_state in ["moves_scramble", "self_solve"]):
            scrambled_cube = self.moves_scrambled_rubiks_cube
        elif self.game_state == "draw_scramble" or (self.game_state == "auto_solve" and self.previous_game_state == "draw_scramble"):
            scrambled_cube = self.draw_scrambled_rubiks_cube
        self.cube_background.delete("all")
        rubiks_cube_view = self.make_moves_sequence(main_cube, self.adjust_cube_view_moves, False)
        scrambled_rubiks_cube_view = self.make_moves_sequence(scrambled_cube, self.adjust_cube_view_moves, False)
        if self.cube_dimensions == "3d":
            # for visible_cube
            centre_offset =  3 / 2 * self.sides_distortion * self.piece_side_length / math.sqrt(2)
            self.front_cube_side_centre = [self.visible_cube_centre_x - centre_offset, self.visible_cube_centre_y + centre_offset]
            self.draw_cube_side(self.cube_background, True, "5", rubiks_cube_view[5], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.front_cube_side_centre[0] - 3 * self.piece_side_length / 2, self.front_cube_side_centre[1] + 3 * self.piece_side_length / 2])
            self.draw_cube_side(self.cube_background, True, "3", rubiks_cube_view[3], 5 * self.borders_width, self.piece_side_length * self.sides_distortion, self.piece_side_length, 45, 0, [self.front_cube_side_centre[0] - 3 * self.piece_side_length / 2, self.front_cube_side_centre[1] - 3 * self.piece_side_length / 2])
            self.draw_cube_side(self.cube_background, True, "4", [[rubiks_cube_view[4][2-j][i] for j in range(3)] for i in range(3)], 5 * self.borders_width, self.piece_side_length, self.piece_side_length * self.sides_distortion, 90, 45, [self.front_cube_side_centre[0] + 3 * self.piece_side_length / 2, self.front_cube_side_centre[1] + 3 * self.piece_side_length / 2])
            if self.axis_visibility == "on":
                self.cube_background.create_line(self.front_cube_side_centre[0] - 3 * self.piece_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre[1] - 3 * self.piece_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre[0] - 3 * self.piece_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre[1] - 3 * self.piece_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) - 50, width = 5, fill = "black", activefill = "white")
                self.cube_background.create_text(self.front_cube_side_centre[0] - 3 * self.piece_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)) - 10, self.front_cube_side_centre[1] - 3 * self.piece_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) - 50, text = "z", font = "Times 20 bold", fill = "black", activefill = "purple")
                self.cube_background.create_line(self.front_cube_side_centre[0] + 3 * self.piece_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre[1] + 3 * self.piece_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), self.front_cube_side_centre[0] + 3 * self.piece_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) + 50, self.front_cube_side_centre[1] + 3 * self.piece_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)), width = 5, fill = "black", activefill = "white")
                self.cube_background.create_text(self.front_cube_side_centre[0] + 3 * self.piece_side_length * (1/ 2 + self.sides_distortion / math.sqrt(2)) + 60, self.front_cube_side_centre[1] + 3 * self.piece_side_length * (1/ 2 - self.sides_distortion / math.sqrt(2)) - 5, text = "y", font = "Times 20 bold", fill = "black", activefill = "purple")
                self.cube_background.create_line(self.front_cube_side_centre[0] - 3 * self.piece_side_length / 2, self.front_cube_side_centre[1] + 3 * self.piece_side_length / 2, self.front_cube_side_centre[0] - 3 * self.piece_side_length / 2 - 50 / math.sqrt(2), self.front_cube_side_centre[1] + 3 * self.piece_side_length / 2 + 50 / math.sqrt(2), width = 5, fill = "black", activefill = "white")
                self.cube_background.create_text(self.front_cube_side_centre[0] - 3 * self.piece_side_length / 2 - 50 / math.sqrt(2), self.front_cube_side_centre[1] + 3 * self.piece_side_length / 2 + 50 / math.sqrt(2) + 10, text = "x", font = "Times 20 bold", fill = "black", activefill = "purple")
            # for hidden_layers
            if self.hidden_sides_visibility == "on":
                self.draw_cube_side(self.cube_background, False, "None", [[rubiks_cube_view[0][2-i][j] for j in range(3)] for i in range(3)], 0, self.hidden_side_length, self.hidden_side_length, 90, 0, [self.hidden_cube_centre_x, self.hidden_cube_centre_y])
                self.draw_cube_side(self.cube_background, False, "None", [[rubiks_cube_view[1][i][2-j] for j in range(3)] for i in range(3)], 0, self.hidden_side_length * self.sides_distortion, self.hidden_side_length, 45, 0, [self.hidden_cube_centre_x - 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2), self.hidden_cube_centre_y + 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2)])
                self.draw_cube_side(self.cube_background, False, "None", [[rubiks_cube_view[2][2-j][2-i] for j in range(3)] for i in range(3)], 0, self.hidden_side_length, self.hidden_side_length * self.sides_distortion, 90, 45, [self.hidden_cube_centre_x - 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2), self.hidden_cube_centre_y + 3 * self.hidden_side_length * self.sides_distortion / math.sqrt(2)])
            if self.hidden_sides_visibility == "on" and self.axis_visibility == "on":
                self.cube_background.create_line(self.hidden_cube_centre_x, self.hidden_cube_centre_y, self.hidden_cube_centre_x, self.hidden_cube_centre_y - 3 * self.hidden_side_length - 10, width = 3, fill = "black", activefill = "white")
                self.cube_background.create_text(self.hidden_cube_centre_x - 10, self.hidden_cube_centre_y - 3 * self.hidden_side_length - 10, text = "z", font = "Times 15 bold", fill = "black", activefill = "purple")
                self.cube_background.create_line(self.hidden_cube_centre_x, self.hidden_cube_centre_y, self.hidden_cube_centre_x + 3 * self.hidden_side_length + 10, self.hidden_cube_centre_y, width = 3, fill = "black", activefill = "white")
                self.cube_background.create_text(self.hidden_cube_centre_x + 3 * self.hidden_side_length + 20, self.hidden_cube_centre_y - 5, text = "y", font = "Times 15 bold", fill = "black", activefill = "purple")
                self.cube_background.create_line(self.hidden_cube_centre_x, self.hidden_cube_centre_y, self.hidden_cube_centre_x - (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2), self.hidden_cube_centre_y + (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2), width = 3, fill = "black", activefill = "white")
                self.cube_background.create_text(self.hidden_cube_centre_x - (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2), self.hidden_cube_centre_y + (3 * self.hidden_side_length * self.sides_distortion + 10) / math.sqrt(2) + 10, text = "x", font = "Times 15 bold", fill = "black", activefill = "purple")
                self.cube_background.create_line(self.hidden_cube_centre_x, self.hidden_cube_centre_y, self.hidden_cube_centre_x, self.hidden_cube_centre_y, width = 5, fill = "black", capstyle = "round", activefill = "white")
        elif self.cube_dimensions == "2d":
            gap = 10
            self.draw_cube_side(self.cube_background, True, "0", rubiks_cube_view[0], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.visible_cube_centre_x, self.visible_cube_centre_y - 3 * self.piece_side_length / 2 - gap])
            self.draw_cube_side(self.cube_background, True, "1", rubiks_cube_view[1], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.visible_cube_centre_x - 6 * self.piece_side_length - 2 * gap, self.visible_cube_centre_y + 3 * self.piece_side_length / 2])
            self.draw_cube_side(self.cube_background, True, "2", rubiks_cube_view[2], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.visible_cube_centre_x - 3 * self.piece_side_length - gap, self.visible_cube_centre_y + 3 * self.piece_side_length / 2])
            self.draw_cube_side(self.cube_background, True, "3", rubiks_cube_view[3], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.visible_cube_centre_x, self.visible_cube_centre_y + 3 * self.piece_side_length / 2])
            self.draw_cube_side(self.cube_background, True, "4", rubiks_cube_view[4], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.visible_cube_centre_x + 3 * self.piece_side_length + gap, self.visible_cube_centre_y + 3 * self.piece_side_length / 2])
            self.draw_cube_side(self.cube_background, True, "5", rubiks_cube_view[5], 5 * self.borders_width, self.piece_side_length, self.piece_side_length, 90, 0, [self.visible_cube_centre_x, self.visible_cube_centre_y + 9 * self.piece_side_length / 2 + gap])
        if self.scramble_pattern_visibility == "on":
            gap = 2
            self.draw_cube_side(self.cube_background, False, "None", scrambled_rubiks_cube_view[0], 1, 15, 15, 90, 0, [self.scrambled_pattern_centre_x, self.scrambled_pattern_centre_y - 3 * 15 / 2 - gap])
            self.draw_cube_side(self.cube_background, False, "None", scrambled_rubiks_cube_view[1], 1, 15, 15, 90, 0, [self.scrambled_pattern_centre_x - 6 * 15 - 2 * gap, self.scrambled_pattern_centre_y + 3 * 15 / 2])
            self.draw_cube_side(self.cube_background, False, "None", scrambled_rubiks_cube_view[2], 1, 15, 15, 90, 0, [self.scrambled_pattern_centre_x - 3 * 15 - gap, self.scrambled_pattern_centre_y + 3 * 15 / 2])
            self.draw_cube_side(self.cube_background, False, "None", scrambled_rubiks_cube_view[3], 1, 15, 15, 90, 0, [self.scrambled_pattern_centre_x, self.scrambled_pattern_centre_y + 3 * 15 / 2])
            self.draw_cube_side(self.cube_background, False, "None", scrambled_rubiks_cube_view[4], 1, 15, 15, 90, 0, [self.scrambled_pattern_centre_x + 3 * 15 + gap, self.scrambled_pattern_centre_y + 3 * 15 / 2])
            self.draw_cube_side(self.cube_background, False, "None", scrambled_rubiks_cube_view[5], 1, 15, 15, 90, 0, [self.scrambled_pattern_centre_x, self.scrambled_pattern_centre_y + 9 * 15 / 2 + gap])
        if move != None:
            self.cube_background.create_text(self.cube_background_width / 2, self.cube_background_height - 20, text = move, font = "Calibri 20 bold", fill = "black")
        else:
            pass
        if self.cube_is_solved(self.rubiks_cube):
            self.cube_background.create_text(self.cube_background_width - 75, self.cube_background_height - 20, text = "solved", font = "Calibri 25 bold", fill = "green")
        else:
            self.cube_background.create_text(self.cube_background_width - 75, self.cube_background_height - 20, text = "scrambled", font = "Calibri 25 bold", fill = "red")
    def destroy_down_area_buttons(self):
        try: self.clear_cube_draw_button.destroy()
        except AttributeError: pass
        try: self.fill_cube_draw_button.destroy()
        except AttributeError: pass
        try: self.same_scramble_cube_button.destroy()
        except AttributeError: pass
        try: self.self_solve_try_yourself_button.destroy()
        except AttributeError: pass
        try: self.self_solve_try_again_button.destroy()
        except AttributeError: pass
        try:
            self.go_to_replay_previous_move_button.destroy()
            self.go_to_replay_next_move_button.destroy()
            self.go_to_replay_start_button.destroy()
            self.go_to_replay_end_button.destroy()
        except AttributeError: pass

class menu_button():
    def __init__(self, background, button_text, button_font, button_fg, button_bg, button_xcor, button_ycor, button_func):
        self.button = tk.Label(background, text = button_text, font = button_font, fg = button_fg, bg = button_bg)
        self.button.place(x = button_xcor, y = button_ycor, anchor = "center")
        self.button.bind("<Enter>", lambda event, button = self.button: [button.configure(font = "Arial {} bold".format(int(button["font"].split(" ")[1]) + 10)), rubiks_cube_root.play_sound("hover_button_sound", "sound")])
        self.button.bind("<Leave>", lambda event, button = self.button: button.configure(font = button_font))
        self.button.bind("<Button-1>", lambda event: [button_func(event), rubiks_cube_root.play_sound("select_button_sound", "sound")])
class menu_label():
    def __init__(self, background, label_text, label_font, label_fg, label_bg, label_xcor, label_ycor):
        self.label = tk.Label(background, text = label_text, font = label_font, fg = label_fg, bg = label_bg)
        self.label.place(x = label_xcor, y = label_ycor, anchor = "center")

root = tk.Tk()
rubiks_cube_root = rubiks_cube(root)
root.mainloop()