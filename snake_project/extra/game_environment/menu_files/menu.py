import getpass
import os
import sys
import time

from colorama import Fore, deinit, init

from extra.tools.validators import Validators
from extra.tools.os_initializer import init_os
from extra.tools.clean_console_command_setter import set_cleaning_command


class BeforeTheGame:
    """The class is responsible for all operations that occur before the game.

    Class's method are used to show the splash screen(Snake's ASCII art,
    Loading...'-label), welcome message. Also it's showing controls for snakes
    in the interface of main menu. The class is used to record the
    information about the game settings(field size , game speed, default length
    of the snake etc.) for game modes.
    """

    def __init__(self):
        """Inits class BeforeTheGame with the player name, dictionary of future
        player's choice and self.gamemode.
        """

        # The name of the player will be selected according to OS user name
        self.player_name = getpass.getuser()
        self._player_choice = {}
        self.gamemode = 1
        self.platform = init_os()
        self.RESET = set_cleaning_command()
        self.validators = Validators()

    def set_gamemode(self, gamemode: int):

        self.gamemode = gamemode

    def show_ascii_art_and_loading(self):
        """Shows snake's ASCII art and 'Loading...'-label on the splash screen.

        Using ASCII symbols from files console_img/snake.txt,
        console_img/loading.txt to show them in the console.
        """
        if self.platform == "Windows":
            os.system('mode con: cols=61 lines=25')
        else:
            sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=25, cols=60))

        init(autoreset=True)  # Initialization of colorama.
        file = 'extra/game_environment/menu_files/console_img/snake.txt'
        with open(file, 'r') as img:
            for line in img:
                for symbol in line:
                    if (symbol == '\\' or symbol == '/' or symbol == '(' or
                        symbol == ')'):
                        # Painting of red forked tongue of the snake.
                        print(Fore.RED + symbol, end='')
                    elif symbol == '#':
                        # Painting of snake's Body.
                        print(Fore.GREEN + symbol, end='')
                    elif symbol == '<' or symbol == '>' or symbol == '.':
                        # Painting of snake's eyes.
                        print(Fore.MAGENTA + symbol, end='')
                    else:
                        # Painting of background.
                        print(symbol, end='')
        deinit()  # Uninstallation of colorama.
        time.sleep(4)
        os.system(self.RESET)

        if self.platform == "Windows":
            os.system('mode con: cols=90 lines=25')
        else:
            sys.stdout.write("\x1b[8;{rows};{cols}t".format(cols=90, rows=25))

        file = 'extra/game_environment/menu_files/console_img/loading.txt'
        with open(file) as img:
            for line in img:
                print(line[:-1])

        time.sleep(2)
        os.system(self.RESET)

    def show_welcome_message_to_player(self):
        os.system(self.RESET)
        print(str(self.player_name) + ", " + "Welcome to the game!")

    def show_controls_for_snakes(self):
        file = 'extra/game_environment/menu_files/console_img/controls.txt'
        with open(file) as img:
            for line in img:
                print(line[:-1])

        while True:
            print("Type 'exit' to return to main menu")
            player_input = input()
            if 'exit' in player_input.lower():
                os.system(self.RESET)
                break

    def ask_player_about_choice_in_menu(self):
        print("Please, сhoose one variant from menu: ")
        print('1) Classic mode\n2) Survival (2 p on one computer)')
        print('3) Battle (2 p on one computer)\n4) My personal score')
        print('5) GitHub repo\n6) Controls\n7) Quit the game')

        validator = self.validators.validate_main_menu_selection()
        player_input = validator
        if player_input == 1:
            self._player_choice['menu_melection'] = 1
        elif player_input == 2:
            self._player_choice['menu_melection'] = 2
        elif player_input == 3:
            self._player_choice['menu_melection'] = 3
        elif player_input == 4:
            self._player_choice['menu_melection'] = 4
        elif player_input == 5:
            self._player_choice['menu_melection'] = 5
        elif player_input == 6:
            self._player_choice['menu_melection'] = 6
        else:
            file = 'extra/game_environment/menu_files/console_img/byebye.txt'
            with open(file) as img:
                for line in img:
                    print(line[:-1])

            time.sleep(2)
            os.system(self.RESET)

            self._player_choice['menu_melection'] = 7

    def ask_player_about_field_size(self):
        print('Field size: ')
        print('1) 20 x 20\n2) 40 x 20\n3) 60 x 20\n4) 78 x 20')

        validator = self.validators.validate_choice_in_field_size()
        player_input = validator
        if player_input == 1:
            self._player_choice['size'] = (20, 20)
        elif player_input == 2:
            self._player_choice['size'] = (40, 20)
        elif player_input == 3:
            self._player_choice['size'] = (60, 20)
        else:
            self._player_choice['size'] = (78, 20)

    def ask_player_about_snake_length(self):
        print('Please, select the length of snake in the start of the game')
        print('1) 3\n2) 6\n3) 9\n4) Custom')

        validator = self.validators.validate_choice_in_snake_length()
        player_input = validator
        if player_input == 1:
            # Head of a snake is not in snake body.
            self._player_choice['length'] = 2
        elif player_input == 2:
            self._player_choice['length'] = 5
        elif player_input == 3:
            self._player_choice['length'] = 8
        else:
            validator = self.validators.validate_choice_in_snake_length(cust=1)
            player_input_cust_length = validator
            self._player_choice['length'] = player_input_cust_length

    def ask_player_about_snake_and_walls(self):
        print('Can snake crawl through the walls?')
        print('1) YEAP!\n2) NOPE! ')

        validator = self.validators.validate_choice_in_snake_and_walls()
        player_input = validator
        if player_input == 1:
            self._player_choice['walls'] = "can crawl through the walls"
        else:
            self._player_choice['walls'] = "can't crawl through the walls"

    def ask_plyaer_about_speed(self):
        print('Please, set game speed')
        print('1) Slow (+20 for 1 fruit)')
        print('2) Normal (+30 for 1 fruit)')
        print('3) High (+40 for 1 fruit)')

        validator = self.validators.validate_player_input_in_speed()
        player_input = validator
        self._player_choice['game_speed'] = player_input

        if player_input == 1:
            self._player_choice['game_speed'] = 0.08
        elif player_input == 2:
            self._player_choice['game_speed'] = 0.06
        else:
            self._player_choice['game_speed'] = 0.03

    def ask_player_about_game_time(self):
        print("Please, set a game time(MIN = 100)")
        validator = self.validators.validate_player_input_in_game_time()
        player_input = validator
        self._player_choice['game_time'] = player_input


