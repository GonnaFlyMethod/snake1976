def complex_ask(menu_instance, mode: int) -> dict:
    """Asks player about the game settings and then returns dictionary
    with them.
    """
    player_choice = {}

    if mode == 1:
        # Classic mode
        menu_instance.set_gamemode(1)
        menu_instance.ask_player_about_field_size()
        menu_instance.ask_player_about_snake_length()
        menu_instance.ask_player_about_snake_and_walls()
        menu_instance.ask_plyaer_about_speed()

        player_choice['width'] = menu_instance.field_size_set_width()
        player_choice['height'] = menu_instance.field_size_set_height()
        player_choice['length'] = menu_instance.set_default_length()
        player_choice['walls'] = menu_instance.set_snake_and_walls_setting()
        player_choice['speed'] = menu_instance.set_game_speed()
        return player_choice

    elif mode == 2:
        # Survival mode
        menu_instance.set_gamemode(2)
        menu_instance.ask_player_about_field_size()
        menu_instance.ask_player_about_snake_length()
        menu_instance.ask_player_about_snake_and_walls()
        menu_instance.ask_plyaer_about_speed()

        player_choice['width'] = menu_instance.field_size_set_width()
        player_choice['height'] = menu_instance.field_size_set_height()
        player_choice['length'] = menu_instance.set_default_length()
        player_choice['walls'] = menu_instance.set_snake_and_walls_setting()
        player_choice['speed'] = menu_instance.set_game_speed()
        return player_choice

    else:
        # Battle mode
        menu_instance.set_gamemode(3)
        menu_instance.ask_player_about_snake_length()
        menu_instance.ask_player_about_snake_and_walls()
        menu_instance.ask_plyaer_about_speed()
        menu_instance.ask_player_about_game_time()

        player_choice['length'] = menu_instance.set_default_length()
        player_choice['walls'] = menu_instance.set_snake_and_walls_setting()
        player_choice['speed'] = menu_instance.set_game_speed()
        player_choice['game_time'] = menu_instance.set_game_time()
        return player_choice
