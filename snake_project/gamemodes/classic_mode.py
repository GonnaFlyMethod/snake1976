import os
import random
import threading
import time

from extra.tools.os_initializer import init_os
if init_os() == 'Windows':
    from msvcrt import getch, kbhit
else:
    import curses
    from extra.tools.linux_functions import set_normal_term, set_curses_term
from extra.tools.asker import complex_ask
from extra.tools.key_setup import set_keyboard_keys
from extra.tools.clean_console_command_setter import set_cleaning_command


class ClassicModeGameManager:
    """This class provides methods for implementing the Classic mod."""

    def __init__(self, player_score_instance, game_menu_instance):
        """Setting the keys on the keyboard for windows to control the snake and
        inits os, dict-obj, player score instance and menu instance.
        """
        self.keys = set_keyboard_keys()
        self.UP = [self.keys["UP_1"][0], self.keys["UP_1"][1]]  # w W
        self.DOWN = [self.keys["DOWN_1"][0], self.keys["DOWN_1"][1]]  # s S
        self.LEFT = [self.keys["LEFT_1"][0], self.keys["LEFT_1"][1]]  # a A
        self.RIGHT = [self.keys["RIGHT_1"][0], self.keys["RIGHT_1"][1]]  # d D

        self.RESET = set_cleaning_command()
        self.platform = init_os()
        self.settings_storage = {}
        self.player_score = player_score_instance
        self.menu = game_menu_instance

    def run(self):
        """Method starting the mode automatically."""
        plays_current_game_in_current_gamemode = True

        while plays_current_game_in_current_gamemode:
            wanna_continue_the_current_game = True
            # Survey of the player about the game settings.
            self.settings_storage = complex_ask(self.menu, 1)

            # Setting default settings according to the choice of the player.
            self.set_default_settings()
            while wanna_continue_the_current_game:
                self.initialize_new_player()

                while not self.get_game_over_status():
                    self.draw_whole_field()

                    if self.platform == "Linux":
                        curses.wrapper(self.process_player_input_linux)
                    else:
                        threads = self.create_new_threads()
                        for t in threads:
                            t.start()

                    self.process_hook_logic()

                    if self.get_game_over_status():  # If a player loses...
                        score_of_player = self.get_score()

                        # Recording the results.
                        self.player_score.write_down_player_score(
                            score_of_player,
                        )

                        print('Game Over\nYour Score: ' + str(self.get_score()))
                        print('Time: ' + str(self.get_time()))
                        print('~' * 40)

                        player_resp = self.menu.ask_player_for_further_actions()

                        if player_resp == 1:
                            self.set_default_settings()
                            self.set_game_over_false()
                            break
                        elif player_resp == 2:
                            wanna_continue_the_current_game = False
                            self.set_game_over_false()
                            break
                        elif player_resp == 3:
                            wanna_continue_the_current_game = False
                            plays_current_game_in_current_gamemode = False
                            self.set_game_over_false()
                            break
                        else:
                            exit()

    def initialize_new_player(self):
        """Method sets the initial length of the snake and sets the adding
        bonus for extra speed of the game.
        """
        # Setting the default length of the snake.
        self.snake_segments_coord_x = [self.head_x_coord
        for i in range(self.num_of_snake_segments + 1)]

        offsets_of_the_snake_segment_y = 1
        for i in range(self.num_of_snake_segments + 1):
            self.snake_segments_coord_y.append(self.head_y_coord +
            offsets_of_the_snake_segment_y)

            offsets_of_the_snake_segment_y += 1

        # Setting points for one fruit.
        if self.game_speed == 0.08:
            self.adding_points = 20
        elif self.game_speed == 0.06:
            self.adding_points = 30
        else:
            self.adding_points = 40

    def draw_whole_field(self):
        """Method constantly redraws the playing field."""
        if self.platform == "Linux": set_curses_term()

        # Drawing the upper edges.
        for i in range(self.width + 1):
            print("█", end="")

        print("")

        # Drawing snake's head, fruits, side edges, snake's tail, and a void.
        for i in range(self.height + 1):
            for j in range(self.width + 1):
                if i == self.head_y_coord and j == self.head_x_coord:
                    print("0", end="")

                # Drawing fruit.
                elif i == self.y_coord_of_fruit and j == self.x_coord_of_fruit:
                    print("*", end="")

                # Drawing side edges.
                elif j == 0 or j == self.width:
                    if j == 0:
                        print("█", end="")
                    else:
                        print("█")

                else:
                    # Drawing tail.
                    print_tail = False

                    for k in range(self.num_of_snake_segments):
                        if (self.snake_segments_coord_x[k] == j and
                            self.snake_segments_coord_y[k] == i):
                            print_tail = True
                            print("o", end="")

                    if not print_tail:
                        print(" ", end="")

        # Drawing bottom edges.
        for i in range(self.width + 1):
            print("█", end="",)

        print("")

        # Drawing score&time indicator.
        print(self.centralize_score_n_time + "Score: " + str(self.score) +
            ' | ' + 'Time: ' + str(round(time.time() - self.time)))

        time.sleep(self.game_speed)
        os.system(self.RESET)

    def process_player_input_win(self):
        """Handles pressing keyboard keys on Windows OS.

        Changes the direction of the snake (depends on the key that player
        presses).
        """
        time.sleep(0.085)
        if kbhit():
            key = ord(getch())
            if key in self.UP:
                self.direction = 'UP'
            elif key in self.DOWN:
                self.direction = 'DOWN'
            elif key in self.LEFT:
                self.direction = 'LEFT'
            elif key in self.RIGHT:
                self.direction = 'RIGHT'

    def process_player_input_linux(self, win):
        """Handles pressing keyboard keys on Linux OS.

        Changes the direction of the snake (depends on the key that player
        presses).
        """
        curses.use_default_colors()
        win.nodelay(True)
        key = ""
        win.clear()
        try:
            key = win.getkey()
            win.clear()
        except Exception:
            # No input
            pass

        if key == "w" or key == "W":
            self.direction = "UP"
        elif key == "a" or key == "A":
            self.direction = "LEFT"
        elif key == "s" or key == "S":
            self.direction = "DOWN"
        elif key == "d" or key == "D":
            self.direction = "RIGHT"

    def process_hook_logic(self):
        """Handles logic that is connected with snake.

        Processes logic related to the tail of the snake, direction of the
        snake, logic for eating fruits,	touching the snake with walls, cases in
        which self.game_over = True.
        """
        # Snake's tail logic.
        self.snake_segments_coord_x.append(0)
        self.snake_segments_coord_y.append(0)

        prev_coord_x = self.snake_segments_coord_x[0]
        prev_coord_y = self.snake_segments_coord_y[0]

        prev_coord2_x = 0
        prev_coord2_y = 0

        self.snake_segments_coord_x[0] = self.head_x_coord
        self.snake_segments_coord_y[0] = self.head_y_coord

        for i in range(1, self.num_of_snake_segments):
            prev_coord2_x = self.snake_segments_coord_x[i]
            prev_coord2_y = self.snake_segments_coord_y[i]

            self.snake_segments_coord_x[i] = prev_coord_x
            self.snake_segments_coord_y[i] = prev_coord_y

            prev_coord_x = prev_coord2_x
            prev_coord_y = prev_coord2_y

        # The logic related to the direction of the snake.
        if self.direction == 'LEFT':
            self.head_x_coord -= 1
        elif self.direction == 'RIGHT':
            self.head_x_coord += 1
        elif self.direction == 'UP':
            self.head_y_coord -= 1
        else:
            self.head_y_coord += 1

        # Snake and walls logic.
        if self.snake_and_walls == 'can crawl through the walls':
            if self.head_x_coord > self.width - 1:
                self.head_x_coord = 1
            elif self.head_x_coord == 0:
                self.head_x_coord = self.width - 1

            if self.head_y_coord > self.height:
                self.head_y_coord = 0
            elif self.head_y_coord < 0:
                self.head_y_coord = self.height
        else:
            if self.head_x_coord > self.width - 1 or self.head_x_coord == 0:
                self.game_over = True
                if self.platform == "Linux": set_normal_term()

            elif self.head_y_coord > self.height or self.head_y_coord < 0:
                self.game_over = True
                if self.platform == "Linux": set_normal_term()

        # Cases for self.game_over = True.
        for i in range(self.num_of_snake_segments):

            if (self.snake_segments_coord_x[i] == self.head_x_coord and
                self.snake_segments_coord_y[i] == self.head_y_coord):
                self.game_over = True
                if self.platform == "Linux": set_normal_term()

        # Eating fruit logic.
        if (self.head_x_coord == self.x_coord_of_fruit and
            self.head_y_coord == self.y_coord_of_fruit):

            self.score += self.adding_points

            self.x_coord_of_fruit = random.randint(1, self.width - 1)
            self.y_coord_of_fruit = random.randint(1, self.height - 1)

            self.num_of_snake_segments += 1

    def get_game_over_status(self):
        return self.game_over

    def set_game_over_false(self):
        self.game_over = False

    def set_default_settings(self):
        """Sets attribute settings before the beginning of the game itself."""
        # Basic settings.
        self.width = self.settings_storage['width']
        self.height = self.settings_storage['height']
        self.snake_and_walls = self.settings_storage['walls']
        self.x_coord_of_fruit = random.randint(1, self.width - 1)
        self.y_coord_of_fruit = random.randint(1, self.height - 1)
        self.time = time.time()
        self.centralize_score_n_time = " " * (int(self.width / 2) - 9)
        self.game_speed = self.settings_storage['speed']
        self.score = 0
        self.game_over = False

        # Snake's settings.
        self.head_x_coord = (self.width / 2)
        self.head_y_coord = (self.height / 2) + 1
        self.direction = 'UP'
        self.num_of_snake_segments = self.settings_storage['length']
        self.snake_segments_coord_x = []
        self.snake_segments_coord_y = []

    def get_score(self) -> int:
        return self.score

    def get_time(self) -> int:
        return round(time.time() - self.time)

    def create_new_threads(self) -> list:
        threading_list = []
        t1 = threading.Thread(target=lambda: self.process_player_input_win())
        threading_list.extend([t1, ])
        return threading_list
