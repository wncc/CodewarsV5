import random, math
from teams.helper_function import Troops, Utils

team_name = "Byte_Bandits"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.prince,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]
deploy_list = Troops([])
team_signal = "Wizard_OP!"

def choose_position(arena_data, troop):
    my_speed  = _speed(troop)
    my_range  = _discovery_range(troop)+_size(troop)
    op = [[t.position[0], t.position[1],_speed(t.name)*0.4/3, _discovery_range(t.name)*1.875,_size(t.name)] for t in arena_data["OppTroops"] if t.position[1] > 35]
    init_x = -25
    init_y = 50
    target_x = -5.233
    target_y = 89.74
    res1 = True
    br = False
    while res1 and not br:
        for t in op:
            if (t[0] - init_x)**2 + (t[1] - init_y)**2 <= (max(my_range, t[3])+t[4])**2:
                res1 = False
                break 
            else:
                if (t[1] < init_y):
                    del op[op.index(t)]
                else:
                    t[1] -= t[2]
        init_x += my_speed*(target_x - init_x)/math.sqrt((target_y - init_y)**2 + (target_x - init_x)**2)
        init_y += my_speed*(target_y - init_y)/math.sqrt((target_y - init_y)**2 + (target_x - init_x)**2)
        if (init_y >= target_y):
            br = True
            break
        if len(op) == 0 :
            res1 = True
            break
    res2 = True
    init_x = 25
    init_y = 50
    target_x = 5.233
    target_y = 89.74
    br = False
    op = [[t.position[0], t.position[1],_speed(t.name)*0.4/3, _discovery_range(t.name)*1.875, _size(t.name)] for t in arena_data["OppTroops"] if t.position[1] > 35]
    while res2:
        for t in op:
            if (t[0] - init_x)**2 + (t[1] - init_y)**2 <= (max(my_range, t[3])+t[4])**2:
                res2 = False
                break 
            else:
                if (t[1] < init_y):
                    del op[op.index(t)]
                else:
                    t[1] -= t[2]
        init_x += my_speed*(target_x - init_x)/math.sqrt((target_y - init_y)**2 + (target_x - init_x)**2)
        init_y += my_speed*(target_y - init_y)/math.sqrt((target_y - init_y)**2 + (target_x - init_x)**2)
        if (init_y >= target_y):
            br = True
            break
        if len(op) == 0 :
            res2 = True
            break
    return (res1, res2)

def _speed(troop):
    return {"Archer": 3,"Prince": 5,"Minion": 5,"Wizard": 3,"Giant": 1,"Dragon": 5,"Balloon": 3,"Barbarian": 3,"Knight": 3,"Skeleton": 5,"Valkyrie": 3,"Musketeer": 3,}[troop]

def _discovery_range(troop):
    return {"Archer":8, "Giant":7, "Dragon":5, "Balloon":5, "Prince":5, "Barbarian":5, "Knight":7, "Minion":4, "Skeleton":4, "Wizard":8, "Valkyrie":7, "Musketeer":8}[troop]
