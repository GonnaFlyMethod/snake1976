# Validators for all player's inputs
import os

from .os_initializer import init_os

from extra.tools.clean_console_command_setter import set_cleaning_command


class Validators:
    """The class helps the user to enter valid data then the game require it."""

    def __init__(self):
        self.platform = init_os()
        self.RESET = set_cleaning_command()

    def validate_main_menu_selection(self) -> int:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, сhoose something from menu[1-7]")
                continue

            if player_input < 1 or player_input > 7:
                print("Please, сhoose something from menu[1-7]")
                continue
            else:
                os.system(self.RESET)
                return player_input

    def validate_choice_in_field_size(self) -> int:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, select one of the available field sizes[1-4]")
                continue
            if player_input < 1 or player_input > 4:
                print("Please, select one of the available field sizes[1-4]")
                continue
            else:
                os.system(self.RESET)
                return player_input

    def validate_choice_in_snake_length(self, cust=0) -> int:
        if cust == 0:
            while True:
                try:
                    player_input = int(input('~ '))
                except ValueError:
                    print("Please, select one variant[1-5]")
                    continue

                if player_input < 1 or player_input > 5:
                    print("Please, select one variant[1-5]")
                    continue
                else:
                    os.system(self.RESET)
                    return player_input
        else:
            while True:
                print('MIN length = 3')
                try:
                    player_input = int(input('~ '))

                except ValueError:
                    print("Please, set custom length [MUST BE NUMBER]")
                    continue

                if player_input < 3:
                    print("The entered snake length doesn't meet the ")
                    print("requirements Try again!")
                    continue
                else:
                    os.system(self.RESET)
                    return player_input

    def validate_choice_in_snake_and_walls(self) -> int:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print('Please, choose one variant[1 or 2]')
                continue

            if player_input < 1 or player_input > 2:
                print('Please, choose one variant[1 or 2]')
                continue
            else:
                os.system(self.RESET)
                return player_input

    def validate_choice_in_color_of_snake(self, second_player=0) -> int:
        if second_player == 0:
            while True:
                try:
                    player_input = int(input('~ '))
                except ValueError:
                    print("Please, сhoose one color for the 1-st player[1-7]")
                    continue

                if player_input < 1 or player_input > 7:
                    print("Please, сhoose one color for the 1-st player[1-7]")
                    continue
                else:
                    os.system(self.RESET)
                    return player_input
        else:
            while True:
                try:
                    player_input = int(input('~ '))
                except ValueError:
                    print("Please, сhoose one color for the 2-nd player[1-6]")
                    continue

                if player_input < 1 or player_input > 6:
                    print("Please, сhoose one color for the 2-nd player[1-6]")
                    continue
                else:
                    os.system(self.RESET)
                    return player_input

    def validate_player_input_in_speed(self) -> int:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, select one variant[1-3]")
                continue

            if player_input < 1 or player_input > 3:
                print("Please, select one variant[1-3]")
                continue
            else:
                os.system(self.RESET)
                return player_input

    def validate_player_input_in_game_time(self) -> int:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, set game time [MUST BE NUMBER]")
                continue

            if player_input < 100:
                print('MIN TIME IS 100!')
                continue
            else:
                os.system(self.RESET)
                return player_input

    def validate_input_after_the_game(self) -> int:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, select one variant[1-4]")
                continue

            if player_input < 1 or player_input > 4:
                print("Please, select one variant[1-4]")
                continue
            else:
                os.system(self.RESET)
                return player_input
