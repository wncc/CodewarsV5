from scripts.utils import convert_player2, convert_player2_area, rescale_position

class DummyTower:
    def __init__(self, object, player2:bool,display_size):
        self.name = object.name
        if player2:
            self.position = rescale_position(convert_player2(object.position,display_size),reverse=True)
            # self.deploy_area = convert_player2_area(object.deploy_area,display_size) # MAINLY USEFUL
        else:
            self.position = rescale_position(object.position,reverse=True)
            # self.deploy_area = object.deploy_area   # MAINLY USEFUL
        self.health = object.health # MAINLY USEFUL
        self.damage = object.damage
        self.attack_range = object.attack_range
        self.target = None # MAINLY USEFUL
        self.deployable_troops = object.deployable_troops.copy()[:4]    # MAINLY USEFUL
        self.size = object.size
        self.total_elixir = object.total_elixir # MAINLY USEFUL
        self.total_dark_elixir = object.total_dark_elixir   # MAINLY USEFUL
        self.level = object.level
        self.game_timer = object.game_timer # MAINLY USEFUL

class DummyTroop:
    def __init__(self, object, player2:bool,display_size):
        self.name = object.name
        if player2:
            self.position = rescale_position(convert_player2(object.position,display_size),reverse=True) # MAINLY USEFUL
        else:
            self.position = rescale_position(object.position,reverse=True)
        self.health = object.health # MAINLY USEFUL
        self.damage = object.damage # MAINLY USEFUL
        self.target = None # MAINLY USEFUL
        self.uid = object.uid # MAINLY USEFUL
        self.size = object.size # MAINLY USEFUL
        self.elixir = object.elixir
        self.type = object.type # MAINLY USEFUL
        self.attack_range = object.attack_range # MAINLY USEFUL
        self.splash_range = object.splash_range
        self.target_type = object.target_type.copy() # MAINLY USEFUL