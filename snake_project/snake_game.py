from extra.tools.git_repo_opener import open_git_repo_in_browser
from extra.game_environment.menu_files.menu import Menu
from extra.game_environment.score_files.score import Score

from gamemodes.classic_mode import ClassicModeGameManager
from gamemodes.survival_mode import SurvivalModeGameManager
from gamemodes.battle_mode import BattleModeGameManager


game_menu = Menu()
game_menu.show_ascii_art_and_loading()
game_menu.show_welcome_message_to_player()
player_name = game_menu.set_name_of_player()
player_score = Score(player_name)

# Main loop
while True:
    game_menu.ask_player_about_choice_in_menu()
    menu_selection = game_menu.set_choice_in_menu()

    if menu_selection == 1:
        classic_mode = ClassicModeGameManager(player_score, game_menu)
        classic_mode.run()

    elif menu_selection == 2:
        survival_mode = SurvivalModeGameManager(player_score, game_menu)
        survival_mode.run()

    elif menu_selection == 3:
        battle_mode = BattleModeGameManager(player_score, game_menu)
        battle_mode.run()

    elif menu_selection == 4:
        player_score.show_score()

    elif menu_selection == 5:
        open_git_repo_in_browser()

    elif menu_selection == 6:
        game_menu.show_controls_for_snakes()

    else:
        exit()
