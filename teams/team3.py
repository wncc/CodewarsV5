import random
from teams.helper_function import Troops, Utils

team_name = "Meow Meow"
# Deck: knight, prince, wizard, archer, valkyrie, minion, skeleton, dragon
troops = [
    Troops.knight, Troops.prince, Troops.wizard, Troops.archer,
    Troops.valkyrie, Troops.minion, Troops.skeleton, Troops.dragon
]
deploy_list = Troops([])
team_signal = "h, ?, ?, ?, ?, ?, ?, ?, ?"  # Rolling queue of 8 slots (plus header "h")

def random_x(min_val=-5, max_val=5):
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
    
    # ------------------ PRIORITY 1: DEPLOY OUR WIZARD FREQUENTLY ------------------
    wizard_threshold = 5
    if Troops.wizard in my_tower.deployable_troops:
        if my_tower.total_elixir < wizard_threshold:
            return  # Not enough elixir; store elixir.
        if opp_troops:
            avg_enemy_x = sum(t.position[0] for t in opp_troops) / len(opp_troops)
        else:
            avg_enemy_x = 3
        wizard_pos = (int(avg_enemy_x), 0)
        if not any(t == Troops.wizard for t, _ in deploy_list.list_):
            deploy_list.list_.insert(0, (Troops.wizard, wizard_pos))
        if not any(t in (Troops.knight, Troops.prince, Troops.valkyrie, Troops.dragon)
                   and pos[0] < wizard_pos[0] for t, pos in deploy_list.list_):
            protector_pos = (wizard_pos[0] - random.randint(1, 3), 0)
            deploy_list.list_.insert(0, (Troops.knight, protector_pos))
    
    # ------------------ PRIORITY 2: COUNTER ENEMY WIZARD ON OUR HALF ------------------
    enemy_wizards = [t for t in opp_troops if t.name == "Wizard" and t.position[1] < 50]
    if enemy_wizards:
        for enemy_wiz in enemy_wizards:
            heavy_candidate = None
            deployable_set = my_tower.deployable_troops
            if Troops.knight in deployable_set:
                heavy_candidate = Troops.knight
            elif Troops.valkyrie in deployable_set:
                heavy_candidate = Troops.valkyrie
            elif Troops.prince in deployable_set:
                heavy_candidate = Troops.prince
            else:
                if Troops.skeleton in deployable_set:
                    heavy_candidate = Troops.skeleton
                elif Troops.dragon in deployable_set:
                    heavy_candidate = Troops.dragon
            if heavy_candidate is not None:
                deploy_list.list_ = [(heavy_candidate, enemy_wiz.position)]
                return  # Focus exclusively on countering enemy Wizard.
    
    # ------------------ PHASE 3: SIDE-SPECIFIC DEFENSIVE REINFORCEMENT ------------------
    if opp_troops:
        avg_enemy_x = sum(t.position[0] for t in opp_troops) / len(opp_troops)
        side_offset = random.randint(-15, -5) if avg_enemy_x < 0 else random.randint(5, 15)
        lowest_enemy_y = min(t.position[1] for t in opp_troops)
        defense_y = lowest_enemy_y - 8  # 8 coordinates closer to our tower
        if Troops.valkyrie in my_tower.deployable_troops:deploy_list.list_.append((Troops.valkyrie, (side_offset, lowest_enemy_y)))
        elif Troops.archer in my_tower.deployable_troops: deploy_list.list_.append((Troops.archer, (side_offset + random.randint(-3, 3), defense_y)))
        elif Troops.minion in my_tower.deployable_troops: deploy_list.list_.append((Troops.minion, (side_offset + random.randint(-3, 3), lowest_enemy_y)))
        non_splash_units = {"Knight", "Prince"}
        if any(t.name in non_splash_units for t in opp_troops):
            deploy_list.list_.append((Troops.skeleton, (random_x(-10, 10), 20)))
    
    # ------------------ PHASE 4: AIR SUPPORT ------------------
    air_threats = {"Balloon", "Dragon"}
    if any(troop.name in air_threats for troop in opp_troops):
        deploy_list.list_.append((Troops.dragon, (random_x(-5,5), 20)))
    
    # ------------------ PHASE 5: MELEE OVERWHELM FOR CLOSE ENEMY TROOPS ------------------
    for enemy in opp_troops:
        if enemy.position[1] < 45 and enemy.name not in {"Skeleton", "Barbarian"}:
            melee_troops = [Troops.knight, Troops.prince, Troops.valkyrie, Troops.minion, Troops.dragon, Troops.skeleton]
            for mt in melee_troops:
                if enemy.name.lower() not in ["valkyri","minion","dragon"] and mt == Troops.skeleton:
                    continue
                pos = enemy.position
                if mt in (Troops.archer, Troops.wizard , Troops.dragon):
                    pos = (pos[0], pos[1]-15)
                else:
                    pos=(pos[0],pos[1])
                deploy_list.list_.append((mt, pos))
            break  # Process only the first enemy that meets this condition.
    
    # ------------------ PHASE 6: REACTIVE FALLBACK ------------------
    if team_signal.count("?") >= 4:
        deploy_list.list_.append((Troops.knight, (random_x(-10, 10), 15)))
    
    # ------------------ PHASE 7: ADVANCED POSITIONING: STAGGERED FORMATION ------------------
    if len(deploy_list.list_) >= 3:
        total_x = sum(pos[0] for _, pos in deploy_list.list_)
        total_y = sum(pos[1] for _, pos in deploy_list.list_)
        count = len(deploy_list.list_)
        avg_x = total_x // count if count > 0 else 0
        avg_y = total_y // count if count > 0 else 0
        formation_offsets = [(-5, 0), (0, 0), (5, 0), (-3, -3), (3, -3)]
        offset = formation_offsets[len(deploy_list.list_) % len(formation_offsets)]
        extra_position = (avg_x + offset[0], avg_y + offset[1])
        deploy_list.list_.append((Troops.archer, extra_position))
    
    # ------------------ PHASE 8: ROLLING QUEUE UPDATE ------------------
    current_opp_troops = set(t.name for t in opp_troops)
    prev_opp_troops = set(team_signal.split(","))
    removed_troops = prev_opp_troops - current_opp_troops
    new_troops = current_opp_troops - prev_opp_troops
    signal_list = team_signal.split(",")
    for troop in removed_troops:
        if troop in signal_list:
            signal_list[signal_list.index(troop)] = "?"
    for troop in new_troops:
        if "?" in signal_list:
            signal_list[signal_list.index("?")] = troop
    team_signal = ",".join(signal_list[:9])
    print(f"Predicted Opponent Deck: {signal_list}")
    
    # ------------------ PHASE 9: STANDARD DEPLOYMENT SCORING (FALLBACK) ------------------
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Knight", "Prince", "Barbarian", "Princess"}
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    if count_ground > count_air:
        recommended_counter = "air"
    elif count_air > count_ground:
        recommended_counter = "ground"
    else:
        recommended_counter = None
    
    deployable = my_tower.deployable_troops
    troop_data = {
        Troops.knight:    {"score": 3, "category": "ground"},
        Troops.prince:    {"score": 5, "category": "ground"},
        Troops.wizard:    {"score": 6, "category": "air"},
        Troops.archer:    {"score": 3, "category": "ground"},
        Troops.valkyrie:  {"score": 4, "category": "ground"},
        Troops.minion:    {"score": 2, "category": "air"},
        Troops.skeleton:  {"score": 3, "category": "ground"},
        Troops.dragon:    {"score": 4, "category": "air"}
    }
    bonus = 3
    best_troop = None
    best_score = -1
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop
    if best_troop is not None:
        # For air-targeting units, adjust y coordinate according to enemy positions.
        if opp_troops:
            min_enemy_y = min(opp.position[1] for opp in opp_troops)
        else:
            min_enemy_y = 20
        if best_troop.lower() in ["dragon", "archer", "wizard"]:
            if min_enemy_y > 45:
                pos = (random_x(-5, 5), 20)
            else:
                pos = (random_x(-5, 5), max(min_enemy_y - 120, 20))
        else:
            if min_enemy_y > 45:
                pos = (random_x(-5, 5), 20)
            else:
                pos = (random_x(-5, 5), max(min_enemy_y, 20))
        deploy_list.list_.append((best_troop, pos))
    elif deployable:
        deploy_list.list_.append((deployable[0], (0, 20)))