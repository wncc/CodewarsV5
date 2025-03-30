from .helper_function import Troops, Utils


import math
import random

team_name = "TurtleSimps"
troops = [Troops.wizard, Troops.minion, Troops.prince, Troops.knight, 
          Troops.dragon, Troops.skeleton, Troops.valkyrie, Troops.barbarian]
deploy_list = Troops([])  # Correct initialization
team_signal = "1000000"

def counting_enemy_elixir(arena_data):
    global team_signal
    current_elixir = int(team_signal[:2]) + float(team_signal[2:4])/100
    
    game_timer = arena_data["MyTower"].game_timer
    
    if game_timer < 1200:  # First 2 minutes (120s * 10fps)
        elixir_rate = 0.05
    else:  # Last 1 minute (60s * 10fps)
        elixir_rate = 0.1

    # Calculate elixir gained
    if current_elixir<10:
        current_elixir += elixir_rate
    latest_uid = int(team_signal[4:7])
    max_uid = 0
    elixir_deployed = 0
    unique_troops = set([])
    for troop in arena_data["OppTroops"]:
        if troop.uid > latest_uid:
            if troop.name not in unique_troops:
                unique_troops.add(troop.name)
                elixir_deployed += troop.elixir
        max_uid = max(max_uid,troop.uid)
    
    current_elixir -= elixir_deployed
    
    int_part = int(current_elixir)
    float_part = int((current_elixir - int_part)*100)
    team_signal = f"{int_part:02d}" + f"{float_part:02d}" + team_signal[4:]
    team_signal = team_signal[:4] + f"{max_uid:03d}" + team_signal[7:]
    
    return current_elixir+0.3
    
