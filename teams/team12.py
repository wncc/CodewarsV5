import random
from teams.helper_function import Troops, Utils
team_name = "NahiKarniCoding"
troops = [
    Troops.wizard, Troops.minion, Troops.prince, Troops.archer,
    Troops.dragon, Troops.knight, Troops.valkyrie, Troops.skeleton
]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def x_notcenter(min_val=0, max_val=1):
    if random.randint(0,1) == 0:
        return random.randint(-25, -8)
    else:
        return random.randint(9, 25)
def send_lane(lane):
    if lane == 0:
        return x_center()
    elif lane == -1:
        return x_left()
    else:
        return x_right()
def send_max_lane(max_lane):
    if max_lane == 0:
        return x_center()
    elif max_lane == -1:
        return x_left()
    else:
        return x_right()
def corners(min_val=0,max_val=1):
    if random.randint(0, 1)==0:
        return -25
    else:
        return 25
def x_left(min_val=-25, max_val=-8):
    return random.randint(min_val, max_val)
def x_center(min_val=-8, max_val=8):
    return random.randint(min_val, max_val)
def x_right(min_val=8, max_val=25):
    return random.randint(min_val, max_val)
def y_top(min_val=34, max_val=50):
    return random.randint(min_val, max_val)
def y_center(min_val=17, max_val=34):
    return random.randint(min_val, max_val)
def y_bottom(min_val=0, max_val=17):
    return random.randint(min_val, max_val)
