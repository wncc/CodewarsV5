from teams.helper_function import Troops, Utils
import random
import math

team_name = "HexaMorph"
troops = [Troops.barbarian, Troops.knight, Troops.dragon, Troops.valkyrie, Troops.musketeer, Troops.archer, Troops.giant, Troops.wizard]
team_signal = "h"

deploy_list = Troops([])

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal



def logic(arena_data: dict):
    # Troop Variables
    troops_data = {
    "Archer": {
        "Elixir": 3,
        "Health": 334,
        "Damage": 118,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 5,
        "Splash Range": 0,
        "Attack Speed": "Fast",
        "Targets": ["Air","Ground","Building"],
        "Discovery Range": 8,
        "Number": 2
    },
    "Minion": {
        "Elixir": 3,
        "Health": "252 (single)",
        "Damage": "129 (single)",
        "Velocity": "Fast",
        "Type": "Air",
        "Attack Range": 2,
        "Splash Range": 0,
        "Attack Speed": "Fast",
        "Targets": ["Air","Ground","Building"],
        "Discovery Range": 4,
        "Number": 3
    },
    "Knight": {
        "Elixir": 3,
        "Health": 1938,
        "Damage": 221,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 0,
        "Splash Range": 0,
        "Attack Speed": "Fast",
        "Targets": ["Ground","Building"],
        "Discovery Range": 7,
        "Number": 1
    },
    "Skeleton": {
        "Elixir": 3,
        "Health": 89*10,
        "Damage": 89*10,
        "Velocity": "Fast",
        "Type": "Ground",
        "Attack Range": 0,
        "Splash Range": 0,
        "Attack Speed": "Fast",
        "Targets": ["Ground","Building"],
        "Discovery Range": 4,
        "Number": 10
},
    "Dragon": {
        "Elixir": 4,
        "Health": 1267,
        "Damage": 176,
        "Velocity": "Fast",
        "Type": "Air",
        "Attack Range": 3.5,
        "Splash Range": 1,
        "Attack Speed": "Fast",
        "Targets": ["Ground","Building"],
        "Discovery Range": 5,
        "Number": 1
    },
    "Valkyrie": {
        "Elixir": 4,
        "Health": 2097,
        "Damage": 195,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 0,
        "Splash Range": 1,
        "Attack Speed": "Fast",
        "Targets": ["Ground","Building"],
        "Discovery Range": 7,
        "Number": 1
    },
    "Musketeer": {
        "Elixir": 4,
        "Health": 792,
        "Damage": 239,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 6,
        "Splash Range": 0,
        "Attack Speed": "Medium",
        "Targets": ["Air","Ground","Building"],
        "Discovery Range": 8,
        "Number": 1
    },
    "Giant": {
        "Elixir": 5,
        "Health": 5423,
        "Damage": 337,
        "Velocity": "Slow",
        "Type": "Ground",
        "Attack Range": 0,
        "Splash Range": 0,
        "Attack Speed": "Slow",
        "Targets": ["Building"],
        "Discovery Range": 7,
        "Number": 1
    },
    "Prince": {
        "Elixir": 5,
        "Health": 1920,
        "Damage": 392,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 0,
        "Splash Range": 0,
        "Attack Speed": "Medium",
        "Targets": ["Ground","Building"],
        "Discovery Range": 5,
        "Number": 1
    },
    "Barbarian": {
        "Elixir": 3,
        "Health": 736*3,
        "Damage": 161*3,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 0,
        "Splash Range": 0,
        "Attack Speed": "Medium",
        "Targets": ["Ground","Building"],
        "Discovery Range": 5,
        "Number": 3
    },
    "Balloon": {
        "Elixir": 5,
        "Health": 2226,
        "Damage": 424,
        "Velocity": "Medium",
        "Type": "Air",
        "Attack Range": 0,
        "Splash Range": 0,
        "Attack Speed": "Medium",
        "Targets": ["Building"],
        "Discovery Range": 5,
        "Number": 1
    },
    "Wizard": {
        "Elixir": 5,
        "Health": 1100,
        "Damage": 410,
        "Velocity": "Medium",
        "Type": "Ground",
        "Attack Range": 5.5,
        "Splash Range": 1,
        "Attack Speed": "Fast",
        "Targets": ["Air","Ground","Building"],
        "Discovery Range": 8,
        "Number": 1
    }
}
    # Variable Set-1
    global team_signal
    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_tower = arena_data["OppTower"]
    opp_troops = arena_data["OppTroops"]

    # Variable Set-2
    deployable = my_tower.deployable_troops
    push_priority=["Knight","Valkyrie","Dragon","Barbarian"]
    cover_priority=["Wizard","Dragon","Musketeer","Archer"]
    air_defense_priority=["Dragon","Giant","Knight","Wizard","Muskeeter"]
    ranged_priority=["Wizard","Musketeer","Archer"]
    balloon_priority=["Archer","Musketeer","Wizard"]
    specific_priority=["Dragon","Giant","Balloon","Wizard","Musketeer","Archer"]

    elixir=my_tower.total_elixir
    cost=0


    # Helping Functions
    def tower_in_danger():
        for x in opp_troops:
            if x.position[1] < 40:
                return True
            
    # Logic
    for x in opp_troops:
        if x.name in ranged_priority:
            if "Barbarian" in deployable and (elixir - cost) >= 3 and x.position[1] < 40:
                deploy_position = x.position
                deploy_list.list_.append(("Barbarian",deploy_position))                    
                cost += 3

            else:
                for y in deployable:
                    if y in push_priority and (elixir - cost) >= troops_data[y]["Elixir"] and x.position[1] < 40:
                        deploy_position = x.position
                        deploy_list.list_.append((y, deploy_position))                    
                        cost += troops_data[y]["Elixir"]
                        break
            

                

    for x in opp_troops:
        if x.name == "Dragon":
            for y in deployable:
                if y in air_defense_priority and (elixir - cost) >= troops_data[y]["Elixir"] and x.position[1] < 30:
                    deploy_position = x.position
                    deploy_list.list_.append((y, deploy_position))                    
                    cost += troops_data[y]["Elixir"]
                    break

    for x in opp_troops:
        if x.name =="Giant":
            for y in deployable:
                if y in push_priority and (elixir - cost) >= troops_data[y]["Elixir"] and x.position[1] < 30:
                    deploy_position = x.position
                    deploy_list.list_.append((y, deploy_position))                    
                    cost += troops_data[y]["Elixir"]
                    break

    for x in opp_troops:
        if x.name == "Balloon":
            for y in deployable:
                if y in balloon_priority and (elixir - cost) >= troops_data[y]["Elixir"] and x.position[1] < 40:
                    deploy_position = x.position
                    deploy_list.list_.append((y, deploy_position))                    
                    cost += troops_data[y]["Elixir"]
                    break

    if tower_in_danger():
        for x in opp_troops:
            if x not in specific_priority:
                if "Wizard" in deployable:
                    deploy_list.list_.append(("Wizard",(random_x(-20,20),0)))
                    cost+=5
                else:
                    for y in deployable:
                        if y in cover_priority and (elixir - cost) >= troops_data[y]["Elixir"]:
                            deploy_position = (0,0)
                            deploy_list.list_.append((y, deploy_position))                    
                            cost += troops_data[y]["Elixir"]
                            break
        
   
    # Aggression Logic: if giant is less than 40 distance from tower, deploy troops to cover it
    
    for x in my_troops:
        if x.name == "Giant" and x.position[1] < 70 and x.position[1] > 20:
            no_in_cover=0
            no_in_push=0
            for z in my_troops :
                if z.position[1] < 50:
                    if z.name in cover_priority:
                        no_in_cover+=1
                    if z.name in push_priority:
                        no_in_push+=1
            if "Wizard" in deployable:
                    deploy_list.list_.append(("Wizard",(random_x(-20,20),0)))
                    cost+=5
            else:        
                for y in deployable:
                    if y in cover_priority and (elixir - cost) >= troops_data[y]["Elixir"] and (no_in_cover<2 or no_in_push>=no_in_push):
                        deploy_position = (random_x(-20,20), x.position[1] - 20)
                        deploy_list.list_.append((y, deploy_position))                   
                        cost += troops_data[y]["Elixir"]
                        break
                    
                    else:
                        if y in push_priority and (elixir - cost) >= troops_data[y]["Elixir"] and no_in_push<=2:
                            deploy_position = (random_x(-20,20), x.position[1] - 20)
                            deploy_list.list_.append((y, deploy_position))                    
                            cost += troops_data[y]["Elixir"]
                            break

    # Handling Elixir Overflow

    if(elixir-cost>=9):
        if "Giant" in deployable:
            deploy_list.list_.append(("Giant",(0,0)))
        elif "Wizard" in deployable:
            deploy_list.list_.append(("Wizard",(random_x(-20,20),0)))
        elif "Dragon" in deployable:
            deploy_list.list_.append(("Dragon",(random_x(-20,20),0)))

        else:            
            if deployable[0]!="Barbarian":
                deploy_list.list_.append((deployable[0],(random_x(-25,25),0)))
            else:
                deploy_list.list_.append((deployable[1],(random_x(-25,25),0)))

    
            
        
