import random
from teams.helper_function import Troops, Utils

team_name = "CPSIMPLE"
troops = [
    Troops.wizard, Troops.minion, Troops.archer,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.knight, Troops.barbarian
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Wizard"

def random_x(min_val=-15, max_val=15):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data.get("MyTower")
    opp_troops = arena_data.get("OppTroops", [])
    time_remaining = arena_data.get("TimeRemaining", 180)
    my_troops = arena_data.get("MyTroops", [])

    if not my_tower:
        return

    # --- Update Team Signal ---
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name

    # --- Dynamic Strategy Switching ---
    defensive_mode = time_remaining <= 60 and my_tower.health > 50
    aggressive_mode = my_tower.health < 50

    # --- Analyze Opponent Composition ---
    opponent_air = {"Minion", "Dragon", "Wizard", "Balloon"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Wizard", "Valkyrie", "Giant"}
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)

    if count_ground > count_air:
        recommended_counter = "air"
    elif count_air > count_ground:
        recommended_counter = "ground"
    else:
        recommended_counter = None

    # --- Score Our Troops Based on Dynamic Strategy ---
    deployable = getattr(my_tower, "deployable_troops", [])
    troop_data = {
        Troops.wizard: {"score": 5, "category": "air", "name": "Wizard"},
        Troops.minion: {"score": 3, "category": "air", "name": "Minion"},
        Troops.archer: {"score": 4, "category": "ground", "name": "Archer"},
        Troops.dragon: {"score": 6, "category": "air", "name": "Dragon"},
        Troops.skeleton: {"score": 3, "category": "ground", "name": "Skeleton"},
        Troops.valkyrie: {"score": 5, "category": "ground", "name": "Valkyrie"},
        Troops.knight: {"score": 4, "category": "ground", "name": "Knight"},
        Troops.barbarian: {"score": 3, "category": "ground", "name": "Barbarian"}
    }

    bonus = 3
    best_troop = None
    best_score = -1

    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        category = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and category == recommended_counter else 0)

        # Adjust for defensive strategy
        if defensive_mode and category == "ground":
            score += 2

        if score > best_score:
            best_score = score
            best_troop = troop

    # --- Deploy Counters for Opponent Troops First ---
    for troop in opp_troops:
        if troop.name in ["Prince", "Musketeer", "Giant"] and hasattr(troop, "position"):
            if Troops.skeleton in deployable:
                deploy_list.list_.append((Troops.skeleton, troop.position))
            elif Troops.barbarian in deployable:
                deploy_list.list_.append((Troops.dragon, troop.position))
        if troop.name == "Musketeer" and hasattr(troop, "position"):
            if Troops.knight in deployable:
                deploy_list.list_.append((Troops.knight, troop.position))
            elif Troops.barbarian in deployable:
                deploy_list.list_.append((Troops.dragon, troop.position))
        if troop.name in ["Knight", "Giant"] and hasattr(troop, "position"):
            if Troops.skeleton in deployable:
                deploy_list.list_.append((Troops.skeleton, troop.position))
            elif Troops.barbarian in deployable:
                deploy_list.list_.append((Troops.dragon, troop.position))
        if troop.name == "Balloon" and hasattr(troop, "position"):
            if Troops.dragon in deployable:
                deploy_list.list_.append((Troops.minion, troop.position))
            elif Troops.minion in deployable:
                deploy_list.list_.append((Troops.dragon, troop.position))
        if troop.name == "Wizard" and hasattr(troop, "position"):
            if Troops.skeleton in deployable:
                deploy_list.list_.append((Troops.skeleton, troop.position))

    # --- Deployment Positioning & Combos ---
    if best_troop is not None:
        deploy_position = (random_x(-5, 5), 10)  # Deploying closer to opponent territory
        deploy_list.list_.append((best_troop, deploy_position))

    combo_pairs = {
        Troops.dragon: [Troops.wizard, Troops.knight],
        Troops.knight: [Troops.wizard, Troops.minion],
        Troops.skeleton:[Troops.dragon, Troops.archer],
        Troops.barbarian:[Troops.valkyrie, Troops.archer],
        Troops.valkyrie: [Troops.wizard, Troops.archer],
    }
    if best_troop in combo_pairs:
        for support_troop in combo_pairs[best_troop]:
            if support_troop in deployable:
                deploy_list.list_.append((support_troop, (random_x(-5, 5), 10)))

    # --- Fallback Deployment ---
    if not deploy_list.list_ and deployable:
        deploy_list.list_.append((deployable[0], (10, 10)))