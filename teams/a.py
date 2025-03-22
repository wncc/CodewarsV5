import random
from teams.helper_function import Troops, Utils

team_name = "Pratyaksh"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.musketeer,
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

def logic(arena_data: dict):
    global team_signal
    troops_data = Troops.troops_data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    # print(f"Team Signal: {team_signal}")
    
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    
    if count_ground > count_air:
        recommended_counter = "air"    # Counter ground with air units.
    elif count_air > count_ground:
        recommended_counter = "ground" # Counter air with ground units.
    else:
        recommended_counter = None     # No clear preference.
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 3, "category": "air",    "name": "Wizard"},
        Troops.minion:    {"score": 2, "category": "air",    "name": "Minion"},
        Troops.archer:    {"score": 4, "category": "ground", "name": "Archer"},
        Troops.musketeer:     {"score": 3, "category": "ground", "name": "Musketeer"},
        Troops.dragon:    {"score": 5, "category": "air",    "name": "Dragon"},
        Troops.skeleton:  {"score": 2, "category": "ground", "name": "Skeleton"},
        Troops.valkyrie:   {"score": 4, "category": "air",    "name": "Valkyrie"},
        Troops.barbarian: {"score": 3, "category": "ground", "name": "Barbarian"}
    }
    
    bonus = 3  # Bonus for matching the recommended counter strategy.
    best_troop = None
    best_score = -1
    
    # Loop over our full troop list, but only consider those that are deployable.
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop

    # --- Deployment Position ---
    if best_troop is not None:
        selected_category = troop_data[best_troop]["category"]
        if selected_category == "air":
            # Deploy air units further forward.
            deploy_position = (random_x(-25, 25), 0)
        else:
            # Deploy ground units slightly closer for support.
            deploy_position = (random_x(-10, 10), 0)
        deploy_list.list_.append((best_troop, deploy_position))
    else:
        # Fallback: If no deployable troop meets criteria, deploy the first available troop.
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))
