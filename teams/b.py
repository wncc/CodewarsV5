from teams.helper_function import Troops, Utils

team_name = "DELHI"
troops = [Troops.wizard,Troops.minion,Troops.archer,Troops.giant,Troops.dragon,Troops.skeleton,Troops.balloon,Troops.barbarian]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    global team_signal
    mytower = arena_data["MyTower"]
    if mytower.game_timer < 10:
        deploy_list.deploy_minion((0,0))
    """
    WRITE YOUR CODE HERE 
    """