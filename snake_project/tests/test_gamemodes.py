from extra.game_environment.menu_files.menu import Menu
from extra.game_environment.score_files.score import Score

from gamemodes.classic_mode import ClassicModeGameManager
from gamemodes.survival_mode import SurvivalModeGameManager
from gamemodes.battle_mode import BattleModeGameManager


class TestClassicGamemodeClass:

    def setup(self):
        """Initialization of the game mode, player and installation of default
        settings.
        """
        menu_inst = Menu()
        score_inst = Score('TestName')
        self.gamemode = ClassicModeGameManager(score_inst, menu_inst)
        self.gamemode.settings_storage['width'] = 40
        self.gamemode.settings_storage['height'] = 20

        walls = "can crawl through the walls"
        self.gamemode.settings_storage['walls'] = walls
        self.gamemode.settings_storage['speed'] = 0.08
        self.gamemode.settings_storage['length'] = 3
        self.gamemode.set_default_settings()
        self.gamemode.initialize_new_player()

    def test_initialize_new_player_method_classic_mode(self):
        """Testing the content of snake_segments' lists and the value
        of adding points.
        """
        self.setup()
        assert len(self.gamemode.snake_segments_coord_x) != 0
        assert len(self.gamemode.snake_segments_coord_y) != 0
        assert self.gamemode.adding_points in [20, 30, 40]

    def test_snake_and_walls_logic_classic_mode(self):
        # Testing the ability to pass through one wall and exit the other.
        # Note: see self.gamemode.settings_storage['walls'] in setup method of
        # this class.
        self.gamemode.head_x_coord = 41
        self.gamemode.process_hook_logic()
        assert self.gamemode.head_x_coord == 1
        assert not self.gamemode.game_over

        self.gamemode.head_x_coord = 0
        self.gamemode.process_hook_logic()
        assert self.gamemode.head_x_coord == self.gamemode.width - 1
        assert not self.gamemode.game_over

        self.gamemode.head_y_coord = 22
        self.gamemode.process_hook_logic()
        assert self.gamemode.head_y_coord == 0
        assert not self.gamemode.game_over

        self.gamemode.head_y_coord = -1
        self.gamemode.process_hook_logic()
        assert self.gamemode.head_y_coord == self.gamemode.height
        assert not self.gamemode.game_over

        # Testing logic when the ability to pass through the wall is disabled.
        walls = "can't crawl through the walls"
        self.gamemode.settings_storage['walls'] = walls
        self.gamemode.set_default_settings()
        self.gamemode.initialize_new_player()

        self.gamemode.head_x_coord = 40
        self.gamemode.process_hook_logic()
        assert self.gamemode.game_over
        self.gamemode.game_over = False

        self.gamemode.head_x_coord = 0
        self.gamemode.process_hook_logic()
        assert self.gamemode.game_over
        self.gamemode.game_over = False

        self.gamemode.head_y_coord = 21
        self.gamemode.process_hook_logic()
        assert self.gamemode.game_over
        self.gamemode.game_over = False

        self.gamemode.head_y_coord = -1
        self.gamemode.process_hook_logic()
        assert self.gamemode.game_over
        self.gamemode.game_over = False

    def test_snake_eats_fruit_logic_classic_mode(self):
        # Testing the logic of increasing the number of snake's segments when it
        # eats fruit.
        self.gamemode.head_x_coord = 20
        self.gamemode.head_y_coord = 11
        self.gamemode.x_coord_of_fruit = 20
        self.gamemode.y_coord_of_fruit = 10
        self.gamemode.process_hook_logic()
        assert self.gamemode.num_of_snake_segments == 4

    def test_snake_eats_itself_logic_classic_mode(self):
        self.gamemode.head_x_coord = 20
        self.gamemode.head_y_coord = 13
        self.gamemode.process_hook_logic()
        assert self.gamemode.game_over


