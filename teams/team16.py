import random
from teams.helper_function import Troops, Utils

team_name = "while(true) Win();"
troops = [
    Troops.wizard, Troops.minion, Troops.giant, Troops.prince,
    Troops.dragon, Troops.barbarian, Troops.valkyrie, Troops.skeleton
]

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
    opp_troops = arena_data["OppTroops"]
    
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name    
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    troops_all=["Archer", "Minion", "Knight", "Skeleton", "Dragon", "Valkyrie","Musketeer", "Giant", "Prince", "Barbarian", "Balloon", "Wizard"]
    troops_health={"Archer":334, "Minion":252, "Knight":1938, "Skeleton":89, "Dragon":1267, "Valkyrie":2097,"Musketeer":792, "Giant":5423, "Prince":1920, "Barbarian":736, "Balloon":2226, "Wizard":1100}
    troop_num = {"Archer":2, "Minion":3, "Knight":1, "Skeleton":10, "Dragon":1, "Valkyrie":1,"Musketeer":1, "Giant":1, "Prince":1, "Barbarian":3, "Balloon":1, "Wizard":1}
    points =[[] for j in range (0,8)]
    points[0] = [9/2, 9/3, 9, 8/10, 7, 8, 7, 6, 6, 9/3, 7, 5]# wizard
    points[1] = [0,0,0,0,0,0,0,0,0,0,0,0]
    points[1] = [5/2, 5/3, 9, 8/10, 6, 3, 5, 6, 6, 7/3, 6, 1] # minions
    #points[2] = [5/2, 6/3, 4, 3/10, 5, 3, 6, 6, 3, 7/3, 8, 2] #archer
    points[2] = [0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0] #giant
    points[3] = [8/2, 4/3, 6, 1/10, 2, 7, 8, 8, 5, 7/3, 0, 5] #prince
    points[4] = [5/2, 7/3, 8, 9/10, 5, 7, 4, 7, 7, 8/3, 8, 2] #dragon
    # points[5] = [0,0,0,0,0,0,0,0,0,0,0,0] #Musketeer
    # points[5] = [6/2, 5/3, 6, 2/10, 6, 4, 5, 7, 4, 4/3, 9, 2] #Musketeer
    points[5] = [0,0,0,0,0,0,0,0,0,0,0,0]
    #points[5] = [8/2, 0/3, 9, 2/10, 1, 5, 8, 9, 8, 5, 0, 4] #Barbarian
    points[6] = [8/2, 2/3, 6, 8/10, 2, 5, 7, 6, 3, 8/3, 0, 4] # valkyrie valkyrie vs skeleton if positioned perfectly wins easily
    points[7] = [9/2, 0/3, 9, 5/10, 0, 7, 8, 9, 8, 7/3, 0, 7]# skeleton    
    # --- Score Our Troops (only from deployable troops) ---
    my_troops = ["Wizard", "Minion", "Giant", "Prince", "Dragon", "Barbarian", "Valkyrie", "Skeleton"]
    elixir_my_troops = [5,3.1,5,5,4,2.9,4,3]
    k = 2
    ranged = [5.5*k,2*k,0,0,3.5*k,0,0,0]
    deployable = my_tower.deployable_troops
    l_best_troop = None
    r_best_troop = None
    l_best_score = -100
    r_best_score = -100
    # Loop over our full troop list, but only consider those that are deployable.
    points_val = {}
    defensive = False
    op_health = 0
    for troop in my_troops:
        if troop not in deployable:
            continue
        l_score = 0
        r_score = 0
        for otroop in opp_troops:
            troop_l =0
            troop_r = 0
            if otroop.position[1]<60:
                op_health+=(otroop.health/troops_health[otroop.name])/troop_num[otroop.name]
            if otroop.position[0]<0:
                troop_l+=1
                l_score += (points[my_troops.index(troop)][troops_all.index(otroop.name)]*otroop.health/troops_health[otroop.name]*((100-otroop.position[1])**3/2000000))
            else:
                troop_r+=1
                r_score += (points[my_troops.index(troop)][troops_all.index(otroop.name)]*otroop.health/troops_health[otroop.name]*((100-otroop.position[1])**3)/2000000)
        #l_score -= 0.2*elixir_my_troops[my_troops.index(troop)]
        #r_score -= 0.2*elixir_my_troops[my_troops.index(troop)]
        if l_score > l_best_score:
            l_best_score = l_score
            l_best_troop = troop
        if r_score > r_best_score:
            r_best_score = r_score
            r_best_troop = troop
        points_val[troop] = l_score + r_score
    my_health = 0
    def_troop=0
    for mtroop in arena_data["MyTroops"]:
        if mtroop.position[1]<=20:
            def_troop +=(mtroop.health/troops_health[mtroop.name])/troop_num[mtroop.name]
        if mtroop.position[1]<50:
            my_health+=(mtroop.health/troops_health[mtroop.name])/troop_num[mtroop.name]
    if(1 + my_health <op_health) or (arena_data["MyTower"].health - arena_data["OppTower"].health)>1000:
        defensive=True

    points_val = dict(sorted(points_val.items(), key=lambda item: item[1],reverse=True))
    # --- Deployment Position ---
    y_min = 100
    if((not defensive) and len(opp_troops)>=1):
        for troop in arena_data["OppTroops"]:
            y_min = y_min if y_min<troop.position[1] else troop.position[1]
        if y_min<15 and arena_data["MyTower"].total_elixir<5:
            min_e = 6
            for troop in deployable:
                if(elixir_my_troops[my_troops.index(troop)])<min_e and min_e>arena_data["MyTower"].total_elixir:
                    min_e = elixir_my_troops[my_troops.index(troop)]
                    troop_dep = troop
            deploy_list.list_.append((troop_dep, (0,12)))

        if l_best_score > r_best_score:
            best_troop = l_best_troop
        else:
            best_troop = r_best_troop
        if best_troop =="Skeleton":
            isWiz = False
            isVal = False
            isPrince = False

            for troop in arena_data["OppTroops"]:
                if troop.name == "Prince":
                    prince = troop
                    isPrince = True
                    break
                elif troop.name == "Wizard":
                    wiz = troop
                    isWiz = True
                elif troop.name == "Valkyrie":
                    val = troop
                    isVal = True

            if (def_troop>0.75 or y_min>30) and isWiz and wiz.position[1] < 65:
                if wiz.position[1] < 45:
                    pos = (wiz.position[0], wiz.position[1] + 3.5)
                    deploy_list.list_.append((best_troop, pos))
            elif (def_troop>0.75 or y_min>30) and isPrince and prince.position[1] < 65:
                if prince.position[1] < 45:
                    pos = (prince.position[0], prince.position[1] + 3.5)
                    deploy_list.list_.append((best_troop, pos))
            elif (def_troop>0.75 or y_min>30) and isVal and val.position[1] < 65:
                if val.position[1] < 45:
                    pos = (val.position[0], val.position[1] + 3)
                    deploy_list.list_.append((best_troop, pos))
            else:
                for key in points_val:
                    y_pos = y_min - ranged[my_troops.index(best_troop)]
                    if y_pos > 20:
                        y_pos = 20
                    elif y_pos < 0:
                        y_pos = 0
                    if key != "Skeleton" and key!="Barbarian":
                        deploy_list.list_.append((key, (0, y_pos)))

        elif best_troop =="Barbarian":
            isWiz = False
            isVal = False
            isPrince = False

            for troop in arena_data["OppTroops"]:
                if troop.name == "Prince":
                    prince = troop
                    isPrince = True
                    break
                elif troop.name == "Wizard":
                    wiz = troop
                    isWiz = True
                elif troop.name == "Valkyrie":
                    val = troop
                    isVal = True

            if isWiz and wiz.position[1] < 50:
                if wiz.position[1] < 45:
                    pos = (wiz.position[0], wiz.position[1] + 5)
                    deploy_list.list_.append((best_troop, pos))
            elif isPrince and prince.position[1] < 50:
                if prince.position[1] < 45:
                    pos = (prince.position[0], prince.position[1] + 5)
                    deploy_list.list_.append((best_troop, pos))
            elif isVal and val.position[1] < 50:
                if val.position[1] < 45:
                    pos = (val.position[0], val.position[1] + 5)
                    deploy_list.list_.append((best_troop, pos))
            else:
                for key in points_val:
                    y_pos = y_min - ranged[my_troops.index(best_troop)]
                    if y_pos > 20:
                        y_pos = 20
                    elif y_pos < 0:
                        y_pos = 0
                    if key != "Barbarian" and key!="Skeleton":
                        deploy_list.list_.append((key, (0, y_pos)))
        elif best_troop == "Prince":
            isWiz = False
            isVal = False
            if(len(opp_troops) <5):
                for troop in arena_data["MyTroops"]:
                    if(troop.name == "Wizard"):
                        wiz = troop
                        isWiz = True
                    elif (troop.name == "Valkyrie"):
                        val = troop
                        isVal = True
                if(isWiz):
                    deploy_list.list_.append(("Prince", (wiz.position[0], wiz.position[1]-3)))
                elif(isVal):
                    deploy_list.list_.append(("Prince", (val.position[0], val.position[1]-10)))
                else:
                    if(troop_l< troop_r and troop_l==0):
                        deploy_list.list_.append(("Prince", (-20,50)))
                    elif(troop_r==0):
                        deploy_list.list_.append(("Prince", (+20,50)))
                    else:
                        for key in points_val:
                            y_pos = y_min - ranged[my_troops.index(best_troop)]
                            if y_pos > 20:
                                y_pos = 20
                            elif y_pos < 0:
                                y_pos = 0
                            if key != "Prince":
                                deploy_list.list_.append((key, (0, y_pos)))
            else:   
                for key in points_val:
                    y_pos = y_min - ranged[my_troops.index(best_troop)]
                    if y_pos > 20:
                        y_pos = 20
                    elif y_pos < 0:
                        y_pos = 0
                    if key != "Prince":
                        deploy_list.list_.append((key, (0, y_pos)))
        elif best_troop is not None:
            y_pos = y_min - ranged[my_troops.index(best_troop)]
            if(y_pos>50):
                y_pos = 50
            elif(y_pos<0):
                y_pos = 0
            if l_best_score <= r_best_score:
                deploy_position = (random_x(0,10), 10)
            else:
                deploy_position = (random_x(-10,0),  10)
            deploy_list.list_.append((best_troop,deploy_position))
        else:
            if "Giant" in deployable:
                deploy_list.list_.append(("Giant", (0, 0)))
            elif deployable:
                deploy_list.list_.append((deployable[0], (0, 0)))
    elif((not defensive) and len(opp_troops)==0):
        if "Prince" in deployable and arena_data["MyTower"].total_elixir>=7:
            if(len(opp_troops)==0):
                deploy_list.list_.append(("Prince",(20 * random_x(-1,1),min(45, 10+10*len(arena_data["MyTroops"]))))) 
        elif "Wizard" in deployable and arena_data["MyTower"].total_elixir>=8:
            if(len(opp_troops)==0):
                deploy_list.list_.append(("Wizard",(0,min(45, 10+10*len(arena_data["MyTroops"])))))
        elif "Dragon" in deployable and arena_data["MyTower"].total_elixir>=7:
            if(len(opp_troops)==0):
                deploy_list.list_.append(("Dragon",(0,min(45, 10+10*len(arena_data["MyTroops"]))))) 
        elif "Valkyrie" in deployable and arena_data["MyTower"].total_elixir>=6:
            if(len(opp_troops)==0):
                deploy_list.list_.append(("Valkyrie",(0,min(45, 10+10*len(arena_data["MyTroops"]))))) 
        elif "Giant" in deployable:
            if(len(opp_troops)==0):
                deploy_list.list_.append(("Giant",(0,10))) 
            
    else:
        for troop in arena_data["OppTroops"]:
            y_min = y_min if y_min<troop.position[1] else troop.position[1]
        if y_min<15 and arena_data["MyTower"].total_elixir<5:
            min_e = 6
            for troop in deployable:
                if(elixir_my_troops[my_troops.index(troop)])<min_e and min_e>arena_data["MyTower"].total_elixir:
                    min_e = elixir_my_troops[my_troops.index(troop)]
                    troop_dep = troop
            deploy_list.list_.append((troop_dep, (0,12)))
        if "Giant" in deployable and arena_data["MyTower"].total_elixir>=7:
            deploy_list.list_.append(("Giant", (0, 5)))
        if "Giant" in arena_data["MyTroops"]:
            if "Wizard" in deployable:
                deploy_list.list_.append(("Wizard",(0,5))) 

        if l_best_score > r_best_score:
            best_troop = l_best_troop
        else:
            best_troop = r_best_troop
        if best_troop =="Skeleton":
            isWiz = False
            isVal = False
            isPrince = False

            for troop in arena_data["OppTroops"]:
                if troop.name == "Prince":
                    prince = troop
                    isPrince = True
                    break
                elif troop.name == "Wizard":
                    wiz = troop
                    isWiz = True
                elif troop.name == "Valkyrie":
                    val = troop
                    isVal = True

            
            if (def_troop>0.75 or y_min>30) and isWiz and wiz.position[1] < 50:
                if wiz.position[1] < 45:
                    pos = (wiz.position[0], wiz.position[1] + 3.5)
                    deploy_list.list_.append((best_troop, pos))
            elif (def_troop>0.75 or y_min>30) and isPrince and prince.position[1] < 65:
                if prince.position[1] < 45:
                    pos = (prince.position[0], prince.position[1] + 3.5)
                    deploy_list.list_.append((best_troop, pos))
            elif (def_troop>0.75 or y_min>30) and isVal and val.position[1] < 65:
                if val.position[1] < 45:
                    pos = (val.position[0], val.position[1] + 3)
                    deploy_list.list_.append((best_troop, pos))
            else:
                for key in points_val:
                    if key != "Skeleton" and key!="Barbarian":
                        deploy_list.list_.append((key, (0, 10)))

        elif best_troop =="Barbarian":
            isWiz = False
            isVal = False
            isPrince = False

            for troop in arena_data["OppTroops"]:
                if troop.name == "Prince":
                    prince = troop
                    isPrince = True
                    break
                elif troop.name == "Wizard":
                    wiz = troop
                    isWiz = True
                elif troop.name == "Valkyrie":
                    val = troop
                    isVal = True


            if y_min>30 and isWiz and wiz.position[1] < 50:
                if wiz.position[1] < 45:
                    pos = (wiz.position[0], wiz.position[1] + 5)
                    deploy_list.list_.append((best_troop, pos))
            elif y_min>30 and isPrince and prince.position[1] < 50:
                if prince.position[1] < 45:
                    pos = (prince.position[0], prince.position[1] + 5)
                    deploy_list.list_.append((best_troop, pos))
                    print(pos)
            elif y_min>30 and isVal and val.position[1] < 50:
                if val.position[1] < 45:
                    pos = (val.position[0], val.position[1] + 5)
                    deploy_list.list_.append((best_troop, pos))
            else:
                for key in points_val:
                    if key != "Barbarian" and key!="Skeleton":
                        deploy_list.list_.append((key, (0, 10)))
        elif best_troop == "Prince":
            isWiz = False
            isVal = False
            for troop in arena_data["MyTroops"]:
                if(troop.name == "Wizard"):
                    wiz = troop
                    isWiz = True
                elif (troop.name == "Valkyrie"):
                    val = troop
                    isVal = True
            if(isWiz):
                deploy_list.list_.append(("Prince", (wiz.position[0], wiz.position[1]-3)))
            elif(isVal):
                deploy_list.list_.append(("Prince", (val.position[0], val.position[1]-10)))
            else:
                for key in points_val:
                    if key != "Prince":
                        deploy_list.list_.append((key, (0, 10)))
        elif best_troop is not None:
            y_pos = y_min - 2*ranged[my_troops.index(best_troop)]
            if(y_pos>20):
                y_pos = 20
            elif(y_pos<0):
                y_pos = 0
            if l_best_score <= r_best_score:
                deploy_position = (random_x(0,10), 10)
            else:
                deploy_position = (random_x(-10,0), 10)
            deploy_list.list_.append((best_troop,deploy_position))
        else:
            if "Giant" in deployable:
                deploy_list.list_.append(("Giant", (0, 5)))
            elif deployable:
                deploy_list.list_.append((deployable[0], (0, 0)))






##Just to reach 400 lines of code :)