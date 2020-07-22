import os
from datetime import datetime

from extra.tools.os_initializer import init_os


class Score:
    """The class provides player with the results of his game[only classic mod].

    Score class writes down player's score and shows to the player his results
    as a table.
    """

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.players = 'extra/game_environment/score_files/records/players.txt'
        self.scores = 'extra/game_environment/score_files/records/scores.txt'
        self.DnT = 'extra/game_environment/score_files/records/date_n_time.txt'
        self.RESET = "cls" if init_os() == "Windows" else "clear"

    def write_down_player_score(self, score: int) -> None:
        """Records player data in 3 different files."""
        with open(self.players, 'a') as file:
            file.write(str(self.player_name) + '\n')

        with open(self.scores, 'a') as file:
            file.write(str(score) + '\n')

        date_n_time_now = datetime.now()
        # DD/MM/YYYY /Hours/Minutes/Seconds
        dt_string = date_n_time_now.strftime("%d/%m/%Y %H:%M:%S")
        with open(self.DnT, 'a') as file:
            file.write(str(dt_string) + '\n')

    def show_score(self):
        """Shows the data about the game in the form of a table.

        The method extracts data from 3 files which were previously recorded.
        The first file contains the players' names. The second one store
        players' game scores and the last one contains game date and time.
        Method inserts this data into the table that draws by itself.
        Shows the data of the top 20 players.
        """
        with open(self.players, 'r') as players:
            with open(self.scores, 'r') as scores:
                with open(self.DnT, 'r') as date_n_time:
                    list_for_parsing = []
                    for line_1 in players:
                        line_2 = scores.readline()
                        line_3 = date_n_time.readline()
                        # There is no need to include No \n.
                        clean_player_name = line_1[:len(line_1) - 1]
                        clean_date_n_time = line_3[:len(line_3) - 1]
                        list_for_parsing.append(
                            (
                                int(line_2),
                                clean_player_name,
                                clean_date_n_time
                            )
                        )

        find_longest_player_name = []
        find_longest_player_score = []
        find_longest_date = []

        for i in list_for_parsing:
            find_longest_player_name.append(len(str(i[1])))
            find_longest_player_score.append(len(str(i[0])))
            find_longest_date.append(len(str(i[2])))

        longest_player_name = max(find_longest_player_name)
        longest_player_score = max(find_longest_player_score)
        longest_date = max(find_longest_date)

        player_row = 'Player' + (' ' * (longest_player_name))
        score_row = 'Score' + (' ' * (longest_player_score))
        # Adds one more '-' symbol.
        date_row = 'D&T' + (' ' * (longest_date - len('D&T') + 1))

        print(player_row + '|' + score_row + '|' + date_row)
        print('-' * len(player_row) + '+' + '-' * len(score_row) + '+' + '-' *
            len(date_row))

        length_of_player_row = len(player_row)
        length_of_score_row = len(score_row)
        length_of_date_row = len(date_row)

        num_of_str = 1

        list_for_parsing.sort(reverse=True)
        for i in list_for_parsing:
            if num_of_str > 20:
                break

            # Takes into account whitespace after the player name in the row
            space_player_row = length_of_player_row - (len(str(i[1])) +
                (len(str(num_of_str)) + 1))

            space_score_row = length_of_score_row - (len(str(i[0])))
            space_date_row = length_of_date_row - (len(str(i[2])))

            print(num_of_str, str(i[1]) + (' ' * (space_player_row)) + '|' +
                str(i[0]) + (' ' * (space_score_row)) + '|' +
                str(i[2]) + (' ' * space_date_row))

            num_of_str += 1

        while True:
            print("Type 'exit' to return to main menu")
            player_input = input()
            if 'exit' in player_input.lower():
                os.system(self.RESET)
                break
