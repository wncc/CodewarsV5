import random
import math
from teams.helper_function import Troops, Utils
# from collections import Counter

team_name = "Algorithm Avengers"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.musketeer,
    Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian
]
deploy_list = Troops([])
team_signal = "h, Prince, Knight, Barbarian, Princess"

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)
def get_troop_damage(my_troops, troop_name):
    for troop in my_troops:
        if troop.name == troop_name:
            return troop.damage
    return None  # Return None if troop is not found
def safe_from_wizard(my_tower, opp_troops):
    """
    Check if the Wizard is far enough from my_tower to deploy a low-cost troop.
    Assumes each troop has attributes 'name' and 'position'.
    """
    # Filter opponent troops for Wizards only.
    wizards = [troop for troop in opp_troops if troop.name.strip() == "Wizard"]
    
    # Return True if no Wizard is found.
    if not wizards:
        return True

    # Find the wizard with the minimum distance from my_tower.
    closest_wizard = min(wizards, key=lambda t: distance(t.position, my_tower.position))
    return distance(closest_wizard.position, my_tower.position) > 40
def closest_target(my_tower, opp_troops):
    # Detremine the closest troop to my my_tower within a distance of 30
    closest_troop = None
    closest_distance = 17      # Maximum distance to consider
    for troop in opp_troops:        
        dist = distance(my_tower.position, troop.position)
        if dist < closest_distance:
            closest_distance = dist
            closest_troop = troop
    return closest_troop
def safe(my_tower,opp_troops):
    #check if no troop within 40 of my tower
    for troop in opp_troops:
        if distance(troop.position, my_tower.position) < 40:
            return False
    return True
def combine(my_troops,my_tower,t1,t2):
    #deploy t1 at  the closest instance  of t2
    pos=my_closest_troop_pos(my_troops, t2, my_tower)
    if my_tower.total_elixir >= Troops.troops_data[t1].elixir and t1 in my_tower.deployable_troops:
        deploy_list.list_.append((t1, pos))
        my_tower.total_elixir -= Troops.troops_data[t1].elixir
def no_of_opps_in_arena(opp_troops):
    count = 0
    for troop in opp_troops:
        if check_troop_in_arena(troop):
            count += 1
    return count

def closest_target_dist(my_tower, opp_troops):
    # Find the distance of the tower to the closest opp troop
    closest_distance = 100
    for troop in opp_troops:    
        dist = distance(my_tower.position, troop.position)
        if dist < closest_distance:
            closest_distance = dist
    return closest_distance
