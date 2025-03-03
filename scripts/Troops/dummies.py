from scripts.utils import convert_player2, convert_player2_area

class DummyTower:
    def __init__(self, object, player2:bool,display_size):
        self.name = object.name
        if player2:
            self.position = convert_player2(object.position,display_size)
            self.deploy_area = convert_player2_area(object.deploy_area,display_size) # MAINLY USEFUL
        else:
            self.position = object.position
            self.deploy_area = object.deploy_area   # MAINLY USEFUL
        self.health = object.health # MAINLY USEFUL
        self.damage = object.damage
        self.attack_range = object.attack_range
        self.target = None # MAINLY USEFUL
        self.deployable_troops = object.deployable_troops.copy()[:4]    # MAINLY USEFUL
        self.size = object.size
        self.total_elixir = object.total_elixir # MAINLY USEFUL
        self.total_dark_elixir = object.total_dark_elixir   # MAINLY USEFUL
        self.level = object.level   # MAINLY USEFUL

class DummyTroop:
    def __init__(self, object, player2:bool,display_size):
        self.name = object.name
        if player2:
            self.position = convert_player2(object.position,display_size) # MAINLY USEFUL
        else:
            self.position = object.position
        self.health = object.health # MAINLY USEFUL
        self.damage = object.damage
        self.attack_range = object.attack_range
        self.target = None # MAINLY USEFUL
        self.size = object.size
        self.elixir = object.elixir
        self.type = object.type
        self.attack_range = object.attack_range
        self.splash_range = object.splash_range
        self.target_type = object.target_type.copy()