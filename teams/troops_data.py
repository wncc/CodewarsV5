SLOW = 1
MEDIUM = 3
FAST = 5

SLOW_ATTACK = 3
MEDIUM_ATTACK = 2
FAST_ATTACK = 1

class Archer:
    def __init__(self):
        self.name = "Archer"
        self.type = "ground"
        self.elixir = 3
        self.size = 0.15 * 9.375
        self.health = 334
        self.damage = 118
        self.speed = MEDIUM
        self.splash_range = 0
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": True, "ground": True, "building": True}
        self.discovery_range = 8 * 1.875
        self.number = 2
        self.attack_range = 5 * 1.875

class Barbarian:
    def __init__(self):
        self.name = "Barbarian"
        self.type = "ground"
        self.elixir = 3
        self.size = 0.25 * 9.375
        self.health = 736
        self.damage = 161
        self.speed = MEDIUM
        self.splash_range = 0
        self.attack_speed = MEDIUM_ATTACK
        self.target_type = {"air": False, "ground": True, "building": True}
        self.discovery_range = 5 * 1.875
        self.number = 3
        self.attack_range = 0

class Balloon:
    def __init__(self):
        self.name = "Balloon"
        self.type = "air"
        self.elixir = 5
        self.size = 0.4 * 9.375
        self.health = 2226
        self.damage = 424
        self.speed = MEDIUM
        self.splash_range = 0
        self.attack_speed = MEDIUM_ATTACK
        self.target_type = {"air": False, "ground": False, "building": True}
        self.discovery_range = 5 * 1.875
        self.number = 1
        self.attack_range = 0

class Dragon:
    def __init__(self):
        self.name = "Dragon"
        self.type = "air"
        self.elixir = 4
        self.size = 0.4 * 9.375
        self.health = 1267
        self.damage = 176
        self.speed = FAST
        self.splash_range = 1 * 1.875
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": True, "ground": True, "building": True}
        self.discovery_range = 5 * 1.875
        self.number = 1
        self.attack_range = 3.5 * 1.875

class Giant:
    def __init__(self):
        self.name = "Giant"
        self.type = "ground"
        self.elixir = 5
        self.size = 0.5 * 9.375
        self.health = 5423
        self.damage = 337
        self.speed = SLOW
        self.splash_range = 0
        self.attack_speed = SLOW_ATTACK
        self.target_type = {"air": False, "ground": False, "building": True}
        self.discovery_range = 7 * 1.875
        self.number = 1
        self.attack_range = 0

class Minion:
    def __init__(self):
        self.name = "Minion"
        self.type = "air"
        self.elixir = 3
        self.size = 0.15 * 9.375
        self.health = 252
        self.damage = 129
        self.speed = FAST
        self.splash_range = 0
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": True, "ground": True, "building": True}
        self.discovery_range = 4 * 1.875
        self.number = 3
        self.attack_range = 2 * 1.875

class Skeleton:
    def __init__(self):
        self.name = "Skeleton"
        self.type = "ground"
        self.elixir = 3
        self.size = 0.15 * 9.375
        self.health = 89
        self.damage = 89
        self.speed = FAST
        self.splash_range = 0
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": False, "ground": True, "building": True}
        self.discovery_range = 4 * 1.875
        self.number = 10
        self.attack_range = 0

class Valkyrie:
    def __init__(self):
        self.name = "Valkyrie"
        self.type = "ground"
        self.elixir = 4
        self.size = 0.2 * 9.375
        self.health = 2097
        self.damage = 195
        self.speed = MEDIUM
        self.splash_range = 1 * 1.875
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": False, "ground": True, "building": True}
        self.discovery_range = 7 * 1.875
        self.number = 1
        self.attack_range = 0

class Wizard:
    def __init__(self):
        self.name = "Wizard"
        self.type = "ground"
        self.elixir = 5
        self.size = 0.25 * 9.375
        self.health = 1100
        self.damage = 410
        self.speed = MEDIUM
        self.splash_range = 1 * 1.875
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": True, "ground": True, "building": True}
        self.discovery_range = 8 * 1.875
        self.number = 1
        self.attack_range = 5.5 * 1.875

class Prince:
    def __init__(self):
        self.name = "Prince"
        self.type = "ground"
        self.elixir = 5
        self.size = 0.3 * 9.375
        self.health = 1920
        self.damage = 392
        self.speed = FAST
        self.splash_range = 0
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": False, "ground": True, "building": True}
        self.discovery_range = 7 * 1.875
        self.number = 1
        self.attack_range = 0

class Musketeer:
    def __init__(self):
        self.name = "Musketeer"
        self.type = "ground"
        self.elixir = 4
        self.size = 0.2 * 9.375
        self.health = 792
        self.damage = 239
        self.speed = MEDIUM
        self.splash_range = 0
        self.attack_speed = MEDIUM_ATTACK
        self.target_type = {"air": True, "ground": True, "building": True}
        self.discovery_range = 8 * 1.875
        self.number = 1
        self.attack_range = 6 * 1.875

class Knight:
    def __init__(self):
        self.name = "Knight"
        self.type = "ground"
        self.elixir = 3
        self.size = 0.3 * 9.375
        self.health = 1938
        self.damage = 221
        self.speed = MEDIUM
        self.splash_range = 0
        self.attack_speed = FAST_ATTACK
        self.target_type = {"air": False, "ground": True, "building": True}
        self.discovery_range = 7 * 1.875
        self.number = 1
        self.attack_range = 0