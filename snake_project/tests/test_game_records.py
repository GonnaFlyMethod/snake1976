import os
from colorama import Fore, deinit, init


records_dir = "snake_project/extra/game_environment/score_files/records"

scores = records_dir + "/scores.txt"
players = records_dir + "/players.txt"
date_and_time = records_dir + "/date_n_time.txt"

init(autoreset=True)  # Initialization of colorama.
print("\n" + "~" * 42 + Fore.CYAN + "[NOTE]" + Fore.RESET + "~" * 42)
print("Before commit you need to make sure that there are 3 files in the " +
    "'records' folder and\nthey are all empty:")

print(date_and_time)
print(players)
print(scores)
deinit()  # Uninstallation of colorama.
print("\n" + "~" * 90)


def test_game_records_for_commit():
    global records_dir, scores, players, date_and_time

    for file in [scores, players, date_and_time]:
        assert os.stat(file).st_size == 0

    assert len(os.listdir(records_dir)) == 3
