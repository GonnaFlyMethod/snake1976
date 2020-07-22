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


class SurvivalModeGameManager:
    """This class provides methods for implementing the Survival mode."""

    def __init__(self, player_score_instance, game_menu_instance):
        """Setting the keys on the keyboard to control the snakes and inits
        os, dict-obj, player score instance and menu instance.

        Note:
            _1 means something related to the 1-st snake,
            _2 means something related to the 2-nd snake.
        """
        self.keys = set_keyboard_keys()
        self.UP_1 = [self.keys["UP_1"][0], self.keys["UP_1"][1]]  # w W
        self.DOWN_1 = [self.keys["DOWN_1"][0], self.keys["DOWN_1"][1]]  # s S
        self.LEFT_1 = [self.keys["LEFT_1"][0], self.keys["LEFT_1"][1]]  # a A
        self.RIGHT_1 = [self.keys["RIGHT_1"][0], self.keys["RIGHT_1"][1]]  # d D

        self.UP_2 = self.keys["UP_2"]  # ^
        self.DOWN_2 = self.keys["DOWN_2"]  # v
        self.LEFT_2 = self.keys["LEFT_2"]  # <
        self.RIGHT_2 = self.keys["RIGHT_2"]  # >
        self.keys_player_2 = [self.UP_2, self.DOWN_2, self.LEFT_2, self.RIGHT_2]

        self.RESET = set_cleaning_command()
        self.platform = init_os()
        self.settings_storage = {}  # Dict for set_default_settings method.
        self.player_score = player_score_instance
        self.menu = game_menu_instance

    def run(self):
        """Method starting the mode automatically."""
        plays_current_game_in_current_gamemode = True

        while plays_current_game_in_current_gamemode:
            wanna_continue_the_current_game = True

            # Survey of the player about the game settings.
            self.settings_storage = complex_ask(self.menu, 2)
            # Setting default settings according to the choice of the player.
            self.set_default_settings()
            while wanna_continue_the_current_game:
                self.initialize_new_players()

                while (not self.get_game_over_status_player_1() and not
                    self.get_game_over_status_player_2()):
                    self.draw_whole_field()

                    if self.platform == "Linux":
                        for i in range(2):
                            curses.wrapper(self.process_players_input_linux)
                    else:
                        threads = self.create_new_threads()
                        for t in threads:
                            t.start()

                    self.process_hook_logic_for_player_1()
                    self.process_hook_logic_for_player_2()
                    self.process_common_logic_of_2_snakes()

                    # If player1 or player2 lose...
                    if (self.get_game_over_status_player_1() or
                        self.get_game_over_status_player_2()):
                        winner = self.determine_who_won()

                        if winner == 1:
                            print("Player 1 won the game!")
                        elif winner == 2:
                            print("Player 2 won the game!")
                        else:
                            print('Draw!')

                        print('Time: ' + str(self.get_time()))
                        print("P1: " + self.get_score_of_players()[0])
                        print("P2: " + self.get_score_of_players()[1])
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

    def initialize_new_players(self):
        """Method sets the initial length of snakes and sets the adding
        bonus for extra speed of the game.
        """
        # Setting the default length of the 1-st snake.
        self.snake_segments_coord_x_1 = [self.head_x_coord_1
        for i in range(self.num_of_snake_segments_1 + 1)]

        offsets_of_the_snake_segment_y_1 = 1
        for i in range(self.num_of_snake_segments_1 + 1):
            self.snake_segments_coord_y_1.append(self.head_y_coord_1 +
            offsets_of_the_snake_segment_y_1)
            offsets_of_the_snake_segment_y_1 += 1

        # Setting the default length of the 2-d snake.
        self.snake_segments_coord_x_2 = [self.head_x_coord_2
        for i in range(self.num_of_snake_segments_2 + 1)]

        offsets_of_the_snake_segment_y_2 = 1
        for i in range(self.num_of_snake_segments_2 + 1):
            self.snake_segments_coord_y_2.append(self.head_y_coord_2 +
            offsets_of_the_snake_segment_y_2)

            offsets_of_the_snake_segment_y_2 += 1

        # Setting points for one fruit.
        if self.game_speed == 0.08:
            self.adding_points = 20
        elif self.game_speed == 0.06:
            self.adding_points = 30
        else:
            self.adding_points = 40

    def draw_whole_field(self):
        """Method constantly redraws the playing field, snakes, fruit and
        score&time indicator
        """
        if self.platform == "Linux": set_curses_term()

        # Drawing the upper edges.
        for i in range(self.width + 1):
            print("█", end="")

        print(" ")
        # Drawing snakes' head, fruit, side edges, snakes' tails, and a void.
        for i in range(self.height + 1):
            for j in range(self.width + 1):
                # Drawing 1-st snake's head.
                if i == self.head_y_coord_1 and j == self.head_x_coord_1:
                    print("0", end="")

                # Drawing 2-nd snake's head.
                elif i == self.head_y_coord_2 and j == self.head_x_coord_2:
                    print("@", end="")

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
                    # Drawing tail of the 1-st snake.
                    print_tail_1 = False
                    for k in range(self.num_of_snake_segments_1):
                        if (self.snake_segments_coord_x_1[k] == j and
                            self.snake_segments_coord_y_1[k] == i):
                            print_tail_1 = True
                            print("o", end="")

                    # Drawing tail of the 2-nd snake.
                    print_tail_2 = False
                    for t in range(self.num_of_snake_segments_2):
                        if (self.snake_segments_coord_x_2[t] == j and
                            self.snake_segments_coord_y_2[t] == i):
                            print_tail_2 = True
                            print("o", end="")

                    if not print_tail_1 and not print_tail_2:
                        print(" ", end="")

        # Drawing the bottom edges.
        for i in range(self.width + 1):
            print("█", end="")

        print(" ")
        # Drawing score&time indicator.
        print(self.centralize_score_n_time + "P1: " + str(self.score_1) +
            " | " + "Time: " + str(round(time.time() - self.time)) + " | " +
            "P2: " + str(self.score_2))

        time.sleep(self.game_speed)
        os.system(self.RESET)

    def process_players_input_win(self):
        """Handles pressing keyboard keys on Windows OS.

        Changes the direction of the snakes (depends on the keys that players
        press).
        """
        time.sleep(0.085)
        if kbhit():
            key = ord(getch())
            if key not in self.keys_player_2:
                if key in self.UP_1:
                    self.direction_1 = 'UP'
                elif key in self.DOWN_1:
                    self.direction_1 = 'DOWN'
                elif key in self.LEFT_1:
                    self.direction_1 = 'LEFT'
                elif key in self.RIGHT_1:
                    self.direction_1 = 'RIGHT'
            else:
                if key == self.UP_2:
                    self.direction_2 = 'UP'
                elif key == self.DOWN_2:
                    self.direction_2 = 'DOWN'
                elif key == self.LEFT_2:
                    self.direction_2 = 'LEFT'
                elif key == self.RIGHT_2:
                    self.direction_2 = 'RIGHT'

    def process_players_input_linux(self, win):
        """Handles pressing keyboard keys on Linux OS.

        Changes the direction of the snake (depends on the key that player
        presses).
        """
        win.clear()
        curses.use_default_colors()
        win.nodelay(True)
        key = ""
        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.keypad(5)
        stdscr.refresh()
        win.clear()
        key = stdscr.getch()
        win.clear()

        if key not in self.keys_player_2:
            if key in self.UP_1:
                self.direction_1 = "UP"
            elif key in self.LEFT_1:
                self.direction_1 = "LEFT"
            elif key in self.DOWN_1:
                self.direction_1 = "DOWN"
            elif key in self.RIGHT_1:
                self.direction_1 = "RIGHT"
        else:
            if key == self.UP_2:
                self.direction_2 = "UP"
            elif key == self.LEFT_2:
                self.direction_2 = "LEFT"
            elif key == self.DOWN_2:
                self.direction_2 = "DOWN"
            elif key == self.RIGHT_2:
                self.direction_2 = "RIGHT"

    def process_hook_logic_for_player_1(self):
        """Handles the 1-st snake logic.

        Handles logic related to the tail of the 1-st snake, direction of
        the	1-st snake, logic for eating fruits(the 1-st snake), cases in which
        self.game_over_1 = True for the 1-st snake.

        Note:
            snake1 = the 1-st snake.
        """
        # Snake1's tail logic.
        self.snake_segments_coord_x_1.append(0)
        self.snake_segments_coord_y_1.append(0)

        prev_coord_x_1 = self.snake_segments_coord_x_1[0]
        prev_coord_y_1 = self.snake_segments_coord_y_1[0]

        prev_coord2_x_1 = 0
        prev_coord2_y_1 = 0

        self.snake_segments_coord_x_1[0] = self.head_x_coord_1
        self.snake_segments_coord_y_1[0] = self.head_y_coord_1

        for i in range(1, self.num_of_snake_segments_1):
            prev_coord2_x_1 = self.snake_segments_coord_x_1[i]
            prev_coord2_y_1 = self.snake_segments_coord_y_1[i]

            self.snake_segments_coord_x_1[i] = prev_coord_x_1
            self.snake_segments_coord_y_1[i] = prev_coord_y_1

            prev_coord_x_1 = prev_coord2_x_1
            prev_coord_y_1 = prev_coord2_y_1

        # The logic related to the direction of the snake1.
        if self.direction_1 == 'LEFT':
            self.head_x_coord_1 -= 1
        elif self.direction_1 == 'RIGHT':
            self.head_x_coord_1 += 1

        elif self.direction_1 == 'UP':
            self.head_y_coord_1 -= 1
        else:
            self.head_y_coord_1 += 1

        # Snake1 and walls logic.
        if self.snake_and_walls == 'can crawl through the walls':
            if self.head_x_coord_1 > self.width - 1:
                self.head_x_coord_1 = 1
            elif self.head_x_coord_1 == 0:
                self.head_x_coord_1 = self.width - 1

            if self.head_y_coord_1 > self.height:
                self.head_y_coord_1 = 0
            elif self.head_y_coord_1 < 0:
                self.head_y_coord_1 = self.height

        else:
            if (self.head_x_coord_1 > self.width - 1 or
                self.head_x_coord_1 == 0):
                self.game_over_1 = True
                if self.platform == "Linux": set_normal_term()

            elif (self.head_y_coord_1 > self.height or
                self.head_y_coord_1 < 0):
                self.game_over_1 = True
                if self.platform == "Linux": set_normal_term()

        # Cases for self.game_over_1 = True (snake1).
        for i in range(self.num_of_snake_segments_1):
            if (self.snake_segments_coord_x_1[i] == self.head_x_coord_1 and
                self.snake_segments_coord_y_1[i] == self.head_y_coord_1):
                self.game_over_1 = True
                if self.platform == "Linux": set_normal_term()

        # Eating fruit logic (snake1)
        if (self.head_x_coord_1 == self.x_coord_of_fruit and
            self.head_y_coord_1 == self.y_coord_of_fruit):

            self.x_coord_of_fruit = random.randint(1, self.width - 1)
            self.y_coord_of_fruit = random.randint(1, self.height - 1)

            self.num_of_snake_segments_1 += 1
            self.score_1 += self.adding_points

    def process_hook_logic_for_player_2(self):
        """Handles the 2-nd Snake logic.

        Handles logic related to the tail of the snake2, direction of
        the 2-nd snake, logic for eating fruits(the 2-nd snake), cases in which
        self.game_over_2 = True for the 2-nd snake.

        Note:
            snake2 == the 2-nd snake.
        """
        # Snake2's tail logic.
        self.snake_segments_coord_x_2.append(0)
        self.snake_segments_coord_y_2.append(0)

        prev_coord_x_2 = self.snake_segments_coord_x_2[0]
        prev_coord_y_2 = self.snake_segments_coord_y_2[0]

        prev_coord2_x_2 = 0
        prev_coord2_y_2 = 0

        self.snake_segments_coord_x_2[0] = self.head_x_coord_2
        self.snake_segments_coord_y_2[0] = self.head_y_coord_2

        for i in range(1, self.num_of_snake_segments_2):
            prev_coord2_x_2 = self.snake_segments_coord_x_2[i]
            prev_coord2_y_2 = self.snake_segments_coord_y_2[i]

            self.snake_segments_coord_x_2[i] = prev_coord_x_2
            self.snake_segments_coord_y_2[i] = prev_coord_y_2

            prev_coord_x_2 = prev_coord2_x_2
            prev_coord_y_2 = prev_coord2_y_2

        # The logic related to the direction of the snake2.
        if self.direction_2 == 'LEFT':
            self.head_x_coord_2 -= 1
        elif self.direction_2 == 'RIGHT':
            self.head_x_coord_2 += 1

        elif self.direction_2 == 'UP':
            self.head_y_coord_2 -= 1
        else:
            self.head_y_coord_2 += 1

        # Snake2 and walls logic.
        if self.snake_and_walls == 'can crawl through the walls':
            if self.head_x_coord_2 > self.width - 1:
                self.head_x_coord_2 = 1
            elif self.head_x_coord_2 == 0:
                self.head_x_coord_2 = self.width - 1

            if self.head_y_coord_2 > self.height:
                self.head_y_coord_2 = 0
            elif self.head_y_coord_2 < 0:
                self.head_y_coord_2 = self.height

        else:
            if self.head_x_coord_2 > self.width - 1 or self.head_x_coord_2 == 0:
                self.game_over_2 = True
            elif self.head_y_coord_2 > self.height or self.head_y_coord_2 < 0:
                self.game_over_2 = True
                if self.platform == "Linux": set_normal_term()

        # Cases for self.game_over_2 = True (snake2).
        for i in range(self.num_of_snake_segments_2):
            if (self.snake_segments_coord_x_2[i] == self.head_x_coord_2 and
                self.snake_segments_coord_y_2[i] == self.head_y_coord_2):
                self.game_over_2 = True
                if self.platform == "Linux": set_normal_term()

        # Eating fruit logic (snake2).
        if (self.head_x_coord_2 == self.x_coord_of_fruit and
            self.head_y_coord_2 == self.y_coord_of_fruit):

            self.x_coord_of_fruit = random.randint(1, self.width - 1)
            self.y_coord_of_fruit = random.randint(1, self.height - 1)

            self.num_of_snake_segments_2 += 1
            self.score_2 += self.adding_points

    def process_common_logic_of_2_snakes(self):
        """Method adds some logic because of increased number of snakes in one
        game field.

        Method handles the collision of both heads of two snakes. This method
        also handles cases when the head of the first snake collides with the
        body of the second snake, and Vice versa: cases when the head of the
        second snake crashes into the body of the first snake.
        """
        # If both heads of snakes collided...
        if (self.head_x_coord_1 == self.head_x_coord_2 and
            self.head_y_coord_1 == self.head_y_coord_2):
            self.game_over_1 = True
            self.game_over_2 = True
            if self.platform == "Linux": set_normal_term()

        for i in range(self.num_of_snake_segments_1):
            # If the head of the second snake hit the tail of the first snake...
            if (self.snake_segments_coord_x_1[i] == self.head_x_coord_2 and
                self.snake_segments_coord_y_1[i] == self.head_y_coord_2):
                self.game_over_2 = True
                if self.platform == "Linux": set_normal_term()

        for i in range(self.num_of_snake_segments_2):
            # If the head of the first snake hit the tail of the second snake...
            if (self.snake_segments_coord_x_2[i] == self.head_x_coord_1 and
                self.snake_segments_coord_y_2[i] == self.head_y_coord_1):
                self.game_over_1 = True
                if self.platform == "Linux": set_normal_term()

    def get_game_over_status_player_1(self) -> bool:
        return self.game_over_1

    def get_game_over_status_player_2(self) -> bool:
        return self.game_over_2

    def set_game_mode_false(self):
        self.gamemode = False

    def set_default_settings(self):
        """Sets attribute settings before the beginning of the game itself."""
        # Basic settings.
        self.width = self.settings_storage['width']
        self.height = self.settings_storage['height']
        self.snake_and_walls = self.settings_storage['walls']
        self.game_speed = self.settings_storage['speed']
        self.time = time.time()
        self.centralize_score_n_time = " " * (int(self.width / 2) - 12)
        self.x_coord_of_fruit = random.randint(1, self.width - 1)
        self.y_coord_of_fruit = random.randint(1, self.height - 1)
        self.adding_points = 0

        # Snake1's settings.
        self.game_over_1 = False
        self.score_1 = 0
        self.head_x_coord_1 = (self.width / 2) - 5
        self.head_y_coord_1 = (self.height / 2) + 1
        self.direction_1 = 'UP'
        self.num_of_snake_segments_1 = self.settings_storage['length']
        self.snake_segments_coord_x_1 = []
        self.snake_segments_coord_y_1 = []

        # Snake2's settings.
        self.game_over_2 = False
        self.score_2 = 0
        self.head_x_coord_2 = (self.width / 2) + 5
        self.head_y_coord_2 = (self.height / 2) + 1
        self.direction_2 = 'UP'
        self.num_of_snake_segments_2 = self.settings_storage['length']
        self.snake_segments_coord_x_2 = []
        self.snake_segments_coord_y_2 = []

    def get_score(self) -> int:
        return self.score

    def get_time(self) -> int:
        return round(time.time() - self.time)

    def set_game_over_false(self):
        self.game_over_1 = False
        self.game_over_2 = False

    def determine_who_won(self) -> int:
        if self.score_1 > self.score_2:
            if not self.game_over_1 and self.game_over_2:
                return 1
            else:
                return 2

        elif self.score_1 < self.score_2:
            if self.game_over_1 and not self.game_over_2:
                return 2
            else:
                return 1
        elif self.score_1 == self.score_2:
            if not self.game_over_1 and self.game_over_2:
                return 1
            elif self.game_over_1 and not self.game_over_2:
                return 2
            else:
                return 3

    def get_score_of_players(self) -> list:
        return [str(self.score_1), str(self.score_2)]

    def get_status_about_snake_and_fruit(self):
        return self.another_player_gets_longer_status

    def create_new_threads(self) -> list:
        threading_list = []
        t1 = threading.Thread(target=lambda: self.process_players_input_win())
        threading_list.extend([t1, ])
        return threading_list