def _size(troop):
    sizes = {
        "Archer":    0.15 * 9.375,
        "Barbarian": 0.25 * 9.375,
        "Balloon":   0.4  * 9.375,
        "Dragon":    0.4  * 9.375,
        "Giant":     0.5  * 9.375,
        "Minion":    0.15 * 9.375,
        "Skeleton":  0.15 * 9.375,
        "Valkyrie":  0.2  * 9.375,
        "Wizard":    0.25 * 9.375,
        "Prince":    0.3  * 9.375,
        "Musketeer": 0.2  * 9.375,
        "Knight":    0.3  * 9.375,
    }
    return sizes[troop]

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
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    deployable = my_tower.deployable_troops
    x = 8 if any(Utils.calculate_distance(my_tower, t) < 40 for t in opp_troops) else 6
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    deployable = my_tower.deployable_troops

    troop_data = {
        "Archer":   {"damage": 118*2, "health": 334*2, "attack_range": 5,   "speed": 1,   "elixir": 3},
        "Minion":   {"damage": 129*3, "health": 252*3, "attack_range": 2,   "speed": 1.5, "elixir": 3},
        "Knight":   {"damage": 221, "health": 1938,"attack_range": 0,   "speed": 1,   "elixir": 3},
        "Skeleton": {"damage": 890,  "health": 890,  "attack_range": 0,   "speed": 1,   "elixir": 3},
        "Dragon":   {"damage": 176, "health": 1267,"attack_range": 3.5, "speed": 1,   "elixir": 4},
        "Valkyrie": {"damage": 195, "health": 2097,"attack_range": 0,   "speed": 1,   "elixir": 4},
        "Musketeer": {"damage": 239, "health": 792, "attack_range": 6,   "speed": 1,   "elixir": 4},
        "Giant":    {"damage": 337, "health": 5423,"attack_range": 0,   "speed": 1,   "elixir": 5},
        "Prince":   {"damage": 392, "health": 1920,"attack_range": 0,   "speed": 1,   "elixir": 5},
        "Wizard":   {"damage": 410, "health": 1100,"attack_range": 5.5, "speed": 1,   "elixir": 5},
        "Barbarian": {"damage": 161*3, "health": 736*3, "attack_range": 0,   "speed": 1,   "elixir": 3},
        "Balloon":  {"damage": 424, "health": 2226,"attack_range": 0,   "speed": 1,   "elixir": 5}
    }
    protecting_troops = {
        Troops.archer:    [Troops.skeleton, Troops.barbarian, Troops.valkyrie, Troops.minion, Troops.archer],
        Troops.minion:    [Troops.wizard, Troops.minion, Troops.archer, Troops.dragon, Troops.barbarian],
        Troops.knight:    [Troops.wizard, Troops.skeleton, Troops.barbarian, Troops.valkyrie, Troops.dragon],
        Troops.skeleton:  [Troops.wizard, Troops.valkyrie, Troops.dragon, Troops.archer, Troops.skeleton],
        Troops.dragon:    [Troops.wizard, Troops.dragon, Troops.minion, Troops.archer, Troops.barbarian],
        Troops.valkyrie:  [Troops.wizard, Troops.minion, Troops.barbarian, Troops.archer, Troops.dragon],
        Troops.musketeer: [Troops.wizard, Troops.skeleton, Troops.barbarian, Troops.prince, Troops.minion],
        Troops.giant:     [Troops.wizard, Troops.skeleton,  Troops.minion, Troops.barbarian, Troops.archer],
        Troops.prince:    [Troops.barbarian, Troops.archer, Troops.valkyrie, Troops.skeleton, Troops.minion],
        Troops.barbarian: [Troops.wizard, Troops.skeleton, Troops.valkyrie, Troops.dragon, Troops.minion],
        Troops.balloon:   [Troops.wizard, Troops.minion, Troops.dragon, Troops.archer, Troops.barbarian],
        Troops.wizard:    [Troops.wizard, Troops.skeleton, Troops.barbarian, Troops.valkyrie, Troops.prince]
    }    
    if(my_tower.game_timer <= 5) and len(opp_troops) == 0:
        return
    enemy_near_tower = [
    troop for troop in opp_troops 
        if Utils.calculate_distance(my_tower, troop) <= 23  
    ]
    if enemy_near_tower:
            enemy = max(enemy_near_tower, key=lambda t: t.damage)
            attacking_enemy = []
            for troop in enemy_near_tower:
                attack_range = troop_data[troop.name]["attack_range"]
                if Utils.calculate_distance(my_tower, troop) <= attack_range*1.875:
                    attacking_enemy.append(troop)
            if attacking_enemy:
                enemy = max(attacking_enemy, key=lambda t: t.damage)
            for counter in protecting_troops[enemy.name]:
                if counter in deployable and troop_data[counter]["elixir"] <= my_tower.total_elixir:
                    y=enemy.position[1]-troop_data[counter]["attack_range"]*1.875
                    if(y<0):
                        y=enemy.position[1]+troop_data[enemy.name]["attack_range"]*1.875-0.1
                    deploy_list.list_.append((counter, enemy.position if troop_data[counter]["attack_range"] == 0 else (enemy.position[0], y)))
                    return
    if my_tower.total_elixir < x:
        return
        
    if my_tower.game_timer > 1150:
        best_score = -1
        best_pair = None
        n = len(deployable)
        for i in range(n):
            troop1 = deployable[i]
            candidate_A = None
            best_health = -1
            for j in range(n):
                if i == j:
                    continue
                troop2 = deployable[j]
                if troop_data[troop2]["health"] > best_health:
                    best_health = troop_data[troop2]["health"]
                    candidate_A = troop2
            if candidate_A is not None:
                score_A = 6*troop_data[troop1]["damage"] + troop_data[candidate_A]["health"]
                if score_A > best_score:
                    best_score = score_A
                    best_pair = (troop1, candidate_A)
        if best_pair:
            attack_troop, health_troop = best_pair
            x = random.uniform(-10, 10)
            deploy_list.list_.append((attack_troop, (x, 36)))
            deploy_list.list_.append((health_troop, (x, 37)))
            return

    for troop in [Troops.prince, Troops.dragon, Troops.skeleton, Troops.barbarian]:
        if troop in deployable:
            (a,b) = choose_position(arena_data, troop)
            if a:
                deploy_list.list_.append((troop, (-25, 50)))
                return
            elif b:
                deploy_list.list_.append((troop, (25, 50)))
                return
    
    if Troops.wizard in deployable:
        deploy_list.list_.append((Troops.wizard, (0, 30)))
        return