class TestSurvivalGamemodeClass:

    def setup(self):
        """Initialization of the game mode, players and installation of default
        settings.
        """
        menu_inst = Menu()
        score_inst = Score('TestName')
        self.gamemode = SurvivalModeGameManager(score_inst, menu_inst)
        self.gamemode.settings_storage['width'] = 40
        self.gamemode.settings_storage['height'] = 20

        walls = "can crawl through the walls"
        self.gamemode.settings_storage['walls'] = walls
        self.gamemode.settings_storage['speed'] = 0.08
        self.gamemode.settings_storage['length'] = 3
        self.gamemode.set_default_settings()
        self.gamemode.initialize_new_players()

    def test_initialize_new_players_method_survival_mode(self):
        """Testing the content of snake_segments_coord_x and
        snake_segments_coord_y for snake 1 and snake 2 and the value of adding
        points.
        """
        self.setup()
        assert len(self.gamemode.snake_segments_coord_x_1) != 0
        assert len(self.gamemode.snake_segments_coord_y_1) != 0
        assert len(self.gamemode.snake_segments_coord_x_2) != 0
        assert len(self.gamemode.snake_segments_coord_y_2) != 0
        assert self.gamemode.adding_points in [20, 30, 40]

    def test_snakes_and_walls_logic_survival_mode(self):
        # Testing the ability to pass through one wall and exit the other for
        # snake 1.
        # Note: see self.gamemode.settings_storage['walls'] in setup method of
        # this class.
        self.gamemode.head_x_coord_1 = 41
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_x_coord_1 == 1
        assert not self.gamemode.game_over_1

        self.gamemode.head_x_coord_1 = 0
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_x_coord_1 == self.gamemode.width - 1
        assert not self.gamemode.game_over_1

        self.gamemode.head_y_coord_1 = 22
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_y_coord_1 == 0
        assert not self.gamemode.game_over_1

        self.gamemode.head_y_coord_1 = -1
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_y_coord_1 == self.gamemode.height
        assert not self.gamemode.game_over_1

        # Testing the ability to pass through one wall and exit the other for
        # snake 2.
        self.gamemode.head_x_coord_2 = 41
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_x_coord_2 == 1
        assert not self.gamemode.game_over_2

        self.gamemode.head_x_coord_2 = 0
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_x_coord_2 == self.gamemode.width - 1
        assert not self.gamemode.game_over_2

        self.gamemode.head_y_coord_2 = 22
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_y_coord_2 == 0
        assert not self.gamemode.game_over_2

        self.gamemode.head_y_coord_2 = -1
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_y_coord_2 == self.gamemode.height
        assert not self.gamemode.game_over_2

        # Testing logic when the ability to pass through the wall is disabled.
        walls = "can't crawl through the walls"
        self.gamemode.settings_storage['walls'] = walls
        self.gamemode.set_default_settings()
        self.gamemode.initialize_new_players()

        # Snake 1.
        self.gamemode.head_x_coord_1 = 40
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        self.gamemode.head_x_coord_1 = 0
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        self.gamemode.head_y_coord_1 = 21
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        self.gamemode.head_y_coord_1 = -1
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        # Snake 2.
        self.gamemode.head_x_coord_2 = 40
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

        self.gamemode.head_x_coord_2 = 0
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

        self.gamemode.head_y_coord_2 = 21
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

        self.gamemode.head_y_coord_2 = -1
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

    def test_snakes_eat_fruit_logic_survival_mode(self):
        # Testing the logic of increasing the number of snakes' segments when
        # they eat fruit.

        # Test for snake 1.
        self.gamemode.head_x_coord_1 = 20
        self.gamemode.head_y_coord_1 = 11
        self.gamemode.x_coord_of_fruit = 20
        self.gamemode.y_coord_of_fruit = 10
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.num_of_snake_segments_1 == 4

        # Test for snake 2.
        self.gamemode.head_x_coord_2 = 20
        self.gamemode.head_y_coord_2 = 11
        self.gamemode.x_coord_of_fruit = 20
        self.gamemode.y_coord_of_fruit = 10
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.num_of_snake_segments_2 == 4

    def test_snakes_eat_themselves_logic_survival_mode(self):
        # Snake 1.
        self.gamemode.head_x_coord_1 = 15
        self.gamemode.head_y_coord_1 = 13
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        # Snake 2.
        self.gamemode.head_x_coord_2 = 25
        self.gamemode.head_y_coord_2 = 13
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

    def test_common_logic_of_2_snakes_survival_mode(self):
        # If two heads of snakes have the same coordinates, they lose.
        self.gamemode.head_x_coord_1 = 20
        self.gamemode.head_y_coord_1 = 20
        self.gamemode.head_x_coord_2 = 20
        self.gamemode.head_y_coord_2 = 20

        self.gamemode.process_common_logic_of_2_snakes()
        assert self.gamemode.game_over_1
        assert self.gamemode.game_over_2
        self.gamemode.game_over_1 = False
        self.gamemode.game_over_2 = False

        # If the coordinates of the first snake match the coordinates of the
        # elements of the tail of the 2nd snake, then the first snake loses and
        # vice versa.

        # Initial coords for the 2-nd snake's segments.
        self.gamemode.head_x_coord_1 = 25
        self.gamemode.head_y_coord_1 = 13
        self.gamemode.process_common_logic_of_2_snakes()
        assert self.gamemode.game_over_1

        # Initial coords for the 1-st snake's segments.
        self.gamemode.head_x_coord_2 = 15
        self.gamemode.head_y_coord_2 = 13
        self.gamemode.process_common_logic_of_2_snakes()
        assert self.gamemode.game_over_2