class SetGameSettings(BeforeTheGame):
    """The class sets the game settings for the game core.

    According to the choice that made by the player this class sets the game
    settings.
    """

    def set_choice_in_menu(self) -> int:
        return self._player_choice['menu_melection']

    def field_size_set_width(self) -> int:
        return self._player_choice['size'][0]

    def field_size_set_height(self) -> int:
        return self._player_choice['size'][1]

    def set_snake_and_walls_setting(self) -> str:
        return self._player_choice['walls']

    def set_default_length(self) -> int:
        return self._player_choice['length']

    def set_name_of_player(self) -> str:
        return self.player_name

    def set_game_speed(self) -> float:
        return self._player_choice['game_speed']

    def set_game_time(self) -> int:
        return self._player_choice['game_time']


class AfterTheGame(SetGameSettings):
    """Class is responsible for processing player's choice after the game."""

    def ask_player_for_further_actions(self) -> int:
        """Gives a choices for further actions after the game.

        Provides player with the interface after the game. Shows ASCII-banner
        'BYE BYE' if '4) Quit the game' was selected.
        """

        print('1) Play one more time\n2) Game settings')
        print('3) Menu\n4) Quit the game')

        validator = self.validators.validate_input_after_the_game()
        player_input = validator
        if player_input == 1:
            self.after_the_game_status = 1
        elif player_input == 2:
            self.after_the_game_status = 2
        elif player_input == 3:
            self.after_the_game_status = 3
        else:
            file = 'extra/game_environment/menu_files/console_img/byebye.txt'
            with open(file) as img:
                for line in img:
                    print(line[:-1])

            self.after_the_game_status = 4
            time.sleep(2)
        os.system(self.RESET)
        return self.after_the_game_status


class Menu(AfterTheGame):
    pass
