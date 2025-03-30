import random
from teams.helper_function import Troops, Utils

team_name = "Code_Warriors"
troops = [
    Troops.giant, Troops.archer, Troops.wizard,
    Troops.valkyrie, Troops.dragon, Troops.musketeer,
    Troops.skeleton, Troops.knight
]

deploy_list = Troops([])
team_signal = "first_deployment_done"


def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def random_position(min_x=-25, max_x=25, min_y=0, max_y=20):
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))

def deploy_random_position(troop_one, troop_two):
    if random.choice([True, False]):
        deploy_list.list_.append((troop_one, (0, 35)))
        deploy_list.list_.append((troop_two, (0, 25)))
        return 'right'
    else:
        deploy_list.list_.append((troop_one, (0, 35)))
        deploy_list.list_.append((troop_two, (0, 35)))
        return 'left'
    
def logic(arena_data: dict):
    global team_signal

    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    opp_elixir = opp_tower.total_elixir
    opp_troops = arena_data["OppTroops"]
    my_troops = arena_data["MyTroops"]
    available_troops = my_tower.deployable_troops
    current_elixir = my_tower.total_elixir
    current_time = my_tower.game_timer
    giant_flag = False
    initial_rush = False
    ground_counter = False 
    air_counter = False
    count_threat = 0
            
    if team_signal:
        first_troop = None
        second_troop = None

        # Prioritize Giant and Wizard Combo
        if Troops.wizard in available_troops and Troops.giant in available_troops:
            deploy_random_position(Troops.giant, Troops.wizard)
        elif Troops.valkyrie in available_troops and Troops.wizard in available_troops:
            deploy_random_position(Troops.valkyrie, Troops.wizard)        
        else:
            for troop in [Troops.dragon, Troops.giant, Troops.valkyrie, Troops.wizard]:
                if troop in available_troops:
                    first_troop = troop
                    break
            for troop in [Troops.valkyrie, Troops.dragon, Troops.wizard, Troops.giant]:
                if troop in available_troops and troop != first_troop:
                    second_troop = troop
                    break
            else:
                if first_troop:
                    deploy_list.list_.append((first_troop, (0, 10)))  
                if second_troop:
                    deploy_list.list_.append((second_troop, (0, 15)))  

        team_signal = ""

    for troop in opp_troops:
        if troop.position[1] < 35:
            count_threat += 1

    if count_threat >=1:
        giant_flag = True

    if giant_flag and Troops.giant in available_troops and current_elixir >=5:
        deploy_list.list_.append((Troops.giant, (0, 10)))
        giant_flag = False

    safe_deploy_position = all(troop.position[1] > 50 for troop in opp_troops)
    deployment_order = [Troops.wizard, Troops.valkyrie, Troops.dragon, Troops.knight]
    
    for troop in my_troops:
        if troop.position[1] < 50:
            deploy_y = 45 if safe_deploy_position else troop.position[1]
            
            for deploy_troop in deployment_order:
                if deploy_troop in available_troops and deploy_troop != troop.type:
                    deploy_list.list_.append((deploy_troop, (troop.position[0]-5, deploy_y)))
                    break
    if Troops.dragon in available_troops:
        for troop in opp_troops:
            if troop.type == Troops.dragon and troop.position[1] < 40:
                deploy_list.list_.append((Troops.dragon, (troop.position[0], troop.position[1])))
                break
    
    elif Troops.musketeer in  available_troops:
        for troop in opp_troops:
            if troop.type == Troops.dragon and troop.position[1] < 40:
                deploy_list.list_.append((Troops.musketeer, (troop.position[0], troop.position[1])))
    elif Troops.archer in  available_troops:
        for troop in opp_troops:
            if troop.type == Troops.dragon and troop.position[1] < 40:
                deploy_list.list_.append((Troops.archer, (troop.position[0], troop.position[1])))
                break

    if Troops.knight in available_troops:
        for troop in opp_troops:
            if troop.name in [Troops.wizard , Troops.valkyrie] and troop.position[1] < 50:
                deploy_list.list_.append((Troops.knight, (troop.position[0], troop.position[1])))
                break

    if Troops.skeleton in available_troops:
        for troop in opp_troops:
            if troop.name in [Troops.prince ,Troops.wizard , Troops.giant ] and troop.position[1] < 50:
                deploy_list.list_.append((Troops.skeleton, (troop.position[0], troop.position[1])))
                break

    for troop in opp_troops:
        if troop.type == Troops.prince and Troops.skeleton not in available_troops and troop.position[1]<50 :
            selected_troop = next((t for t in [Troops.archer,Troops.musketeer, Troops.knight, Troops.wizard , Troops.valkyrie , Troops.giant] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.minion and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.archer, Troops.wizard, Troops.dragon , Troops.valkyrie , Troops.giant] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.dragon or troop.type == Troops.musketeer and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.archer, Troops.dragon, Troops.wizard , Troops.valkyrie] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
        
    for troop in opp_troops:
        if troop.type == Troops.balloon and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.wizard, Troops.dragon, Troops.musketeer , Troops.archer] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    if Troops.musketeer in available_troops:
        for troop in opp_troops:
            if troop.type in [Troops.dragon , Troops.minion , Troops.balloon] and troop.position[1] < 40:
                deploy_list.list_.append((Troops.dragon, (troop.position[0], troop.position[1])))
                break
    
    if Troops.skeleton in available_troops:
        for troop in opp_troops:
            if troop.name in [Troops.prince ] and troop.position[1] < 50:
                deploy_list.list_.append((Troops.skeleton, (troop.position[0], troop.position[1])))
                break
    
    for troop in opp_troops:
        if troop.type == Troops.skeleton and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.valkyrie, Troops.skeleton, Troops.wizard , Troops.giant , Troops.dragon] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.wizard and troop.position[1]<50 :
            selected_troop = next((t for t in [Troops.wizard, Troops.giant, Troops.valkyrie, Troops.knight] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.barbarian and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.knight, Troops.valkyrie, Troops.archer, Troops.wizard] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.prince and Troops.skeleton not in available_troops and troop.position[1]<50 :
            selected_troop = next((t for t in [Troops.archer,Troops.musketeer, Troops.knight, Troops.wizard , Troops.valkyrie , Troops.giant] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.dragon or troop.type == Troops.musketeer and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.archer, Troops.dragon, Troops.musketeer , Troops.wizard , Troops.valkyrie] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.balloon and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.wizard, Troops.dragon, Troops.musketeer , Troops.archer , Troops.valkyrie] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.minion and troop.position[1]<40 :
            selected_troop = next((t for t in [Troops.archer,Troops.musketeer, Troops.wizard, Troops.dragon , Troops.valkyrie , Troops.giant] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    for troop in opp_troops:
        if troop.type == Troops.valkyrie and troop.position[1]<50 :
            selected_troop = next((t for t in [Troops.wizard, Troops.valkyrie, Troops.knight,  Troops.archer ,Troops.giant] if t in available_troops), None)

            if selected_troop:
                deploy_list.list_.append((selected_troop, (0, 6)))
            break
    if Troops.musketeer in available_troops:
        for troop in opp_troops:
            if troop.type in [Troops.dragon , Troops.minion , Troops.balloon] and troop.position[1] < 40:
                deploy_list.list_.append((Troops.dragon, (troop.position[0], troop.position[1])))
                break
           
    safe_deploy_position = all(troop.position[1] > 50 for troop in opp_troops)

    deployment_order = [Troops.wizard, Troops.valkyrie, Troops.dragon, Troops.knight]

    for troop in my_troops:
        if troop.position[1] < 50:
            deploy_y = 45 if safe_deploy_position else troop.position[1]
            
            for deploy_troop in deployment_order:
                if deploy_troop in available_troops and deploy_troop != troop.type:
                    deploy_list.list_.append((deploy_troop, (troop.position[0]-5, deploy_y)))
                    break

    if not deploy_list.list_ and available_troops:
        defensive_troops = [Troops.wizard, Troops.valkyrie , Troops.knight , Troops.dragon , Troops.archer]  
        for troop in defensive_troops:
            if troop in available_troops:
                deploy_list.list_.append((troop, (0, 5)))  
                return