class TestBattleGamemodeClass:

    def setup(self):
        """Initialization of the game mode, players and installation of default
        settings.
        """
        menu_inst = Menu()
        score_inst = Score('TestName')
        self.gamemode = BattleModeGameManager(score_inst, menu_inst)

        walls = "can crawl through the walls"
        self.gamemode.settings_storage['walls'] = walls
        self.gamemode.settings_storage['speed'] = 0.08
        self.gamemode.settings_storage['game_time'] = 1000
        self.gamemode.settings_storage['length'] = 3
        self.gamemode.set_default_settings()
        self.gamemode.initialize_new_players()

    def test_initialize_new_players_method_battle_mode(self):
        """Testing the content of snake_segments_coord_x and
        snake_segments_coord_y for snake 1 and snake 2 and the value of adding
        points.
        """
        self.setup()
        assert len(self.gamemode.snake_segments_coord_x_1) != 0
        assert len(self.gamemode.snake_segments_coord_y_1) != 0
        assert len(self.gamemode.snake_segments_coord_x_2) != 0
        assert len(self.gamemode.snake_segments_coord_y_2) != 0
        assert self.gamemode.adding_points in [20, 30, 40]

    def test_snakes_and_walls_logic_battle_mode(self):
        # Testing the ability to pass through one wall and exit the other for
        # snake 1.
        # Note: see self.gamemode.settings_storage['walls'] in setup method of
        # this class.
        self.gamemode.head_x_coord_1 = 20
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_x_coord_1 == 1
        assert not self.gamemode.game_over_1

        self.gamemode.head_x_coord_1 = 0
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_x_coord_1 == 19
        assert not self.gamemode.game_over_1

        self.gamemode.head_y_coord_1 = 22
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_y_coord_1 == 0
        assert not self.gamemode.game_over_1

        self.gamemode.head_y_coord_1 = -1
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.head_y_coord_1 == 20
        assert not self.gamemode.game_over_1

        # Testing the ability to pass through one wall and exit the other for
        # snake 2.
        self.gamemode.head_x_coord_2 = 60
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_x_coord_2 == 41
        assert not self.gamemode.game_over_2

        self.gamemode.head_x_coord_2 = 40
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_x_coord_2 == 59
        assert not self.gamemode.game_over_2

        self.gamemode.head_y_coord_2 = 22
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_y_coord_2 == 0
        assert not self.gamemode.game_over_2

        self.gamemode.head_y_coord_2 = -1
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.head_y_coord_2 == 20
        assert not self.gamemode.game_over_2

        # Testing logic when the ability to pass through the wall is disabled.
        walls = "can't crawl through the walls"
        self.gamemode.settings_storage['walls'] = walls
        self.gamemode.set_default_settings()
        self.gamemode.initialize_new_players()

        # Snake 1.
        self.gamemode.head_x_coord_1 = 20
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        self.gamemode.head_x_coord_1 = 0
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        self.gamemode.head_y_coord_1 = 21
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        self.gamemode.head_y_coord_1 = -1
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1
        self.gamemode.game_over_1 = False

        # Snake 2.
        self.gamemode.head_x_coord_2 = 60
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

        self.gamemode.head_x_coord_2 = 40
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

        self.gamemode.head_y_coord_2 = 21
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

        self.gamemode.head_y_coord_2 = -1
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
        self.gamemode.game_over_2 = False

    def test_snakes_eat_fruit_logic_battle_mode(self):
        # Testing the logic of increasing the number of segments of the 2-nd
        # snake when the first one eats fruit and vice versa.

        # Snake 1.
        self.gamemode.head_x_coord_1 = 10
        self.gamemode.head_y_coord_1 = 11
        self.gamemode.x_coord_of_fruit_1 = 10
        self.gamemode.y_coord_of_fruit_1 = 10
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.num_of_snake_segments_2 == 4

        # Snake 2.
        self.gamemode.head_x_coord_2 = 55
        self.gamemode.head_y_coord_2 = 11
        self.gamemode.x_coord_of_fruit_2 = 55
        self.gamemode.y_coord_of_fruit_2 = 10
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.num_of_snake_segments_1 == 4

    def test_snakes_eat_themselves_logic_battle_mode(self):
        # Snake 1.
        self.gamemode.head_x_coord_1 = 10
        self.gamemode.head_y_coord_1 = 13
        self.gamemode.process_hook_logic_for_player_1()
        assert self.gamemode.game_over_1

        # Snake 2.
        self.gamemode.head_x_coord_2 = 50
        self.gamemode.head_y_coord_2 = 13
        self.gamemode.process_hook_logic_for_player_2()
        assert self.gamemode.game_over_2
