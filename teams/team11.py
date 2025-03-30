import random
import math
from teams.helper_function import Troops, Utils

team_name = "Shadow_V5"
troops = [
    Troops.minion, Troops.dragon, Troops.valkyrie, Troops.archer,
    Troops.knight, Troops.wizard, Troops.skeleton, Troops.barbarian
]
# Total Elixr cost = 3 + 4 + 4 + 3 + 5 + 5 + 3 + 3 = 30
# Average Elixr cost = 3.75

deploy_list = Troops([])
team_signal = ""

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
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    
    # If game just started, wait for sometime
    if my_tower.game_timer < 1:
        return
    
    elixr = my_tower.total_elixir # Current elixr
    
    deployable = my_tower.deployable_troops # Deployable troops
    
    # List of all troop weakness
    weakness = {
    "Archer": ["everything"],
    "Minion": ["Minion", "Archer", "Musketeer", "Wizard"],
    "Knight": ["everything"],
    "Skeleton": ["Minion", "Skeleton", "Valkyrie", "Dragon", "Wizard"],
    "Dragon": ["Minion", "Dragon", "Wizard", "Archer", "Musketeer"],
    "Valkyrie": ["Minion", "Dragon", "Valkyrie", "Prince", "Wizard"],
    "Musketeer": ["everything"],
    "Giant": ["Minion", "Skeleton", "Barbarian", "Dragon", "Archer", "Musketeer", "Knight", "Valkyrie", "Wizard", "Prince"],
    "Prince": ["Skeleton", "Minion", "Knight", "Prince", "Wizard"], 
    "Barbarian": ["Skeleton", "Barbarian", "Valkyrie", "Minion", "Dragon", "Wizard"],
    "Balloon": ["Minion", "Archer", "Musketeer", "Dragon", "Wizard"],
    "Wizard": ["Skeleton", "Knight", "Valkyrie", "Prince", "Giant", "Wizard"]
    }

    # Elixr data
    elixr_3 = ["Archer", "Knight", "Minion", "Skeleton", "Barbarian"]
    elixr_4 = ["Musketeer", "Valkyrie", "Dragon"]
    elixr_5 = ["Giant", "Balloon", "Prince", "Wizard"]
    
    # List of all close range and far range troops
    close_troops = ["Minion", "Knight", "Skeleton", "Valkyrie", "Prince", "Barbarian"]
    far_troops = ["Archer", "Dragon", "Musketeer", "Wizard"]
    tank_troops = ["Giant", "Balloon"]

    # Getting opponent troop data
    opp_troop_data = {}
    for troop in opp_troops:
        opp_troop_data[troop.name] = troop.position
        
    # Getting my troop data
    my_troop_data = {}
    for troop in my_troops:
        my_troop_data[troop.name] = troop.position
    
    troops_deployed = False # Flag for checking if we have deployed troops

    # Checking weakness and deploying
    offense = True # Is true if we have already reacted to opponent's weakness or ignored it
    for troop_name in opp_troop_data.keys():

        # Check if extremely weak troop is deployed and only deal with it if it gets too close and no other troop is nearby
        troop_nearby = False
        for troop_pos in my_troop_data.values():
            dist = math.sqrt((troop_pos[0] - opp_troop_data[troop_name][0])**2 + (troop_pos[1] - opp_troop_data[troop_name][0])**2)
            if dist <= 10:
                troop_nearby = True
                break

        if weakness[troop_name][0] == "everything":
            if opp_troop_data[troop_name][1] <= 30 and not troop_nearby:
                weakness_defended = False
                # Deploy the troop with the least elixr in the deck
                troops_deployed = True
                for deploy in deployable:
                    if deploy in elixr_3:
                        deploy_list.list_.append((deploy, (opp_troop_data[troop_name][0], opp_troop_data[troop_name][1])))
                        weakness_defended = True
                        break
                if not weakness_defended:
                    for deploy in deployable:
                        if deploy in elixr_4:
                            deploy_list.list_.append((deploy, (opp_troop_data[troop_name][0], opp_troop_data[troop_name][1])))
                            weakness_defended = True
                            break
            else:
                continue
        
        offense = False # We are on defense as opponent is on offense

        # Not react if we have simultaneously dealt with this weakness and some other weakness using some troop if elixr <= 5
        # React if weakness is wizard as wizard is op
        weakness_dealt = False # Flag telling us whether there exists a troop dealing with weakness
        counter_troops = list(set(my_troop_data.keys()) & set(weakness[troop_name]))
        if not counter_troops:
            weakness_dealt = False
        else:
            for counter_troop in counter_troops:
                dist = math.sqrt((my_troop_data[counter_troop][0] - opp_troop_data[troop_name][0])**2 + (my_troop_data[counter_troop][1] - opp_troop_data[troop_name][1])**2)
                if dist <= 18 or (math.fabs(my_troop_data[counter_troop][0] - opp_troop_data[troop_name][0]) <= 12 and my_troop_data[counter_troop][1] < opp_troop_data[troop_name][1]):
                    weakness_dealt = True
                    break
        if weakness_dealt and "Wizard" != troop_name and "Prince" != troop_name:
            if elixr <= 6:
                continue
        
        mirror_deployed = False # Check if we have dealt with weakness

        # Check if we can deal with weakness
        for mirror in weakness[troop_name]:
            if mirror not in deployable:
                continue
            
            mirror_deployed = True
            if my_troop_data:
                y_choice = min(my_troop_data[list(my_troop_data.keys())[0]][1], 50)
            else:
                y_choice = 0
            if opp_troop_data[troop_name][1] <= 40:
                if mirror in close_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], opp_troop_data[troop_name][1])))
                elif mirror in tank_troops:
                    deploy_list.list_.append((mirror, (0, 0)))
                else:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], max(opp_troop_data[troop_name][1]-10, 0))))
            else:
                if mirror in far_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], y_choice)))
                elif mirror in tank_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                else:
                    mirror_deployed = False
        
        if mirror_deployed:
            troops_deployed = True
            
    # Modify team_signal if we have deployed troops
    if troops_deployed:
        team_signal = "Shadow"

    # Go on offensive if we have more elixr
    if elixr >= 9.7 and not troops_deployed:
        offense = True
    
    # Do not go on offensive if we haven't deployed any troops yet
    if not team_signal:
        if my_tower.game_timer > 20:
            offense = True
            team_signal = "Shadow"
        else:
            offense = False

    # If we have dealt with all weaknesses, we shall go on the offensive
    if offense:
        if my_troop_data:
            x_choice = my_troop_data[list(my_troop_data.keys())[0]][0]
            y_choice = min(my_troop_data[list(my_troop_data.keys())[0]][1], 50)
        else:
            x_choice = random.choice((-25, 25))
            y_choice = 0

        # Try to use combos
        combo = False
        if "Wizard" in deployable:
            deploy_list.list_.append(("Wizard", (x_choice, y_choice)))
        elif "Dragon" in deployable:
            deploy_list.list_.append(("Dragon", (x_choice, y_choice)))
        elif "Valkyrie" in deployable:
            deploy_list.list_.append(("Valkyrie", (x_choice, y_choice)))
        else:
            deploy_list.list_.append((deployable[0], (x_choice, y_choice)))
        if not combo:
            deploy_list.list_.append((deployable[0], (x_choice, y_choice)))