def same_lane(x):
    if x <= -8:
        return x_left()
    elif x <= 8:
        return x_center()
    else:
        return x_right()

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    min_total_elixir = 2
    Emergency = False

    current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
    deployable = my_tower.deployable_troops
    fail_safe_elixir = 2

    #check for lane with min_OPPTroops elixir
    lane,elixir_left,elixir_right,elixir_center,max_lane=0,0,0,0,0 
    for opp in opp_troops:
        if opp.position[0] <=-8:
            if opp.name == "Archer":
                elixir_left+=(opp.elixir)/2
            elif opp.name == "Skeleton":
                elixir_left += (opp.elixir)/10
            elif opp.name == "Minion":
                elixir_left += (opp.elixir)/3
            elif opp.name == "Barbarian":
                elixir_left += (opp.elixir)/3
            else:
                elixir_left += (opp.elixir)
        elif opp.position[0] <= 8:
            if opp.name == "Archer":
                elixir_center+=(opp.elixir)/2
            elif opp.name == "Skeleton":
                elixir_center += (opp.elixir)/10
            elif opp.name == "Minion":
                elixir_center += (opp.elixir)/3
            elif opp.name == "Barbarian":
                elixir_center += (opp.elixir)/3
            else:
                elixir_center += (opp.elixir)
        else:
            if opp.name == "Archer":
                elixir_right+=(opp.elixir)/2
            elif opp.name == "Skeleton":
                elixir_right += (opp.elixir)/10
            elif opp.name == "Minion":
                elixir_right += (opp.elixir)/3
            elif opp.name == "Barbarian":
                elixir_right += (opp.elixir)/3
            else:
                elixir_right += (opp.elixir)
    if elixir_left<=elixir_center and elixir_left<=elixir_right:
        lane=-1
        if elixir_center<=elixir_right:
            max_lane=1
        else:
            max_lane=0
    elif elixir_center<=elixir_left and elixir_center<=elixir_right:
        lane=0
        if elixir_left<=elixir_right:
            max_lane=1  
        else:
            max_lane=-1
    else:
        lane=1
        if elixir_left<=elixir_center:
            max_lane=0
        else:
            max_lane=-1
    total_elixir=int(my_tower.total_elixir)
    total_enemy_elixir = elixir_right + elixir_left + elixir_center    
    
    ### AGGRESSION

    #MAJOR ATTACK
    if total_elixir >= 10 and total_enemy_elixir <= 5 :
        ##Send a strong attacker and a ranged support
        if Troops.wizard in deployable and Troops.dragon in deployable:
            deploy_list.list_.append((Troops.wizard, (send_lane(lane), 50))) 
            deploy_list.list_.append((Troops.dragon, (send_lane(lane), 50)))
        elif Troops.wizard in deployable and Troops.knight in deployable:
            deploy_list.list_.append((Troops.wizard, (send_lane(lane), 50))) 
            deploy_list.list_.append((Troops.knight, (send_lane(lane), 50)))
        elif Troops.wizard in deployable and Troops.valkyrie in deployable:
            deploy_list.list_.append((Troops.wizard, (send_lane(lane), 50))) 
            deploy_list.list_.append((Troops.valkyrie, (send_lane(lane), 50)))
        elif Troops.wizard in deployable and Troops.minion in deployable:
            deploy_list.list_.append((Troops.wizard, (send_lane(lane), 50))) 
            deploy_list.list_.append((Troops.minion, (send_lane(lane), 50)))
        elif Troops.prince in deployable:
            if Troops.minion in deployable:
                deploy_list.list_.append((Troops.prince, (send_lane(lane), 50)))
                deploy_list.list_.append((Troops.minion, (send_lane(lane), 50)))
            elif Troops.skeleton in deployable:
                deploy_list.list_.append((Troops.prince, (send_lane(lane), 50)))
                deploy_list.list_.append((Troops.skeleton, (send_lane(lane), 50)))
            if Troops.dragon in deployable:
                deploy_list.list_.append((Troops.prince, (send_lane(lane), 50)))
                deploy_list.list_.append((Troops.dragon, (send_lane(lane), 50)))                 
                
    #if total_elixir >= 9 and total_enemy_elixir <= 10 and total_enemy_elixir >=5 and Troops.giant or Troops.wizard not in opp_troops:
    #    #sendsomething at the back
    #    if Troops.dragon in deployable:
    #        deploy_list.list_.append((Troops.dragon, (send_lane(lane), y_bottom())))
    #    elif Troops.valkyrie in deployable:
    #        deploy_list.list_.append((Troops.valkyrie, (send_lane(lane), y_bottom())))
    #    elif Troops.prince in deployable:
    #        deploy_list.list_.append((Troops.prince, (send_lane(lane), y_bottom())))


    #ATTACK - sending support troop
    team_signal = ",".join(current_names)
    for troop in my_troops:
        if troop.name == "Wizard" and troop.position[1] >= 50:
            if Troops.dragon in deployable and total_elixir >= 4+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.dragon, (troop.position[0],troop.position[1] - 4)))
            elif Troops.knight in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.knight, (troop.position[0], troop.position[1])))
            elif Troops.valkyrie in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.valkyrie, (troop.position[0], troop.position[1])))
            elif Troops.minion in deployable and total_elixir >= 3:
                deploy_list.list_.append((Troops.minion, (troop.position[0],troop.position[1]-4)))
            elif Troops.skeleton in deployable and  total_elixir >= 3 + min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.skeleton, troop.position))
           
        if troop.name == "Prince" and troop.position[1] >= 50:
            if Troops.minion in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.minion, (troop.position[0],troop.position[1]-4)))
            elif Troops.skeleton in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.skeleton, (troop.position[0],troop.position[1]-4)))
            if Troops.dragon in deployable and total_elixir >= 4+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.dragon, (troop.position[0],troop.position[1]-4)))
        if troop.name == "Dragon" and troop.position[1] >= 50:
            if Troops.minion in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.minion, (troop.position[0],troop.position[1]-4)))
            elif Troops.skeleton in deployable and total_elixir >= 3+min_total_elixir and  total_enemy_elixir <= 9:
                deploy_list.list_.append((Troops.skeleton, (troop.position[0],troop.position[1]-4)))
        if troop.name == "Valkyrie" and troop.position[1] >= 50:
            if Troops.dragon in deployable and total_elixir >= 4+min_total_elixir and total_enemy_elixir <= 8:
                deploy_list.list_.append((Troops.dragon, (troop.position[0],troop.position[1]-4)))
            elif Troops.wizard in deployable and total_elixir >= 5+min_total_elixir and total_enemy_elixir <= 8:
                deploy_list.list_.append((Troops.wizard, (troop.position[0],troop.position[1]-4)))
        if troop.name == "Knight" and troop.position[1] >= 50:
            if Troops.minion in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 8:
                deploy_list.list_.append((Troops.minion, (troop.position[0],troop.position[1]-4)))
            elif Troops.archer in deployable and total_elixir >= 3+min_total_elixir and total_enemy_elixir <= 5:
                deploy_list.list_.append((Troops.archer, (troop.position[0],troop.position[1]-4)))
            elif Troops.dragon in deployable and total_elixir >= 4+min_total_elixir and total_enemy_elixir <= 6:
                deploy_list.list_.append((Troops.dragon, (troop.position[0],troop.position[1]-4)))
            elif Troops.wizard in deployable and total_elixir >= 5+min_total_elixir and total_enemy_elixir <= 6:
                deploy_list.list_.append((Troops.wizard, (troop.position[0],troop.position[1]-4)))

        

    ##### DEFENCE ####
    for opp_troop in opp_troops:



        if ((opp_troop.name=="Giant" and opp_troop.position[1] <= 50) or (opp_troop.name=="Balloon" and opp_troop.position[1] <= 50)):
            Emergency = True
            min_total_elixir = 0
        if total_enemy_elixir >= 12 and opp.position[1] <= 50:
            Emergency = True
            min_total_elixir = 0
        if (opp.position[1]<25):
            Emergency=True
            min_total_elixir=0
            


        #Base Counter against every troop
        if str(opp_troop.uid) not in current_names:
            if opp_troop.name ==  "Prince" and opp_troop.position[1] < 50:
                if(Troops.skeleton in deployable and total_elixir >=3+min_total_elixir):
                    deploy_list.list_.append((Troops.skeleton, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.dragon in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-2)))
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-5)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and (Troops.archer in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-9)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and(Troops.minion in deployable and total_elixir >=3):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and (Troops.dragon in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and(Troops.valkyrie in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0],opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and (Troops.archer in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=3+min_total_elixir) and(Troops.minion in deployable and total_elixir >=3):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=3+min_total_elixir) and(Troops.dragon in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.minion in deployable and total_elixir >=3+min_total_elixir)and(Troops.archer in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-10)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.minion in deployable and total_elixir >=3+min_total_elixir)and(Troops.dragon in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-5)))
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and (Troops.archer in deployable and total_elixir >=4):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-6)))
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-10)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and (Troops.archer in deployable and total_elixir >=4) and Troops.archer not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-14)))
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and my_tower.total_elixir >=9+min_total_elixir) and (Troops.wizard in deployable and total_elixir >=9)):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-10)))
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.minion in deployable and total_elixir >=3+min_total_elixir) and (Troops.minion in deployable and total_elixir >=3):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-10)))
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            if opp_troop.name == "Wizard" and opp_troop.position[1] < 50:
                if(Troops.knight in deployable and total_elixir >=3+min_total_elixir):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.knight in deployable and total_elixir >=3+min_total_elixir) and Troops.archer in deployable and total_elixir >=6):
                    deploy_list.list_.append(("Knight", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Archer", (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and (Troops.minion in deployable and total_elixir) >=6:
                    deploy_list.list_.append(("Knight", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Minion", (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and (Troops.dragon in deployable and total_elixir >=7):
                    deploy_list.list_.append(("Knight", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Dragon", (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and (Troops.archer in deployable and total_elixir >=7):
                    deploy_list.list_.append(("Valkyrie", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Archer", (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and (Troops.minion in deployable and total_elixir >=7):
                    deploy_list.list_.append(("Valkyrie", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Minion", (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and (Troops.dragon in deployable and total_elixir >=8):
                    deploy_list.list_.append(("Valkyrie", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Dragon", (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append(("Wizard", (opp_troop.position[0], opp_troop.position[1]-10)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.prince in deployable and total_elixir >=5+min_total_elixir) and Troops.prince not in my_troops):
                    deploy_list.list_.append(("Prince", (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.minion in deployable and total_elixir >=3+min_total_elixir) and (Troops.dragon in deployable and total_elixir >=4):
                    deploy_list.list_.append(("Minion", (opp_troop.position[0], opp_troop.position[1]-3)))
                    deploy_list.list_.append(("Dragon", (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.archer in deployable and total_elixir >=4+min_total_elixir) and (Troops.dragon in deployable and total_elixir >=4):
                    deploy_list.list_.append(("Archer", (opp_troop.position[0], opp_troop.position[1]-8)))
                    deploy_list.list_.append(("Dragon", (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)        
                elif(Troops.minion in deployable and total_elixir >=3+min_total_elixir) and (Troops.archer in deployable and total_elixir >=4):
                    deploy_list.list_.append(("Minion", (opp_troop.position[0], opp_troop.position[1]-3)))
                    deploy_list.list_.append(("Archer", (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.knight in deployable and total_elixir >=3+min_total_elixir) and (Troops.valkyrie in deployable and total_elixir >=4):
                    deploy_list.list_.append(("Knight", (opp_troop.position[0], opp_troop.position[1])))
                    deploy_list.list_.append(("Valkyrie", (opp_troop.position[0], opp_troop.position[1]-1.5)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif (Troops.knight in deployable and total_elixir >=3)+min_total_elixir:
                    deploy_list.list_.append(("Knight", (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir):
                    deploy_list.list_.append(("Valkyrie", (opp_troop.position[0], opp_troop.position[1]-1.5)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            if opp_troop.name == "Knight" and opp_troop.position[1] < 35:
                if((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0],opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(Troops.skeleton in deployable and total_elixir >=3+min_total_elixir):
                    deploy_list.list_.append((Troops.skeleton, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.knight in deployable and total_elixir >=3+min_total_elixir) and Troops.knight not in my_troops):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and Troops.valkyrie not in my_troops):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1]-9)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.prince in deployable and total_elixir >=5+min_total_elixir) and Troops.prince not in my_troops):
                    deploy_list.list_.append((Troops.prince, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-30)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            if opp_troop.name == "Valkyrie" and opp_troop.position[1] < 35:
                if((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-4)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-5)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-30)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.knight in deployable and total_elixir >=3+min_total_elixir) and Troops.knight not in my_troops):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1]-8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.archer in deployable and total_elixir >=3+min_total_elixir) and Troops.archer not in my_troops):
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-30)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)                
            if opp_troop.name == "Minion" and opp_troop.position[1] < 50:
                if(Troops.archer in deployable and total_elixir >=3+min_total_elixir):
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-30)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)                    
                if((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-10)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-30)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            if opp_troop.name == "Dragon" and opp_troop.position[1] <= 50:
                if((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.archer in deployable and total_elixir >=4+min_total_elixir) and Troops.archer not in my_troops):
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0],5)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], 15)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0],10 )))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            
            if opp_troop.name == "Skeleton" and opp_troop.position[1] < 50:
                if((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and Troops.valkyrie not in my_troops):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1]-10)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], opp_troop.position[1]-25)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.skeleton in deployable and total_elixir >=3+min_total_elixir) and Troops.skeleton not in my_troops):
                    deploy_list.list_.append((Troops.skeleton, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                    
            if opp_troop.name == "Barbarian" and opp_troop.position[1] < 50:
                if((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and Troops.valkyrie not in my_troops):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1]-15)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0],opp_troop.position[1]-20 )))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                
            if opp_troop.name == "Archer" and opp_troop.position[1] < 50:
                if((Troops.knight in deployable and total_elixir >=3+min_total_elixir) and Troops.knight not in my_troops):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0],opp_troop.position[1] )))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and Troops.valkyrie not in my_troops):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.wizard in deployable and total_elixir >=5+min_total_elixir) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], 8)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            
            if opp_troop.name == "Musketeer" and opp_troop.position[1] < 50:
                if((Troops.knight in deployable and total_elixir >=3+min_total_elixir) and Troops.knight not in my_troops):
                    deploy_list.list_.append((Troops.knight, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.minion in deployable and total_elixir >=3+min_total_elixir) and Troops.minion not in my_troops):
                    deploy_list.list_.append((Troops.minion, (opp_troop.position[0], opp_troop.position[1]-3)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.archer in deployable and total_elixir >=3+min_total_elixir) and Troops.archer not in my_troops):
                    deploy_list.list_.append((Troops.archer, (opp_troop.position[0], opp_troop.position[1]-10)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.valkyrie in deployable and total_elixir >=4+min_total_elixir) and Troops.valkyrie not in my_troops):
                    deploy_list.list_.append((Troops.valkyrie, (opp_troop.position[0], opp_troop.position[1])))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.dragon in deployable and total_elixir >=4+min_total_elixir) and Troops.dragon not in my_troops):
                    deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], opp_troop.position[1]-6)))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            if opp_troop.name == "Giant" and opp_troop.position[1] < 50:
                Emergency = True
                min_total_elixir = 0
                if (("Prince" in deployable and total_elixir >=5) and Troops.prince not in my_troops):
                    deploy_list.list_.append(("Prince", (opp_troop.position[0], y_top())))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(("Wizard" in deployable and total_elixir >=5) and Troops.wizard not in my_troops):
                    deploy_list.list_.append(("Wizard", (opp_troop.position[0], y_center())))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(("Minion" in deployable and total_elixir >=3) and Troops.minion not in my_troops):
                    deploy_list.list_.append(("Minion", (opp_troop.position[0], y_top())))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(("Dragon" in deployable and total_elixir >=4) and Troops.dragon not in my_troops):
                    if(("Archer" in deployable and total_elixir >=3) and Troops.archer not in my_troops):
                        deploy_list.list_.append(("Archer", (opp_troop.position[0], y_bottom())))
                        deploy_list.list_.append(("Dragon", (opp_troop.position[0], y_top())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                    else:
                        deploy_list.list_.append(("Dragon", (opp_troop.position[0], y_top())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif(("Archer" in deployable and total_elixir >=3) and Troops.archer not in my_troops):
                    deploy_list.list_.append(("Archer", (opp_troop.position[0], y_bottom())))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
            if opp_troop.name == "Balloon"and opp_troop.position[1] < 50:
                Emergency = True
                min_total_elixir = 0
                if((Troops.wizard in deployable and total_elixir >=5) and Troops.wizard not in my_troops):
                    deploy_list.list_.append((Troops.wizard, (opp_troop.position[0], y_center())))
                    team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.minion in deployable and total_elixir >=3) and Troops.dragon not in my_troops):
                    if((Troops.dragon in deployable and total_elixir >=4) and Troops.minion not in my_troops):
                        deploy_list.list_.append((Troops.dragon, (x_center(), y_bottom())))
                        deploy_list.list_.append((Troops.minion, (opp_troop.position[0], y_center())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                    elif((Troops.archer in deployable and total_elixir >=3) and Troops.archer not in my_troops):
                        deploy_list.list_.append((Troops.archer, (x_center(), y_bottom())))
                        deploy_list.list_.append((Troops.minion, (opp_troop.position[0], y_top())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)                
                    else:
                        deploy_list.list_.append((Troops.minion, (x_center(), y_bottom())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                elif((Troops.archer in deployable and total_elixir >=3) and Troops.archer not in my_troops):
                    if((Troops.dragon in deployable and total_elixir >=4) and Troops.dragon not in my_troops):
                        deploy_list.list_.append((Troops.archer, (opp_troop.position[0], y_center())))
                        deploy_list.list_.append((Troops.dragon, (opp_troop.position[0], y_top())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)
                    else:
                        deploy_list.list_.append((Troops.minion, (opp_troop.position[0], y_center())))
                        team_signal = team_signal + ", " + str(opp_troop.uid) if team_signal else str(opp_troop.uid)

        #Emergency state, if any troop gets too close to the tower
        if opp.position[1] <= 25:
            if(Troops.wizard in deployable and total_elixir >=5):
                deploy_list.list_.append((Troops.wizard, (opp.position[0], 0)))
            elif(Troops.dragon in deployable and total_elixir >=4):
                deploy_list.list_.append((Troops.dragon, (opp.position[0], opp.position[1])))
            elif(Troops.knight in deployable and total_elixir >=3):
                deploy_list.list_.append((Troops.knight, (opp.position[0], opp.position[1])))
            elif(Troops.minion in deployable and total_elixir >=3):
                deploy_list.list_.append((Troops.minion, (opp.position[0], opp.position[1])))
            elif(Troops.archer in deployable and total_elixir >=3):
                deploy_list.list_.append((Troops.archer, (opp.position[0], 10)))
            elif(Troops.prince in deployable and total_elixir >=5):
                deploy_list.list_.append((Troops.prince, (opp.position[0], opp.position[1])))
            elif(Troops.valkyrie in deployable and total_elixir >=4):
                deploy_list.list_.append((Troops.valkyrie, (opp.position[0], opp.position[1])))
        
    if total_elixir == 10 and total_enemy_elixir <=6 :
        if Troops.wizard in deployable:
            deploy_list.list_.append((Troops.wizard, (send_max_lane(max_lane), 45)))
        elif Troops.dragon in deployable:
            deploy_list.list_.append((Troops.dragon, (send_max_lane(max_lane), 45)))
        elif Troops.knight in deployable:
            deploy_list.list_.append((Troops.knight, (send_max_lane(max_lane), y_bottom())))
        elif Troops.prince in deployable:
            deploy_list.list_.append((Troops.prince, (send_max_lane(max_lane), y_bottom())))
        elif Troops.archer in deployable:
            deploy_list.list_.append((Troops.archer, (send_max_lane(max_lane), y_bottom())))
        elif Troops.valkyrie in deployable:
            deploy_list.list_.append((Troops.valkyrie, (send_max_lane(max_lane), y_bottom())))
            
    elif total_elixir == 10:
        if Troops.wizard in deployable:
            deploy_list.list_.append((Troops.wizard, (send_max_lane(max_lane), 5)))
        elif Troops.dragon in deployable:
            deploy_list.list_.append((Troops.dragon, (send_max_lane(max_lane), 5)))
        elif Troops.knight in deployable:
            deploy_list.list_.append((Troops.knight, (send_max_lane(max_lane), y_bottom())))
        elif Troops.prince in deployable:
            deploy_list.list_.append((Troops.prince, (send_max_lane(max_lane), y_bottom())))
        elif Troops.archer in deployable:
            deploy_list.list_.append((Troops.archer, (send_max_lane(max_lane), y_bottom())))
        elif Troops.valkyrie in deployable:
            deploy_list.list_.append((Troops.valkyrie, (send_max_lane(max_lane), y_bottom())))        
            
    
  
    while len(str(team_signal)) > 140:
        new_signal = team_signal.split(",")[1:]
        team_signal = ",".join(new_signal)