def deploy(arena_data: dict):
    """ 
    DON'T TAMPER WITH DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def compute_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def best_troop(arena_data, enemy):
    counter_troops = {
        "Archer": ["Dragon", "Valkyrie", "Barbarian"],
        "Minion": ["Skeleton", "Dragon", "Minion"],
        "Knight": ["Skeleton", "Dragon", "Wizard"],
        "Skeleton": ["Valkyrie", "Skeleton", "Dragon","Wizard","Barbarian","Knight"],
        "Dragon": ["Dragon", "Wizard", "Minion"],
        "Valkyrie": ["Valkyrie", "Dragon", "Knight"],
        "Musketeer": ["Barbarian", "Knight", "Dragon"],
        "Giant": ["Skeleton", "Wizard", "Minion"],
        "Prince": ["Skeleton", "Dragon", "Wizard"],
        "Barbarian": ["Skeleton","Barbarian", "Dragon"],
        "Balloon": ["Wizard", "Minion", "Dragon"],
        "Wizard": ["Valkyrie", "Wizard", "Knight"]
    }


    distraction_troops=["Dragon", "Minion","Wizard","Knight", "Valkyrie","Barbarian","Skeleton", "Prince"]



    best_troops = counter_troops[enemy.name]
    
    # Deploy the first available counter troop
    for troop in best_troops:
        if troop in arena_data["MyTower"].deployable_troops:  
            return troop  
        elif enemy.target is None:
            for troop in distraction_troops:
                if troop in arena_data["MyTower"].deployable_troops:
                    return troop
    
    return arena_data["MyTower"].deployable_troops[0] 

def dvalue(enemyname):
    troops = {
        "Archer": 354,
        "Minion": 387,
        "Knight": 663,
        "Skeleton": 267,
        "Dragon": 528,
        "Valkyrie": 585,
        "Musketeer": 478,
        "Giant": 337,
        "Prince": 1176,
        "Barbarian": 322,
        "Balloon": 848,
        "Wizard": 1230
    }

    value =troops[enemyname]
    return value
  


    class_attributes={
    "Archer": {
        "name": "Archer",
        "type": "ground",
        "elixir": 3,
        "size": 1.40625,
        "health": 334,
        "damage": 118,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 15.0,
        "number": 2,
        "attack_range": 9.375
    },
    "Barbarian": {
        "name": "Barbarian",
        "type": "ground",
        "elixir": 3,
        "size": 2.34375,
        "health": 736,
        "damage": 161,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 2,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 9.375,
        "number": 3,
        "attack_range": 0
    },
    "Balloon": {
        "name": "Balloon",
        "type": "air",
        "elixir": 5,
        "size": 3.75,
        "health": 2226,
        "damage": 424,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 2,
        "target_type": {"air": False, "ground": False, "building": True},
        "discovery_range": 9.375,
        "number": 1,
        "attack_range": 0
    },
    "Dragon": {
        "name": "Dragon",
        "type": "air",
        "elixir": 4,
        "size": 3.75,
        "health": 1267,
        "damage": 176,
        "speed": 5,
        "splash_range": 1.875,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 9.375,
        "number": 1,
        "attack_range": 6.5625
    },
    "Giant": {
        "name": "Giant",
        "type": "ground",
        "elixir": 5,
        "size": 4.6875,
        "health": 5423,
        "damage": 337,
        "speed": 1,
        "splash_range": 0,
        "attack_speed": 3,
        "target_type": {"air": False, "ground": False, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    },
    "Minion": {
        "name": "Minion",
        "type": "air",
        "elixir": 3,
        "size": 1.40625,
        "health": 252,
        "damage": 129,
        "speed": 5,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 7.5,
        "number": 3,
        "attack_range": 3.75
    },
    "Skeleton": {
        "name": "Skeleton",
        "type": "ground",
        "elixir": 3,
        "size": 1.40625,
        "health": 89,
        "damage": 89,
        "speed": 5,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 7.5,
        "number": 10,
        "attack_range": 0
    },
    "Valkyrie": {
        "name": "Valkyrie",
        "type": "ground",
        "elixir": 4,
        "size": 1.875,
        "health": 2097,
        "damage": 195,
        "speed": 3,
        "splash_range": 1.875,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    },
    "Wizard": {
        "name": "Wizard",
        "type": "ground",
        "elixir": 5,
        "size": 2.34375,
        "health": 1100,
        "damage": 410,
        "speed": 3,
        "splash_range": 1.875,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 15.0,
        "number": 1,
        "attack_range": 10.3125
    },
    "Prince": {
        "name": "Prince",
        "type": "ground",
        "elixir": 5,
        "size": 2.8125,
        "health": 1920,
        "damage": 392,
        "speed": 5,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    },
    "Musketeer": {
        "name": "Musketeer",
        "type": "ground",
        "elixir": 4,
        "size": 1.875,
        "health": 792,
        "damage": 239,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 2,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 15.0,
        "number": 1,
        "attack_range": 11.25
    },
    "Knight": {
        "name": "Knight",
        "type": "ground",
        "elixir": 3,
        "size": 2.8125,
        "health": 1938,
        "damage": 221,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    }
}

    
    if enemy.name in ["Balloon", "Prince","Wizard","Valkyrie","Knight"]:
        distance = compute_distance(enemy.position[0], enemy.position[1], 0, 25)
    #else:
        #distance = compute_distance(enemy.position[0], enemy.position[1], 0, 0)-15
    

    if distance <=18:
        selected_troop = best_troop(arena_data, enemy)
        cls=class_attributes[selected_troop]
        if cls["attack_range"] != 0:
           deploy_distance= cls["attack_range"] + cls["size"] + enemy.size-2
        else: 
            deploy_distance=0


        
        deploy_list.list_.append((selected_troop, (enemy.position[0], enemy.position[1]-deploy_distance)))
        print(f"Deployed {selected_troop} for defence of {enemy.name}")
        return
 

def kill_them_troops(arena_data, enemy):
    class_attributes={
    "Archer": {
        "name": "Archer",
        "type": "ground",
        "elixir": 3,
        "size": 1.40625,
        "health": 334,
        "damage": 118,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 15.0,
        "number": 2,
        "attack_range": 9.375
    },
    "Barbarian": {
        "name": "Barbarian",
        "type": "ground",
        "elixir": 3,
        "size": 2.34375,
        "health": 736,
        "damage": 161,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 2,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 9.375,
        "number": 3,
        "attack_range": 0
    },
    "Balloon": {
        "name": "Balloon",
        "type": "air",
        "elixir": 5,
        "size": 3.75,
        "health": 2226,
        "damage": 424,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 2,
        "target_type": {"air": False, "ground": False, "building": True},
        "discovery_range": 9.375,
        "number": 1,
        "attack_range": 0
    },
    "Dragon": {
        "name": "Dragon",
        "type": "air",
        "elixir": 4,
        "size": 3.75,
        "health": 1267,
        "damage": 176,
        "speed": 5,
        "splash_range": 1.875,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 9.375,
        "number": 1,
        "attack_range": 6.5625
    },
    "Giant": {
        "name": "Giant",
        "type": "ground",
        "elixir": 5,
        "size": 4.6875,
        "health": 5423,
        "damage": 337,
        "speed": 1,
        "splash_range": 0,
        "attack_speed": 3,
        "target_type": {"air": False, "ground": False, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    },
    "Minion": {
        "name": "Minion",
        "type": "air",
        "elixir": 3,
        "size": 1.40625,
        "health": 252,
        "damage": 129,
        "speed": 5,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 7.5,
        "number": 3,
        "attack_range": 3.75
    },
    "Skeleton": {
        "name": "Skeleton",
        "type": "ground",
        "elixir": 3,
        "size": 1.40625,
        "health": 89,
        "damage": 89,
        "speed": 5,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 7.5,
        "number": 10,
        "attack_range": 0
    },
    "Valkyrie": {
        "name": "Valkyrie",
        "type": "ground",
        "elixir": 4,
        "size": 1.875,
        "health": 2097,
        "damage": 195,
        "speed": 3,
        "splash_range": 1.875,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    },
    "Wizard": {
        "name": "Wizard",
        "type": "ground",
        "elixir": 5,
        "size": 2.34375,
        "health": 1100,
        "damage": 410,
        "speed": 3,
        "splash_range": 1.875,
        "attack_speed": 1,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 15.0,
        "number": 1,
        "attack_range": 10.3125
    },
    "Prince": {
        "name": "Prince",
        "type": "ground",
        "elixir": 5,
        "size": 2.8125,
        "health": 1920,
        "damage": 392,
        "speed": 5,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    },
    "Musketeer": {
        "name": "Musketeer",
        "type": "ground",
        "elixir": 4,
        "size": 1.875,
        "health": 792,
        "damage": 239,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 2,
        "target_type": {"air": True, "ground": True, "building": True},
        "discovery_range": 15.0,
        "number": 1,
        "attack_range": 11.25
    },
    "Knight": {
        "name": "Knight",
        "type": "ground",
        "elixir": 3,
        "size": 2.8125,
        "health": 1938,
        "damage": 221,
        "speed": 3,
        "splash_range": 0,
        "attack_speed": 1,
        "target_type": {"air": False, "ground": True, "building": True},
        "discovery_range": 13.125,
        "number": 1,
        "attack_range": 0
    }
}

    
    if enemy.name in ["Dragon", "Minion","Barbarian","Musketeer","Archer"]:
        distance = compute_distance(enemy.position[0], enemy.position[1], 0, 0)
    #else:
        #distance = compute_distance(enemy.position[0], enemy.position[1], 0, 0)-15
    

        if distance <= enemy.attack_range + enemy.size + arena_data["MyTower"].size +6 :
            selected_troop = best_troop(arena_data, enemy)
            cls=class_attributes[selected_troop]
            if cls["attack_range"] != 0:
                deploy_distance= cls["attack_range"] + cls["size"] + enemy.size-2
            else: 
                deploy_distance=0
            deploy_list.list_.append((selected_troop, (enemy.position[0], enemy.position[1]-deploy_distance)))
    
    
    
    if enemy.name in ["Balloon", "Prince","Wizard","Valkyrie","Knight"]:
        distance = compute_distance(enemy.position[0], enemy.position[1], 0, 25)
    #else:
        #distance = compute_distance(enemy.position[0], enemy.position[1], 0, 0)-15
    

        if distance <=18:
            selected_troop = best_troop(arena_data, enemy)
            cls=class_attributes[selected_troop]
            if cls["attack_range"] != 0:
                deploy_distance= cls["attack_range"] + cls["size"] + enemy.size-2
            else: 
                deploy_distance=0
            deploy_list.list_.append((selected_troop, (enemy.position[0], enemy.position[1]-deploy_distance)))



    if enemy.name== "Skeleton":
        distance = compute_distance(enemy.position[0], enemy.position[1], 0, 0)
        if distance <= enemy.attack_range + enemy.size + arena_data["MyTower"].size +10:
            selected_troop = best_troop(arena_data, enemy)
            cls=class_attributes[selected_troop]
            if cls["attack_range"] != 0:
                deploy_distance= cls["attack_range"] + cls["size"] + enemy.size-2
            else: 
                deploy_distance=0
            deploy_list.list_.append((selected_troop, (enemy.position[0], enemy.position[1]-deploy_distance)))

    return


def killing_giant(arena_data, enemy):
    selected_troop=best_troop(arena_data,enemy)
    deploy_list.list_.append((selected_troop, (enemy.position[0],50)))
    print(f"Deployed {selected_troop} to attack Giant")
    return






def attack(arena_data):
    wizard_troops=["Valkyrie", "Dragon", "Knight", "Barbarian", "Minion", "Prince"]
    prince_troops=[ "Dragon", "Valkyrie", "Knight", "Minion", "Barbarian", "Wizard"]
    dragon_troops=["Knight", "Minion", "Valkyrie", "Barbarian"]
    enemy_elixir= counting_enemy_elixir(arena_data)

    if enemy_elixir>=7:
        count=0
        x=random.choice([-25,25])
        for troop in arena_data["MyTower"].deployable_troops:
            if count<2:
                deploy_list.list_.append((troop, (x,50)))
                count+=1

    elif "Wizard" in arena_data["MyTower"].deployable_troops and arena_data["MyTower"].total_elixir>=8:
        for t in wizard_troops:
            if t in arena_data["MyTower"].deployable_troops:
                if t in ["Dragon", "Valkyrie"] and arena_data["MyTower"].total_elixir>=9:
                    x=random.choice([-25,25])
                    deploy_list.list_.append((t, (x,50)))
                    print(f"Wizard + {t}")
                    deploy_list.list_.append(("Wizard", (x,50)))
                    return
                elif t in ["Knight", "Barabrian","Minion","Skeleton"]:
                    x=random.choice([-25,25])
                    deploy_list.list_.append((t, (x,50)))
                    print(f"Wizard + {t}")
                    deploy_list.list_.append(("Wizard", (x,50)))
                    return


    elif "Prince" in arena_data["MyTower"].deployable_troops and arena_data["MyTower"].total_elixir>=8:
        for t in prince_troops:
            if t in arena_data["MyTower"].deployable_troops:
                if t in ["Dragon", "Valkyrie"] and arena_data["MyTower"].total_elixir>=9:
                    x=random.choice([-25,25])
                    deploy_list.list_.append((t, (x,50)))
                    print(f"Prince + {t}")
                    deploy_list.list_.append(("Prince", (x,50)))
                    return
                elif t in ["Knight", "Barabrian","Minion","Skeleton"]:
                    x=random.choice([-25,25])
                    deploy_list.list_.append((t, (x,50)))
                    print(f"Prince+ {t}")
                    deploy_list.list_.append(("Prince", (x,50)))
                    return


    elif "Dragon" in arena_data["MyTower"].deployable_troops and arena_data["MyTower"].total_elixir>=7:
        for t in dragon_troops:
            if t in arena_data["MyTower"].deployable_troops:
                x=random.choice([-25,25])
                deploy_list.list_.append((t, (x,50)))
                print(f"Dragon+ {t}")
                deploy_list.list_.append(("Dragon", (x,50)))
                return
    elif arena_data["MyTower"].total_elixir>=8:
        x=random.choice([-25,25])
        deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0], (x,50)))
        deploy_list.list_.append((arena_data["MyTower"].deployable_troops[1], (x,50)))

            

def sending_reinforcements(arena_data):
    Light=[ "Dragon", "Minion","Valkyrie","Knight","Skeleton","Barbarian"]

    Heavy=["Prince", "Wizard"]
    total_health=0
    for my_troop in arena_data["MyTroops"]:
        if 70<=my_troop.position[1]<=100:
            total_health+=my_troop.health

    for my_troop in arena_data["MyTroops"]:
        if 70<=my_troop.position[1]<=100 and total_health>=350:
            if arena_data["MyTower"].total_elixir>=5.7:
                for t in Heavy:
                    deploy_list.list_.append((t, (random.randint(-10,10),50)))
                    print(f"Sending{t} as reinforcement")
                    return
            elif arena_data["MyTower"].total_elixir>=5:
                for l in Light:
                    deploy_list.list_.append((l,((random.randint(-10,10),50))))
                    print(f"Sending{l} as reinforcement")
                    return

          
                
      



def logic(arena_data: dict):
    global team_signal
    attack_bool = True
    enemy_elixir= counting_enemy_elixir(arena_data)

    wizard_troops=["Valkyrie", "Dragon", "Knight", "Barbarian", "Minion", "Skeleton", "Prince"]
    prince_troops=["Skeleton", "Dragon", "Valkyrie", "Knight", "Minion", "Barbarian", "Wizard"]
    dragon_troops=["Knight", "Minion", "Valkyrie", "Barbarian", "Skeleton"]
    health={
    "Barbarian":736,
 
    "Dragon": 1267,

    "Minion": 252,

    "Skeleton": 89,

    "Valkyrie": 2097,

    "Wizard":  1100,

    "Prince": 1920,

    "Knight": 1938
}
    if arena_data["MyTower"].total_elixir>=9:
        attack_bool=True
    
    
    enemy_health=0
    for enemy in arena_data["OppTroops"]:
        if enemy.position[1]<=48:
            enemy_health+=enemy.health
    if enemy_health>=150:
        attack_bool=False

    for enemy in arena_data["OppTroops"]:
        if enemy.name=="Giant" and enemy.position[1]<=60:
            killing_giant(arena_data,enemy)
            if arena_data["MyTower"].total_elixir>=4:
                attack_bool=True
            else:
                attack_bool=False
        elif enemy.name=="Prince" and enemy.position[1]<=50:
            attack_bool=False
        elif enemy.name=="Wizard" and enemy.position[1]<=35:
            attack_bool=False
        elif enemy.name=="Balloon" and enemy.position[1]<=50:
            attack_bool=False



    if arena_data["MyTower"].total_elixir<=4:
        attack_bool=False

    if attack_bool:

        incoming_troops=[]
        incoming_troops_usage=[]
        if enemy_elixir<=3:
            for troop in arena_data["MyTroops"]:
                if 47<troop.position[1]<55 and troop.health>=0.6*health[troop.name]:
                    incoming_troops.append(troop)
                    incoming_troops_usage.append(1)
            i=0
            for troop in incoming_troops:
                x=troop.position[0]  
                if troop.name=="Wizard":
                    for t in wizard_troops:
                        if t in arena_data["MyTower"].deployable_troops:
                            deploy_list.list_.append((t, (x,50)))
                            incoming_troops_usage[i]=0

                elif troop.name=="Prince":
                    for t in prince_troops:
                        if t in arena_data["MyTower"].deployable_troops:
                            deploy_list.list_.append((t, (x,50)))
                            incoming_troops_usage[i]=0
                elif troop.name=="Dragon":
                    for t in dragon_troops:
                        if t in arena_data["MyTower"].deployable_troops:
                            deploy_list.list_.append((t, (x,50)))
                            incoming_troops_usage[i]=0                        

                i=i+1

            secondary=False
            for y in incoming_troops_usage:
                if y==0:
                    secondary=True

            attempt1=["Wizard", "Prince"]
            attempt2=["Dragon","Valkyrie","Knight","Minions","Barbarians"]

            if secondary is False:
                for troop in incoming_troops:
                    x=troop.position[0]
                    success=False
                    if arena_data["MyTower"].total_elixir>7:
                        for t in attempt1:
                            if t in arena_data["MyTower"].deployable_troops:
                                deploy_list.list_.append((t, (x,50)))
                                success=True
                    if 3<arena_data["MyTower"].total_elixir and success==False:
                        for t in attempt2:
                            if t in arena_data["MyTower"].deployable_troops:
                                deploy_list.list_.append((t, (x,50)))
                                success=True

        else:
            attack(arena_data)
            sending_reinforcements(arena_data)


        
        
        
    
    
    
    else:
        for enemy in arena_data["OppTroops"]:
            kill_them_troops(arena_data, enemy)
           


        

   

    

    


 


    
    
    
  
    


    