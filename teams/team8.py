import random
from teams.helper_function import Troops, Utils

team_name = "Junglee_Log.cpp"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.knight,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data):
    my_tower = arena_data["MyTower"]
    deployable_troops = my_tower.deployable_troops
    opp_troops = arena_data["OppTroops"]
    buffer_cards = ["Minion", "Knight", "Archer", "Dragon"]

    # 1. Wizard check
    if "Wizard" in deployable_troops:
        deploy_list.deploy_wizard((0, 0))
        # return

    # 2. Opponent troops crossing middle
    crossing_troops = [t for t in opp_troops if t.position[1] > 0]
    if crossing_troops:
        closest = min(crossing_troops, key=lambda t: Utils.calculate_distance(my_tower.position, t.position, False))
        deploy_pos = (closest.position[0] + random_x(-5, 5), closest.position[1] + random_x(-5, 5))
        if "Valkyrie" in deployable_troops:
            deploy_list.deploy_valkyrie(deploy_pos)
        elif "Barbarian" in deployable_troops:
            deploy_list.deploy_barbarian(deploy_pos)
        # return

    # 3. Prince or Giant check
    prince_giant = [t for t in opp_troops if t.name in ["Prince", "Giant"] and t.position[1] > 0]
    if prince_giant:
        target = min(prince_giant, key=lambda t: Utils.calculate_distance(my_tower.position, t.position, False))
        spawn_pos = (target.position[0], 0)
        if "Skeleton" in deployable_troops:
            deploy_list.deploy_skeleton(spawn_pos)
        # return

    # 4. Buffer cards with excess elixir
    if my_tower.total_elixir > 5:
        available_buffer = [card for card in buffer_cards if card in deployable_troops]
        if available_buffer:
            card = random.choice(available_buffer)
            spawn_pos = (0, 0)
            if card == "Minion":
                deploy_list.deploy_minion(spawn_pos)
            elif card == "Knight":
                deploy_list.deploy_knight(spawn_pos)
            elif card == "Archer":
                deploy_list.deploy_archer(spawn_pos)
            elif card == "Dragon":
                deploy_list.deploy_dragon(spawn_pos)