# from teams.helper_function import Troops, Utils

# team_name = "MUMBAI"
# troops = [Troops.prince,Troops.minion,Troops.archer,Troops.giant,Troops.dragon,Troops.skeleton,Troops.balloon,Troops.barbarian]
# deploy_list = Troops([])
# team_signal = "h"

# def deploy(arena_data:dict):
#     """
#     DON'T TEMPER DEPLOY FUCNTION
#     """
#     deploy_list.list_ = []
#     logic(arena_data)
#     return deploy_list.list_, team_signal

# def logic(arena_data:dict):
#     global team_signal
#     deploy_list.deploy_prince((-16,0))
#     """
#     WRITE YOUR CODE HERE 
#     """

import random
from teams.helper_function import Troops, Utils

team_name = "bioHAZARD"
troops = [
    Troops.wizard, Troops.skeleton, Troops.archer, Troops.prince,
    Troops.dragon, Troops.minion, Troops.valkyrie, Troops.barbarian
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
        Troops.wizard:    {"score": 0, "category": "ground",    "name": "Wizard"},
        Troops.skeleton:    {"score": 7, "category": "ground",    "name": "Skeleton"},
        Troops.archer:    {"score": 12, "category": "ground", "name": "Archer"},
        Troops.prince:     {"score": 10, "category": "ground", "name": "Prince"},
        Troops.dragon:    {"score": 10, "category": "air",    "name": "Dragon"},
        Troops.minion:  {"score": 12, "category": "air", "name": "Minion"},
        Troops.valkyrie:   {"score": 0, "category": "ground",    "name": "Valkyrie"},
        Troops.barbarian: {"score": 10, "category": "ground", "name": "Barbarian"},
        Troops.knight: {"score": 7, "category": "ground", "name": "Knight"}
    }
    
    bonus = 0  # Bonus for matching the recommended counter strategy.
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
    wizard_counter = ["Prince", "Valkyrie","Skeleton"]
    wizard_support =["Knight","Valkyrie","Skeleton","Barbarian","Prince","Dragon","Minion","Wizard"]
    baby_dragon = ["Wizard","Dragon","Musketeer","Archer"]
    
    # --- Deployment Position ---
    #attack
    def attack():
        for i in arena_data["MyTroops"]:
            if i.name=="Wizard":        
                for j in wizard_support:
                    if j in deployable:
                        deploy_list.list_.append((j,(i.position[0],min(i.position[1]+5,50))))
                    
        for i in troops:
            if i is Troops.wizard and i in deployable:
                deploy_list.list_.append((i,(0,10)))
           
    # --- cycle --- 
    def cycle(elixir=7):   
        
        if arena_data["MyTower"].total_elixir >elixir:    
            bonus = 10  # Bonus for matching the recommended counter strategy.
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

            
            if best_troop is not None:
                
                deploy_position = (0, 10)
                deploy_list.list_.append((best_troop, deploy_position))
            else:
                # Fallback: If no deployable troop meets criteria, deploy the first available troop.
                if deployable:
                    deploy_list.list_.append((deployable[0], (0, 0)))

        
    def defense_dragon():
        for i in arena_data["OppTroops"]:
            if i.name == "Dragon":
                for j in baby_dragon:
                    deploy_list.list_.append((j,(i.position[0],i.position[1])))
    def defense_wizard():                  
        for i in arena_data["OppTroops"]:
            if i.name == "Wizard":
                for j in wizard_counter:
                    deploy_list.list_.append((j,i.position))                
        
    # def tower_defense():
    #     for i in arena_data["OppTroops"]:
    #         if i.position[1]<-30:
    #             deploy_list.list_.append()
    
    if len(arena_data["OppTroops"])!=0:
        for i in arena_data["OppTroops"] : 
            if(i.position[1]<20):
                cycle(0)
    
    defense_wizard()
    attack() 
    defense_dragon() 
    cycle()
    
    if arena_data["OppTower"].health <arena_data["MyTower"].health-500:
        #tower_defense()
        return
              
def rescale(x):
    return (x[0],x[1]/2+50)