def distance(pos1, pos2):
    """Compute Euclidean distance between two points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
def my_closest_troop_pos(my_troopsi,mytroop,my_tower):
    # Find the closest wizard to my tower
    closest_distance = 1000
    closest_troop = (0,50)
    for troop in my_troopsi:
        if troop.position[1]<50: 
            if troop.name == mytroop:
                dist = distance(troop.position, my_tower.position)
                if dist < closest_distance:
                    closest_distance = dist
                    closest_troop = troop.position
    return closest_troop
def continue_deploying_troops(my_tower, my_troops, deploy_list, deploy_area):
    """
    Deploy troops until the total elixir is less than 8 or no Wizard is close to my_tower.
    Assumes each troop has attributes 'name' and 'position'.
    """
    # Check if the total elixir is less than 8.
    
    
    # Deploy a low-cost troop if no Wizard is close to my_tower.
    if "Valkyrie" in my_tower.deployable_troops and my_tower.total_elixir >=4:
        deploy_list.list_.append(("Valkyrie", (random_x(-23,23),25)))
        my_tower.total_elixir -= 4
    elif "Minion" in my_tower.deployable_troops and my_tower.total_elixir >=3:
        deploy_list.list_.append(("Minion", my_closest_troop_pos(my_troops, "Dragon", my_tower)))
        my_tower.total_elixir -= 3
    
    elif "Musketeer" in my_tower.deployable_troops and my_tower.total_elixir >=4:
        deploy_list.list_.append(("Musketeer", (random_x(-23,23),25)))
        my_tower.total_elixir -= 4    
    elif "Archer" in my_tower.deployable_troops and my_tower.total_elixir >=3:
        deploy_list.list_.append(("Archer", my_closest_troop_pos(my_troops, "Skeleton", my_tower)))
        my_tower.total_elixir -= 3    
    elif "Skeleton" in my_tower.deployable_troops and my_tower.total_elixir >=3:
        deploy_list.list_.append(("Skeleton", my_closest_troop_pos(my_troops, "Wizard", my_tower)))
        my_tower.total_elixir -= 3
    elif "Barbarian" in my_tower.deployable_troops and my_tower.total_elixir >=3:
        deploy_list.list_.append(("Barbarian", (random_x(-23,23),25)))
        my_tower.total_elixir -= 3
    elif "Knight" in my_tower.deployable_troops and my_tower.total_elixir >=3:
        deploy_list.list_.append("Knight", (random_x(-23,23),25))
        my_tower.total_elixir -= 3

def try_priorities(my_tower, priorities,target_pos=None):
    """
    Deploy troops based on a list of priorities.
    """
    troops_data= Troops.troops_data
    tpos= my_tower.position
    if target_pos:
        tpos = target_pos
    for troop in priorities:
        if troop in my_tower.deployable_troops and my_tower.total_elixir >=troops_data[troop].elixir:
            deploy_list.list_.append((troop, tpos))
            my_tower.total_elixir -= troops_data[troop].elixir
            return
def check_troop_in_arena(troop):
    """
    Check if a troop is within the arena boundaries.
    """
    return -25 <= troop.position[0] <= 25 and 0 <= troop.position[1] <= 50
def get_closest_enemy_troop(pos, opp_troops,etroop):
    """
    Return the opponent Wizard troop that is closest to your tower.
    Assumes each troop has attributes 'name' and 'position'.
    """
    # Filter opponent troops for Wizards only.
    etroops = [troop for troop in opp_troops if troop.name.strip() == etroop]
    
    # Return None if no Wizard is found.
    if not etroops:
        return None

    # Find the wizard with the minimum distance from my_tower.
    closest_etroop = min(etroops, key=lambda t: distance(t.position, pos))
    return closest_etroop
    
def get_closest_wizard(pos, opp_troops):
    """
    Return the opponent Wizard troop that is closest to your tower.
    Assumes each troop has attributes 'name' and 'position'.
    """
    # Filter opponent troops for Wizards only.
    wizards = [troop for troop in opp_troops if troop.name.strip() == "Wizard"]
    
    # Return None if no Wizard is found.
    if not wizards:
        return None

    # Find the wizard with the minimum distance from my_tower.
    closest_wizard = min(wizards, key=lambda t: distance(t.position, pos))
    return closest_wizard
def get_dynamic_bonus(my_tower, troop, fps=10, base_bonus=2):
    """
    Compute a bonus that increases with game time and available elixir,
    but scales down for high-cost troops when elixir is low.

    - total_game_frames: total frames in 3 minutes (fps * 180).
    - time_ratio: fraction of game time elapsed.
    - elixir_ratio: current elixir relative to maximum (assumed 10).
    - troop_elixir_factor: computed as min(1, my_tower.total_elixir / troop.elixir), 
      but not less than 0.3.
    
    The dynamic bonus is:
         base_bonus * (1 + 0.5 * time_ratio + 0.5 * elixir_ratio) * troop_elixir_factor
    """
    cost_map = {
        "Archer":    3, "Minion": 3, "Knight": 3, "Skeleton": 3,
        "Valkyrie":  4, "Musketeer": 4, "Giant": 5, "Balloon": 5,
        "Wizard":    5, "Dragon": 4, "Prince": 5, "Barbarian": 3
    }
    total_game_frames = fps * 180  # total frames in 3 minutes
    time_ratio = my_tower.game_timer / total_game_frames if hasattr(my_tower, "game_timer") else 0.5
    elixir_ratio = my_tower.total_elixir / 10.0  # assuming maximum elixir is 10
    # Compute the troop elixir factor: if current elixir is low relative to troop cost, bonus is scaled down.
    if troop is None:
        raise ValueError("Troop name is None, but it should never be.")
    
    troop_cost = cost_map[troop.strip()]  # Strip spaces if needed

    # **Compute troop elixir factor**
    troop_elixir_factor = min(2, 1 + my_tower.total_elixir / troop_cost)  
    troop_elixir_factor = max(0.3, troop_elixir_factor)  # Ensure min factor is 0.3

    return base_bonus * (1 + 0.5 * time_ratio + 0.5 * elixir_ratio) + troop_elixir_factor
def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal
def logic(arena_data: dict):
    global team_signal
    fps=10
    # Unpack arena data
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    opp_tower = arena_data["OppTower"]
    my_troops = arena_data["MyTroops"]
    cost_map = {
        "Archer":    3, "Minion": 3, "Knight": 3, "Skeleton": 3,
        "Valkyrie":  4, "Musketeer": 4, "Giant": 5, "Balloon": 5,
        "Wizard":    5, "Dragon": 4, "Prince": 5, "Barbarian": 3
    }
    max_health = 7032  # Fixed maximum health for opponent tower

    # -------------------------------------------------------------------------
    # 1. Update team_signal (kept as a string) for opponent troop history.
    #    We update it using current opponent troops.
    # -------------------------------------------------------------------------
    for troop in opp_troops:
        name = troop.name.strip()
        if name not in team_signal:
            team_signal += ", " + name if team_signal else name
            if len(team_signal) > 200:
                tokens = team_signal.split(", ")
                tokens.pop(0)
                team_signal = ", ".join(tokens)

    # -------------------------------------------------------------------------
    # 2. Compute frequencies for ONLY CURRENT opponent troops using a dictionary.
    # -------------------------------------------------------------------------
    current_opp_counts = {}
    for troop in opp_troops:
        name = troop.name
        current_opp_counts[name] = current_opp_counts.get(name, 0) + 1

    # -------------------------------------------------------------------------
    # 3. Define base scores for each troop type.
    # -------------------------------------------------------------------------
    base_scores = {
        "Archer":    4,
        "Minion":    3,
        "Knight":    3,
        "Skeleton":  2,
        "Valkyrie":  4,
        "Musketeer": 3,
        "Giant":     5,
        "Balloon":   5,
        "Wizard":    5,
        "Dragon":    5,
        "Prince":    5,
        "Barbarian": 3
    }
    
    # -------------------------------------------------------------------------
    # 4. Iterate Over Deployable Troops and Compute Their Scores
    # Each candidate: (troop_name, score, troop_elixir)
    # -------------------------------------------------------------------------
    scored_troops = []
    combo_cost = cost_map["Dragon"] + cost_map["Barbarian"]  # e.g., 4 + 3 = 7

# Check if the opponent troop is a Wizard and if we have enough elixir for the combo.
    ARENA_HEIGHT = 100
    ARENA_WIDTH = 50
    arena_display_size = (ARENA_WIDTH, ARENA_HEIGHT)
    # deploy_area: (min_x, max_x, min_y, max_y)
    deploy_area = (0, arena_display_size[0], arena_display_size[1]/2, arena_display_size[1])  
    # Assume cost_map, opp_troops, my_tower, and deploy_list are defined
#     combo_cost = cost_map["Dragon"] + cost_map["Barbarian"]  # Example: 4 + 3 = 7
    # Check for a Wizard among opponent troops.
    n= no_of_opps_in_arena(opp_troops)
    # if(my_tower.game_timer<50 or 0<opp_tower.health -my_tower.health<0.4*max_health):
    #     try_priorities(my_tower, ["Dragon"],(25,50))
    #     try_priorities(my_tower, ["Valkyrie"],(25,50))
    #     try_priorities(my_tower, ["Wizard"],(25,50))
        
    # try_priorities(my_tower, ["Wizard"],my_tower.position)
    tar = closest_target(my_tower, opp_troops)
    
    closest_wiz = get_closest_enemy_troop(my_tower.position, opp_troops,"Wizard")
    # closest_dragon= get_closest_enemy_troop(my_tower.position, opp_troops,"Dragon")
    if closest_wiz :
        wizard_pos = closest_wiz.position

    if closest_wiz and check_troop_in_arena(closest_wiz):
        try_priorities(my_tower, ["Skeleton","Minion","Valkyrie","Dragon","Barbarian","Musketeer","Knight"],wizard_pos)
    try_priorities(my_tower, ["Wizard"],my_tower.position)
    try_priorities(my_tower, ["Dragon"],my_tower.position)
    # try_priorities(my_tower, ["Valkyrie"],my_tower.position)    
    # if(my_tower.health < 0.4*max_health or  opp_tower.health > 0.8*max_health):
    #     try_priorities(my_tower, ["Wizard"],(0,50))
    #     try_priorities(my_tower, ["Dragon"],(0,50))
   
     # if tar=="Dragon":
    #     try_priorities(my_tower, ["Skeleton","Minion","Barbarian","Dragon","Valkyrie","Archer","Musketeer"],tar.position)
    for troop in opp_troops:
        if ((check_troop_in_arena(troop) and troop=="Dragon") ):
            try_priorities(my_tower, ["Wizard","Dragon"],my_tower.position)
            if troop:
                try_priorities(my_tower, ["Skeleton","Minion","Valkyrie","Barbarian","Musketeer"],troop.position)
            try_priorities(my_tower, ["Archer"],my_tower.position)
    if tar in [ "Minion","Skeleton","Valkyrie","Archer","Musketeer"]:
        try_priorities(my_tower, ["Minion","Skeleton","Wizard","Barbarian","Dragon","Valkyrie","Archer","Musketeer"],tar.position)
    # elif not tar :
    #     try_priorities(my_tower, ["Wizard"],(0,50))
    #     combine(my_troops,my_tower,"Dragon","Wizard")
    #     combine(my_troops,my_tower,"Archer","Wizard")
    #     combine(my_troops,my_tower,"Skeleton","Valkyrie")
    #     combine(my_troops,my_tower,"Minion","Wizard")

    elif not tar or (n<=2 and tar not in ["Dragon", "Wizard","Valkyrie"]):
        try_priorities(my_tower, ["Wizard"], (0, 50))
        combine(my_troops, my_tower, "Dragon", "Wizard")
        combine(my_troops, my_tower, "Archer", "Wizard")
        combine(my_troops, my_tower, "Skeleton", "Valkyrie")
        combine(my_troops, my_tower, "Minion", "Wizard")
#Added the next two lines
    # if my_tower.target=="Dragon":
    #     try_priorities(my_tower, ["Wizard","Skeleton","Minion","Archer","Barbarian","Dragon","Valkyrie","Musketeer"],my_tower.target.position)
    # if my_tower.target  or any((check_troop_in_arena(troop) and troop in ["Dragon", "Wizard", "Giant","Balloon"]) for troop in opp_troops ):
    #     if my_tower.target:
    #         try_priorities(my_tower, ["Wizard","Skeleton","Minion","Barbarian","Dragon","Valkyrie","Archer","Musketeer"],my_tower.target.position)
    #     # try_priorities(my_tower, ["Wizard"],my_tower.position)

    #     for troop in opp_troops:
    #         if check_troop_in_arena(troop) :
    #             try_priorities(my_tower, ["Wizard","Skeleton","Minion","Barbarian","Dragon","Valkyrie","Archer","Musketeer"],troop.position)
  
        
    cost_map = {
        "Archer":    3, "Minion": 3, "Knight": 3, "Skeleton": 3,
        "Valkyrie":  4, "Musketeer": 4, "Giant": 5, "Balloon": 5,
        "Wizard":    5, "Dragon": 4, "Prince": 5, "Barbarian": 3
    }
    if my_tower.total_elixir ==10 and   "Wizard" in my_tower.deployable_troops and "Dragon" in my_tower.deployable_troops:
        deploy_list.list_.append(("Wizard", my_tower.position))
        deploy_list.list_.append(("Dragon",  my_tower.position))

        my_tower.total_elixir-=10
    if "Wizard" in my_tower.deployable_troops and closest_target_dist(my_tower, opp_troops) >= 50 and my_tower.total_elixir <5:
        return
    if "Wizard" in my_tower.deployable_troops and my_tower.total_elixir >=5 and my_tower.health >=0.7*max_health:
        deploy_list.list_.append(("Wizard",(0,50)))
        my_tower.total_elixir-=5
            
    elif "Dragon" in my_tower.deployable_troops and my_tower.total_elixir >=4:
        pos= my_closest_troop_pos(my_troops, "Wizard", my_tower)
        if pos != (0,50): 
            deploy_list.list_.append(("Dragon", pos))
        else:
            deploy_list.list_.append(("Dragon", my_tower.position))
        my_tower.total_elixir-=4    
    
    
    

    
   

        # for troop in my_troops:
        #     combine(my_troops,my_tower,"Minion",troop)
        # for troop in my_troops:
        #     combine(my_troops,my_tower,"Skeleton",troop)    
        # continue_deploying_troops(my_tower, my_troops, deploy_list, deploy_area)